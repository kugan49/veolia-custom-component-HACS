"""Sensor platform for Veolia."""

import logging

from .const import COORDINATOR, DOMAIN
from .entity import VeoliaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    sensors = [
        VeoliaDailyUsageSensor(coordinator, entry),
    ]
    async_add_devices(sensors)


class VeoliaDailyUsageSensor(VeoliaEntity):
    """Monitors the daily water usage."""

    _attr_name = "veolia_daily_consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data}")
        state = self.coordinator.data["historyConsumption"][0][1]

        if state > 0:
            return state

        return None
