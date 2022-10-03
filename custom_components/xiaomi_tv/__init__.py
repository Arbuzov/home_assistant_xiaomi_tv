"""The xiaomi_tv component."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, STATE_OFF
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PLATFORMS: list[str] = [
    Platform.MEDIA_PLAYER,
    Platform.SWITCH,
    Platform.SELECT
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up oiot from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    hass.data[DOMAIN][entry.unique_id] = {'state': STATE_OFF}
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.unique_id)
    return unload_ok
