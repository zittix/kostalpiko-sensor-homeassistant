"""The Kostal piko integration."""


import logging
import urllib.request
import xmltodict

from homeassistant.const import (
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_HOST,
    CONF_MONITORED_CONDITIONS,
)

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle


from .const import SENSOR_TYPES, MIN_TIME_BETWEEN_UPDATES, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Add an Kostal piko entry."""
    # Add the needed sensors to hass
    data = PikoData(entry.data[CONF_HOST], entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD], hass)

    entities = []

    for sensor in entry.data[CONF_MONITORED_CONDITIONS]:
        entities.append(PikoInverter(data, sensor, entry.title))
    async_add_entities(entities)


class PikoInverter(Entity):
    """Representation of a Piko inverter."""

    def __init__(self, piko_data, sensor_type, name):
        """Initialize the sensor."""
        self._sensor = SENSOR_TYPES[sensor_type][0]
        self._name = name
        self.type = sensor_type
        self.piko = piko_data
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self.serial_number = None
        self.model = None
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._name, self._sensor)

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def icon(self):
        """Return icon."""
        return self._icon

    @property
    def unique_id(self):
        """Return unique id based on device serial and variable."""
        return "{} {}".format(self.serial_number, self._sensor)

    @property
    def device_info(self):
        """Return information about the device."""
        return {
            "identifiers": {(DOMAIN, self.serial_number)},
            "name": self._name,
            "manufacturer": "Kostal",
            "model": self.model,
        }

    def update(self):
        """Update data."""
        self.piko.update()
        self.serial_number = self.piko.info['sn']
        self.model = self.piko.info['model']
        if self.type == "solar_generator_power":
            if "AC_Power" in self.piko.measurements:
                self._state = self.piko.measurements['AC_Power']
            else:
                return "No value available"
        elif self.type == "ac_voltage":
            if "AC_Voltage" in self.piko.measurements:
                self._state = self.piko.measurements['AC_Voltage']
            else:
                return "No value available"
        elif self.type == "ac_current":
            if "AC_Current" in self.piko.measurements:
                self._state = self.piko.measurements['AC_Current']
            else:
                return "No value available"


class PikoData(Entity):
    """Representation of a Piko inverter."""

    def __init__(self, host, username, password, hass):
        """Initialize the data object."""
        self.host = host
        self.hass = hass
        self.info = {}
        self.measurements = None
        self.retrieve()

    def _retrieve_page(self, url):
        with urllib.request.urlopen(self.host + url) as f:
            return f.read().decode('utf-8')

    def retrieve(self):
        page = self._retrieve_page("/all.xml")
        obj = xmltodict.parse(page)
        self.info['model'] = obj["root"]["Device"]["@Name"]
        self.info['sn'] = obj["root"]["Device"]["@Serial"]
        self.measurements = {}
        for i in obj["root"]["Device"]["Measurements"]["Measurement"]:
            if '@Value' in i and '@Type' in i:
                self.measurements[i["@Type"]] = float(i["@Value"])
# <Measurement Value="241.4" Unit="V" Type="AC_Voltage"/>
# <Measurement Value="0.876" Unit="A" Type="AC_Current"/>
# <Measurement Value="206.7" Unit="W" Type="AC_Power"/>
# <Measurement Value="205.8" Unit="W" Type="AC_Power_fast"/>
# <Measurement Value="49.976" Unit="Hz" Type="AC_Frequency"/>
# <Measurement Value="267.9" Unit="V" Type="DC_Voltage"/>
# <Measurement Value="0.854" Unit="A" Type="DC_Current"/>
# <Measurement Value="357.2" Unit="V" Type="LINK_Voltage"/>
# <Measurement Unit="W" Type="GridPower"/>
# <Measurement Unit="W" Type="GridConsumedPower"/>
# <Measurement Unit="W" Type="GridInjectedPower"/>
# <Measurement Unit="W" Type="OwnConsumedPower"/>
# <Measurement Value="100.0" Unit="%" Type="Derating"/>


    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update inverter data."""
        # pylint: disable=protected-access

        _LOGGER.debug(self.data)
        _LOGGER.debug(self.ba_data)

if __name__ == "__main__":
    import sys
    data = PikoData(sys.argv[1], None, None, None)
    print(data.measurements)
    print(data.info)