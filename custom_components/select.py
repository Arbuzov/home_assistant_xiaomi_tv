import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import SelectEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    ip = entry.as_dict().get('data').get(CONF_HOST)
    name = entry.as_dict().get('data').get(CONF_NAME)
    async_add_entities([XiaomiTVInputSelect(ip, name, hass)])
    return True


class XiaomiTVInputSelect(SelectEntity):

    _attr_name = 'Select input'
    _attr_icon = 'mdi:television'
    _attr_options = ['hdmi1', 'hdmi2']

    def __init__(self, ip: str, name: str, hass: HomeAssistant):
        self._ip = ip
        self._name = name
        self._config_id = f'{DOMAIN}_{self._ip}'
        self._attr_unique_id = f'{self._config_id}_{self.__class__.__name__}'
        self._hass = hass

    async def async_select_option(self, option: str) -> None:
        """Change the input option."""
        pass

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
