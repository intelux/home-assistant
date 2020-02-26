"""Platform for light integration."""
import logging

import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light
from homeassistant.const import CONF_HOST, CONF_TOKEN
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_HOST): cv.string, vol.Optional(CONF_TOKEN): cv.string}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    # host = config[CONF_HOST]
    # token = config.get(CONF_TOKEN)

    # Setup connection with devices/cloud

    # Verify that passed in configuration works
    if not True:
        _LOGGER.error("Could not connect to AwesomeLight hub")
        return

    # Add devices
    add_entities(AwesomeLight())


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the lights from a config entry."""
    pass


class AwesomeLight(Light):
    """Representation of an Awesome Light."""

    def __init__(self):
        """Initialize an AwesomeLight."""
        self._name = "Some light"
        self._state = None
        self._brightness = None

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on.

        You can skip the brightness part if your light does not support
        brightness control.
        """
        self._light.brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        self._light.turn_on()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        pass
        # self._light.turn_off()

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        pass
        # self._light.update()
        # self._state = self._light.is_on()
        # self._brightness = self._light.brightness
