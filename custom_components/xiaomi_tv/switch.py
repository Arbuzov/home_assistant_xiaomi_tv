import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant,
                            entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback):
    ip = entry.as_dict().get('data').get(CONF_HOST)
    name = entry.as_dict().get('data').get(CONF_NAME)
    async_add_entities([XiaomiTVStatusSwitch(ip, name, hass)])
    return True


class XiaomiTVStatusSwitch(ToggleEntity):

    _attr_name = 'Reset status'
    _attr_icon = 'mdi:television'

    def __init__(self, ip: str, name: str, hass: HomeAssistant):
        self._ip = ip
        self._name = name
        self._config_id = f'{DOMAIN}_{self._ip}'
        self._attr_unique_id = f'{self._config_id}_{self.__class__.__name__}'
        self._hass = hass

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        self._hass.data[DOMAIN][self._config_id].update({'state': STATE_ON})

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        self._hass.data[DOMAIN][self._config_id].update({'state': STATE_OFF})

    @property
    def is_on(self):
        return \
            self._hass.data[DOMAIN][self._config_id].get('state') is STATE_ON

    @property
    def device_info(self):
        """Shared entity info information"""
        return {
            'identifiers': {
                (DOMAIN, self._ip),
                ('hacs', 'home_assistant_xiaomi_tv')
            },
            'name': self._name,
            'manufacturer': 'xiaomi'
        }
