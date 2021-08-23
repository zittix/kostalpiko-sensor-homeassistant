"""Config flow for Kostal piko integration."""

# import logging

import voluptuous as vol
from requests.exceptions import HTTPError, ConnectTimeout
from .sensor import PikoData
from homeassistant import config_entries, exceptions
import homeassistant.helpers.config_validation as cv

from homeassistant.const import (
    CONF_NAME,
    CONF_HOST,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_MONITORED_CONDITIONS,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.util import slugify

from .const import DOMAIN, DEFAULT_NAME, SENSOR_TYPES  # pylint:disable=unused-import


# DATA_SCHEMA = vol.Schema({"host": str, "username": str, "password": str})

SUPPORTED_SENSOR_TYPES = list(SENSOR_TYPES)

DEFAULT_MONITORED_CONDITIONS = [
    "solar_generator_power",
    "total_solar_power"
]


@callback
def kostal_entries(hass: HomeAssistant):
    """Return the hosts for the domain."""
    return set(
        (entry.data[CONF_HOST]) for entry in hass.config_entries.async_entries(DOMAIN)
    )


class KostalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kostal piko."""

    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    # @staticmethod
    # @callback
    # def async_get_options_flow(config_entry):
    #     """Get the options flow for this handler."""
    #     return KostalOptionsFlowHandler(config_entry)

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._errors = {}

    def _host_in_configuration_exists(self, host) -> bool:
        """Return True if site_id exists in configuration."""
        if host in kostal_entries(self.hass):
            return True
        return False

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:

            name = slugify(user_input.get(CONF_NAME, DEFAULT_NAME))
            if self._host_in_configuration_exists(user_input[CONF_HOST]):
                self._errors[CONF_HOST] = "host_exists"
            else:
                host = user_input[CONF_HOST]
                username = user_input[CONF_USERNAME]
                password = user_input[CONF_PASSWORD]
                conditions = user_input[CONF_MONITORED_CONDITIONS]
                return self.async_create_entry(
                        title=name,
                        data={
                            CONF_HOST: host,
                            CONF_USERNAME: username,
                            CONF_PASSWORD: password,
                            CONF_MONITORED_CONDITIONS: conditions,
                        },
                    )
        else:
            user_input = {}
            user_input[CONF_NAME] = DEFAULT_NAME
            user_input[CONF_HOST] = "http://"
            user_input[CONF_USERNAME] = ""
            user_input[CONF_PASSWORD] = ""
            user_input[CONF_MONITORED_CONDITIONS] = DEFAULT_MONITORED_CONDITIONS

        default_monitored_conditions = (
            [] if self._async_current_entries() else DEFAULT_MONITORED_CONDITIONS
        )
        setup_schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME, default=user_input.get(CONF_NAME, DEFAULT_NAME)
                ): str,
                vol.Required(CONF_HOST, default=user_input[CONF_HOST]): str,
                vol.Optional(
                    CONF_USERNAME, default=user_input[CONF_PASSWORD]
                ): str,
                vol.Optional(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                vol.Required(
                    CONF_MONITORED_CONDITIONS, default=default_monitored_conditions
                ): cv.multi_select(SUPPORTED_SENSOR_TYPES),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=setup_schema, errors=self._errors
        )

    async def async_step_import(self, user_input=None):
        """Import a config entry."""
        if self._host_in_configuration_exists(user_input[CONF_HOST]):
            return self.async_abort(reason="host_exists")
        return await self.async_step_user(user_input)


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
