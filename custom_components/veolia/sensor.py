"""Sensor platform for Veolia."""

import logging

from homeassistant.components.sensor import SensorStateClass

from .const import DAILY, DOMAIN, HISTORY, MONTHLY
from .debug import decoratorexceptionDebug
from .entity import VeoliaEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        VeoliaDailyUsageSensor(coordinator, entry),
        VeoliaMonthlyUsageSensor(coordinator, entry),
        VeoliaLastIndexSensor(coordinator, entry),
    ]
    async_add_devices(sensors)


class VeoliaLastIndexSensor(VeoliaEntity):
    """Monitors the last index."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return "veolia_last_index"

    @property
    def state_class(self):
        """Return the state_class of the sensor."""
        _LOGGER.debug(f"state_class = {SensorStateClass.TOTAL_INCREASING}")
        return SensorStateClass.TOTAL_INCREASING

    @property
    @decoratorexceptionDebug
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data['last_index']}")
        state = self.coordinator.data["last_index"]
        if state > 0:
            return state
        return None

    @property
    @decoratorexceptionDebug
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        return self._base_extra_state_attributes()


class VeoliaDailyUsageSensor(VeoliaEntity):
    """Monitors the daily water usage."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return "veolia_daily_consumption"

    @property
    @decoratorexceptionDebug
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data[DAILY]}")
        state = self.coordinator.data[DAILY][HISTORY][0][1]
        if state > 0:
            return state
        return None

    @property
    @decoratorexceptionDebug
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        _LOGGER.debug(f"Daily : self.coordinator.data = {self.coordinator.data[DAILY]}")
        attrs = self._base_extra_state_attributes() | {
            "historyConsumption": self.coordinator.data[DAILY][HISTORY],
        }
        return attrs


class VeoliaMonthlyUsageSensor(VeoliaEntity):
    """Monitors the monthly water usage."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return "veolia_monthly_consumption"

    @property
    def state(self):
        """Return the state of the sensor."""
        _LOGGER.debug(f"self.coordinator.data = {self.coordinator.data[MONTHLY]}")
        state = self.coordinator.data[MONTHLY][HISTORY][0][1]
        if state > 0:
            return state
        return None

    @property
    @decoratorexceptionDebug
    def extra_state_attributes(self):
        """Return the extra state attributes."""
        _LOGGER.debug(f"Monthly : self.coordinator.data = {self.coordinator.data[MONTHLY]}")
        attrs = self._base_extra_state_attributes() | {
            "historyConsumption": self.coordinator.data[MONTHLY][HISTORY],
        }
        return attrs
