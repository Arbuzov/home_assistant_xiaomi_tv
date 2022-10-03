import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant,
                            entry: ConfigEntry,
                            async_add_entities: AddEntitiesCallback):
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
        ent_reg = er.async_get(self._hass)
        entity_id = ent_reg.async_get_entity_id(
            Platform.MEDIA_PLAYER,
            DOMAIN,
            f'{self._config_id}_XiaomiTV'
        )
        await self._hass.services.async_call(
            'media_player',
            'select_source',
            service_data={
                'source': option,
                'entity_id': entity_id
            },
            target={
                'entity_id': entity_id
            }
        )
        self._hass.data[DOMAIN][self._config_id].update({'source': option})

    @property
    def current_option(self):
        self._hass.data[DOMAIN][self._config_id].get(
            'source', self._attr_options[0])

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
