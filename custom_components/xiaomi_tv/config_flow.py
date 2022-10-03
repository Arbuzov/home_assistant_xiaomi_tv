"""Config flow for the smart curtain integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_HOST
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = voluptuous.Schema(
    {
        voluptuous.Required(CONF_NAME): str,
        voluptuous.Required(CONF_HOST): str
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Xiaomi TV"""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id='user', data_schema=STEP_USER_DATA_SCHEMA
            )
        else:
            await self.async_set_unique_id(f'{DOMAIN}_{user_input[CONF_HOST]}')
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input)
