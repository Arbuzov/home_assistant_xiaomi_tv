"""The xiaomi_tv component."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .proxy import MyProxyView

PLATFORMS: list[str] = [
    Platform.MEDIA_PLAYER,
    Platform.SWITCH
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up oiot from a config entry."""
    # Исправлено: используем импортированный async_get_clientsession
    websession = async_get_clientsession(hass)
    hass.http.register_view(MyProxyView(websession))
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    if entry.unique_id not in hass.data[DOMAIN]:
        hass.data[DOMAIN][entry.unique_id] = {}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    try:
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, PLATFORMS)
    except ValueError as error:
        if str(error) == 'Config entry was never loaded!':
            unload_ok = True
    if unload_ok:
        hass.data[DOMAIN].pop(entry.unique_id)
    return unload_ok
