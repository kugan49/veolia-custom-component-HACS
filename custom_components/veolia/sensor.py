"""Sensor platform for Veolia."""

import logging

from .const import COORDINATOR, DAILY, DOMAIN, HISTORY, MONTHLY
from .debug import decoratorexceptionDebug
from .entity import VeoliaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][COORDINATOR]
    sensors = [
        VeoliaDailyUsageSensor(coordinator, entry),
        VeoliaMonthlyUsageSensor(coordinator, entry),
    ]
    async_add_devices(sensors)


class VeoliaDailyUsageSensor(VeoliaEntity):
    """Monitors the daily water usage."""

    _attr_name = "veolia_daily_consumption"

    @property
    @decoratorexceptionDebug
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data[DAILY]}")
        state = self.coordinator.data[DAILY]["historyConsumption"][0][1]

        if state > 0:
            return state

        return None

    @property
    @decoratorexceptionDebug
    def extra_state_attributes(self):
        """Return the state attributes."""
        _LOGGER.debug(f"Daily : self.coordinator.data = {self.coordinator.data[DAILY]}")
        attrs = {
            "last_report": self.coordinator.data[DAILY]["historyConsumption"][0][0],
            "historyConsumption": self.coordinator.data[DAILY]["historyConsumption"],
        }
        return attrs


class VeoliaMonthlyUsageSensor(VeoliaEntity):
    """Monitors the monthly water usage."""

    _attr_name = "veolia_monthly_consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data[MONTHLY]}")
        state = self.coordinator.data[MONTHLY]["historyConsumption"][0][1]

        if state > 0:
            return state

        return None

    @property
    @decoratorexceptionDebug
    def extra_state_attributes(self):
        """Return the state attributes."""
        _LOGGER.debug(f"Monthly : self.coordinator.data = {self.coordinator.data[MONTHLY]}")
        attrs = {
            "last_report": self.coordinator.data[DAILY]["historyConsumption"][0][0],
            "historyConsumption": self.coordinator.data[MONTHLY]["historyConsumption"],
        }
        return attrs
