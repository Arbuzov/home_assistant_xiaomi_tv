"""Add support for the Xiaomi TVs."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import homeassistant.helpers.config_validation as cv
import pymitv
import voluptuous as vol
from homeassistant.components.media_player import (PLATFORM_SCHEMA,
                                                   MediaPlayerDeviceClass,
                                                   MediaPlayerEntity,
                                                   MediaPlayerEntityFeature,
                                                   MediaType)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN
from .switch import XiaomiTVStatusSwitch

DEFAULT_NAME = 'Xiaomi TV'

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
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if f'{DOMAIN}_{host}' not in hass.data[DOMAIN]:
        hass.data[DOMAIN][f'{DOMAIN}_{host}'] = {}
    if host is not None:
        # Check if there's a valid TV at the IP address.
        if not pymitv.Discover().check_ip(host):
            _LOGGER.error(
                'Could not find Xiaomi TV with specified IP: %s', host)
        else:
            # Register TV with Home Assistant.
            hass.data[DOMAIN][f'{DOMAIN}_{host}'] = {}
            add_entities([
                XiaomiTV(host, name, hass),
                XiaomiTVStatusSwitch(host, name, hass)
            ])
    else:
        # Otherwise, discover TVs on network.
        entities = []
        for tv in pymitv.Discover().scan():
            hass.data[DOMAIN][f'{DOMAIN}_{host}'] = {'state': STATE_OFF}
            entities.append(XiaomiTV(tv, DEFAULT_NAME, hass))
            entities.append(XiaomiTVStatusSwitch(tv, DEFAULT_NAME, hass))
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
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.BROWSE_MEDIA
        | MediaPlayerEntityFeature.PLAY_MEDIA
    )

    _attr_device_class = MediaPlayerDeviceClass.TV
    _attr_source_list = ['hdmi1', 'hdmi2', 'cast']
    _app_list = None

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
        self._volume = 1
        self._max_volume = 1

    @property
    def name(self):
        """Return the display name of this TV."""
        return self._name

    @property
    def state(self):
        """Return _state variable, containing the appropriate constant."""
        return self._hass.data[DOMAIN][self._config_id].get('state', STATE_OFF)

    @property
    def source(self):
        """Return the current input source."""
        return self._hass.data[DOMAIN][self._config_id].get('source', 'hdmi1')

    async def async_select_source(self, source):
        """Select input source."""
        if source == 'cast':
            await self._hass.async_create_task(
                self._async_start_app(
                    'com.xiaomi.mitv.smartshare'
                )
            )
        else:
            self._tv.change_source(source)
        self._hass.data[DOMAIN][self._config_id].update({'source': source})

    @property
    def assumed_state(self):
        """Indicate that state is assumed."""
        return True

    async def async_play_media(
        self, media_type: MediaType | str, media_id: str, **kwargs: Any
    ) -> None:
        """Play media on the TV."""
        pass

    def turn_off(self):
        """
        Instruct the TV to turn sleep.

        This is done instead of turning off,
        because the TV won't accept any input when turned off. Thus, the user
        would be unable to turn the TV back on, unless it's done manually.
        """
        if self.state != STATE_OFF:
            self._tv.sleep()

            self._hass.data[DOMAIN][self._config_id].update({
                'state': STATE_OFF})

    def turn_on(self):
        """Wake the TV back up from sleep."""
        if self.state != STATE_ON:
            self._tv.wake()

            self._hass.data[DOMAIN][self._config_id].update({
                'state': STATE_ON})

    async def async_update(self):
        """Update the TV state and volume."""
        tv_url = 'http://{}:6095/controller?action=getVolume'.format(
            self._tv.ip_address)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(tv_url) as resp:
                    response = await resp.json(content_type='text/json')
                    self._volume = response['data']['volume']
                    self._max_volume = response['data']['maxVolume']
        except aiohttp.ClientError as error:
            _LOGGER.warning(error)

    async def _async_start_app(self, package: str) -> None:
        """Start an app on the TV."""
        tv_url = (
            f'http://{self._tv.ip_address}:6095/controller'
            f'?action=startapp&type=packagename&packagename={package}'
        )
        try:
            async with aiohttp.ClientSession() as session:
                await session.get(tv_url)
        except aiohttp.ClientError as error:
            _LOGGER.warning(error)

    @property
    def volume_level(self) -> float | None:
        """Return the current volume level."""
        return self._volume / self._max_volume

    async def async_set_volume_level(self, volume: float) -> None:
        """Set the volume level."""
        diff = volume - self._volume / self._max_volume
        steps = round(diff * self._max_volume)
        if steps > 0:
            for _ in range(steps):
                await self._hass.async_add_executor_job(self._tv.volume_up)
        else:
            for _ in range(-1 * steps):
                await self._hass.async_add_executor_job(self._tv.volume_down)

    async def async_volume_up(self):
        """Increase volume by one."""
        await self._hass.async_add_executor_job(self._tv.volume_up)

    async def async_volume_down(self):
        """Decrease volume by one."""
        await self._hass.async_add_executor_job(self._tv.volume_down)

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        self._tv.mute()

    @property
    def device_info(self):
        """Shared entity info information"""
        return {
            'identifiers': {
                (DOMAIN, self._ip),
                ('hacs', 'home_assistant_xiaomi_tv'),
                ('device_tracker', 'mitv4s')
            },
            'name': self._name,
            'manufacturer': 'xiaomi'
        }
