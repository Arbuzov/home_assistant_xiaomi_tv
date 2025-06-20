"""The xiaomi_tv component."""

from __future__ import annotations

import fileinput
import logging
import os

import pymitv
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.issue_registry import (IssueSeverity,
                                                  async_create_issue)

from .const import DOMAIN, PYMITV_HACK
from .proxy import MyProxyView

PLATFORMS: list[str] = [
    Platform.MEDIA_PLAYER,
    Platform.SWITCH
]

LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up oiot from a config entry."""
    await hass.async_create_task(hack_pymitv(hass))
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


async def hack_pymitv(hass: HomeAssistant):
    def _hack_pymitv_sync():
        hacked = False
        try:
            pymitv_path = pymitv.__path__[0]
            for hack in PYMITV_HACK:
                with fileinput.input(
                    files=(os.path.join(pymitv_path, hack.get('file'))),
                    inplace=True
                ) as f:
                    line_number = 1
                    for ip_line in f:
                        if (
                            hack.get('from') in ip_line
                            and (
                                hack.get('line') is None
                                or hack.get('line') == line_number
                            )
                        ):
                            hacked = True
                            ip_line = ip_line.replace(
                                hack.get('from'),
                                hack.get('to')
                            )
                            LOGGER.warning(
                                'Hacked file %s line "%s" line %d',
                                hack.get('file'),
                                hack.get('from'), line_number)

                        print(ip_line, end='')
                        line_number = line_number + 1
        except (FileNotFoundError, PermissionError) as err:
            LOGGER.error("Error applying pymitv hack: %s", err)
        except Exception:
            LOGGER.exception("Unexpected error applying pymitv hack")
        return hacked

    hacked = await hass.async_add_executor_job(_hack_pymitv_sync)

    if hacked:
        await hass.services.async_call(
            'persistent_notification',
            'create',
            {
                'message': 'Please reboot HA to apply the changes',
                'title': 'Pymitv was hacked',
                'notification_id': f'{DOMAIN}_event'
            }
        )
        async_create_issue(
            hass=hass,
            domain=DOMAIN,
            issue_id=f"restart_required_{DOMAIN}",
            is_fixable=True,
            issue_domain=DOMAIN,
            severity=IssueSeverity.WARNING,
            translation_key="restart_required"
        )
