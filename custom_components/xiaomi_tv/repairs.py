"""Repairs flows for the Xiaomi TV integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.components.repairs import RepairsFlow
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult


class RestartRequiredFlow(RepairsFlow):
    """Repair flow to restart Home Assistant."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the first step."""
        return await self.async_step_confirm_restart()

    async def async_step_confirm_restart(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Show a confirmation and restart Home Assistant when accepted."""
        if user_input is not None:
            await self.hass.services.async_call(
                "homeassistant", "restart", blocking=False
            )
            return self.async_create_entry(data={})

        return self.async_show_form(
            step_id="confirm_restart",
            data_schema=vol.Schema({}),
        )


async def async_create_fix_flow(
    hass: HomeAssistant,
    issue_id: str,
    data: dict[str, Any] | None,
) -> RepairsFlow:
    """Create a repair flow for a fixable issue."""
    return RestartRequiredFlow()
