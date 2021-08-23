"""Constants for the Kostal piko integration."""
from datetime import timedelta

from homeassistant.const import (
    POWER_WATT,
    ELECTRIC_POTENTIAL_VOLT,
    ELECTRICAL_CURRENT_AMPERE,
)

DOMAIN = "kostal"

DEFAULT_NAME = "Kostal piko"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=1)

SENSOR_TYPES = {
    "solar_generator_power": ["Solar generator power", POWER_WATT, "mdi:solar-power"],
    "ac_voltage": ["AC Voltage", ELECTRIC_POTENTIAL_VOLT, "mdi:current-ac"],
    "ac_current": ["AC Current", ELECTRICAL_CURRENT_AMPERE, "mdi:flash"],
}
