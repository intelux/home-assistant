"""Platform for light integration."""
import logging

from ohm_led import Device
import voluptuous as vol

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_HS_COLOR,
    PLATFORM_SCHEMA,
    SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR,
    Light,
)
from homeassistant.const import CONF_URL
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_URL): cv.string})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Awesome Light platform."""
    pass


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the lights from a config entry."""
    device = Device(base_url=config_entry.data[CONF_URL])
    info = await device.get_info()
    state = await device.get_state()
    led_stripe = OhmLEDLight(device=device, info=info, state=state)
    async_add_entities([led_stripe])


class OhmLEDLight(Light):
    """Representation of an Ohm-Made LED stripe."""

    def __init__(self, device, info, state):
        """Initialize a LED stripe."""
        self._device = device
        self._info = info
        self._state = state

    @property
    def unique_id(self):
        """Return the unique ID of this Ohm-LED device."""
        return self._info.get("name", "ohm-led")

    @property
    def device_id(self):
        """Return the ID of this Ohm-LED device."""
        return self.unique_id

    @property
    def name(self):
        """Return the name of this Ohm-LED device."""
        return self.unique_id

    @property
    def brightness(self):
        """Return the brightness of the light.

        This method is optional. Removing it indicates to Home Assistant
        that brightness is not supported for this light.
        """
        return self._state["value"]

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state["mode"] != "off"

    @property
    def supported_features(self):
        """Flag supported features."""
        return [
            SUPPORT_BRIGHTNESS,
            SUPPORT_COLOR,
        ]

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.device_id)},
            "name": self.name,
            "num_led": self._info.get("num-led", 0),
            "host": self.device.base_url,
        }

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        hsv = (None, None, None)

        if ATTR_HS_COLOR in kwargs:
            hsv[0] = int(kwargs[ATTR_HS_COLOR][0] / 360 * 255)
            hsv[1] = int(kwargs[ATTR_HS_COLOR][1] / 100 * 255)

        if ATTR_BRIGHTNESS in kwargs:
            hsv[2] = int(kwargs[ATTR_BRIGHTNESS])

        await self._device.on(hsv=hsv)

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        await self._device.off()

    async def async_update(self):
        """Fetch new state data for this light."""
        self._state = await self._device.get_state()
