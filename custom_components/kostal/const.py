"""Constants for the Kostal piko integration."""
from datetime import timedelta

from homeassistant.const import UnitOfElectricCurrent, UnitOfPower, UnitOfElectricPotential, UnitOfEnergy

from homeassistant.components.sensor.const import SensorStateClass, SensorDeviceClass
from homeassistant.components.sensor import SensorEntityDescription

DOMAIN = "kostal"

DEFAULT_NAME = "Kostal piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=1)

SENSOR_TYPES = {
    "solar_generator_power": SensorEntityDescription(
        key="solar_generator_power",
        name="Solar generator power",
        unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power"
    ),
    "total_solar_power": SensorEntityDescription(
        key="total_solar_power",
        name="Total generated power",
        unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class="total_increasing",
        icon="mdi:solar-power"
    ),
    "ac_voltage": SensorEntityDescription(
        key="ac_voltage",
        name="AC Voltage",
        unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:current-ac"
    ),
    "ac_current": SensorEntityDescription(
        key="ac_current",
        name="AC Current",
        unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:flash"
    )
}
