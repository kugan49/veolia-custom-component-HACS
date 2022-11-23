# TODO a revoir
"""Sensor platform for Veolia."""
from .const import COORDINATOR, DAILY, DOMAIN
from .entity import VeoliaEntity


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
        state = self.coordinator.data[DAILY][-1]

        if state > 0:
            return state

        return None
