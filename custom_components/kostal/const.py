"""Constants for the Kostal piko integration."""
from datetime import timedelta

from homeassistant.const import (
    POWER_WATT,
    ELECTRIC_POTENTIAL_VOLT,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_WATT_HOUR
)
from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    SensorEntityDescription
)

DOMAIN = "kostal"

DEFAULT_NAME = "Kostal piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=1)

SENSOR_TYPES = {
    "solar_generator_power": SensorEntityDescription(
        key="solar_generator_power",
        name="Solar generator power",
        unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
        icon="mdi:solar-power"
    ),
    "total_solar_power": SensorEntityDescription(
        key="total_solar_power",
        name="Total generated power",
        unit_of_measurement=ENERGY_WATT_HOUR,
        device_class=DEVICE_CLASS_ENERGY,
        state_class="total_increasing",
        icon="mdi:solar-power"
    ),
    "ac_voltage": SensorEntityDescription(
        key="ac_voltage",
        name="AC Voltage",
        unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
        icon="mdi:current-ac"
    ),
    "ac_current": SensorEntityDescription(
        key="ac_current",
        name="AC Current",
        unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        device_class=DEVICE_CLASS_CURRENT,
        state_class=STATE_CLASS_MEASUREMENT,
        icon="mdi:flash"
    )
}
