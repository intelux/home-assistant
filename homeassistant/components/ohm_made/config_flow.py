"""Config flow for Ohm-made integration."""
import logging

from ohm_led import Device
import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import DOMAIN  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({"url": str})


async def validate_input(hass: core.HomeAssistant, data):
    """Validate the user input allows us to connect.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    url = data["url"]
    device = Device(base_url=url)

    try:
        info = await device.get_info()
        # TODO: Fetch the type of the device once it is known.
        name = info["name"]
    except Exception:  # pylint: disable=broad-except
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {"title": f"{name}"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ohm-made."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # device_unique_id = self.hass["host"]
        # await self.async_set_unique_id(device_unique_id)
        # self._abort_if_unique_id_configured()

        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
