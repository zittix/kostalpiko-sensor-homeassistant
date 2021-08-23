"""Constants for the Kostal piko integration."""
from datetime import timedelta

from homeassistant.const import (
    POWER_WATT,
    ELECTRIC_POTENTIAL_VOLT,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_WATT_HOUR
)
from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT
)

DOMAIN = "kostal"

DEFAULT_NAME = "Kostal piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=1)

SENSOR_TYPES = {
    "solar_generator_power": ["Solar generator power", POWER_WATT, "mdi:solar-power", STATE_CLASS_MEASUREMENT, "power"],
    "total_solar_power": ["Total generated power", ENERGY_WATT_HOUR, "mdi:solar-power", "total_increasing", "energy"],
    "ac_voltage": ["AC Voltage", ELECTRIC_POTENTIAL_VOLT, "mdi:current-ac", STATE_CLASS_MEASUREMENT, "voltage"],
    "ac_current": ["AC Current", ELECTRIC_CURRENT_AMPERE, "mdi:flash", STATE_CLASS_MEASUREMENT, "current"],
}
