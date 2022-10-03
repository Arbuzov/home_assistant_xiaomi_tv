"""Add support for the Xiaomi TVs."""
from __future__ import annotations

import logging

from homeassistant.components.media_player import (
    PLATFORM_SCHEMA,
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import pymitv
import voluptuous as vol

from .const import DOMAIN
from .select import XiaomiTVInputSelect
from .switch import XiaomiTVStatusSwitch


DEFAULT_NAME = "Xiaomi TV"

_LOGGER = logging.getLogger(__name__)

# No host is needed for configuration, however it can be set.
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Xiaomi TV platform."""

    # If a hostname is set. Discovery is skipped.
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    _LOGGER.error(config)
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if host is not None:
        # Check if there's a valid TV at the IP address.
        if not pymitv.Discover().check_ip(host):
            _LOGGER.error(
                "Could not find Xiaomi TV with specified IP: %s", host)
        else:
            # Register TV with Home Assistant.
            hass.data[DOMAIN][f'{DOMAIN}_{host}'] = {'state': STATE_OFF}
            add_entities([
                XiaomiTV(host, name, hass),
                XiaomiTVStatusSwitch(host, name, hass)],
                XiaomiTVStatusSwitch(host, name, hass)])
    else:
        # Otherwise, discover TVs on network.
        entities = []
        for tv in pymitv.Discover().scan():
            hass.data[DOMAIN][f'{DOMAIN}_{host}'] = {'state': STATE_OFF}
            entities.append(XiaomiTV(tv, DEFAULT_NAME, hass))
            entities.append(XiaomiTVStatusSwitch(tv, DEFAULT_NAME, hass))
            entities.append(XiaomiTVInputSelect(tv, DEFAULT_NAME, hass))
        add_entities(entities)


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback):
    host = entry.as_dict().get('data').get(CONF_HOST)
    name = entry.as_dict().get('data').get(CONF_NAME)
    async_add_entities([XiaomiTV(host, name, hass)])
    return True


class XiaomiTV(MediaPlayerEntity):
    """Represent the Xiaomi TV for Home Assistant."""

    _attr_supported_features = (
        MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    _attr_device_class = MediaPlayerDeviceClass.TV

    def __init__(self, ip: str, name: str, hass: HomeAssistant):
        """Receive IP address and name to construct class."""

        # Initialize the Xiaomi TV.
        self._tv = pymitv.TV(ip)
        # Default name value, only to be overridden by user.
        self._name = name
        self._ip = ip
        self._config_id = f'{DOMAIN}_{self._ip}'
        self._attr_unique_id = f'{self._config_id}_{self.__class__.__name__}'
        self._hass = hass

    @property
    def name(self):
        """Return the display name of this TV."""
        return self._name

    @property
    def state(self):
        """Return _state variable, containing the appropriate constant."""
        return self._hass.data[DOMAIN][self._config_id].get('state', None)

    @property
    def source(self):
        return self._hass.data[DOMAIN][self._config_id].get('source', None)

    def select_source(self, source):
        """Select input source."""
        self._tv.change_source(source)
        self._hass.data[DOMAIN][self._config_id].setDefault('source', source)

    @property
    def assumed_state(self):
        """Indicate that state is assumed."""
        return True

    def turn_off(self):
        """
        Instruct the TV to turn sleep.

        This is done instead of turning off,
        because the TV won't accept any input when turned off. Thus, the user
        would be unable to turn the TV back on, unless it's done manually.
        """
        if self._state != STATE_OFF:
            self._tv.sleep()

            self._hass.data[DOMAIN][self._config_id].setDefault(
                'state', STATE_OFF)

    def turn_on(self):
        """Wake the TV back up from sleep."""
        if self._state != STATE_ON:
            self._tv.wake()

            self._hass.data[DOMAIN][self._config_id].setDefault(
                'state', STATE_ON)

    def volume_up(self):
        """Increase volume by one."""
        self._tv.volume_up()

    def volume_down(self):
        """Decrease volume by one."""
        self._tv.volume_down()

    @property
    def device_info(self):
        """Shared entity info information"""
        return {
            'identifiers': {
                (DOMAIN, self._ip),
                ('hacs', 'home_assistant_xiaomi_tv'),
                ('device_tracker', 'mitv4s'),
                ('mobile_app', 'mitv4s'),
                ('mobile_app', 'mitv4s'),
            },
            'name': self._name,
            'manufacturer': 'xiaomi'
        }
