"""VeoliaEntity class."""
from datetime import datetime

from homeassistant.const import VOLUME_LITERS
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, FORMAT_DATE, NAME
from .debug import decoratorexceptionDebug


class VeoliaEntity(CoordinatorEntity):
    """Representation of a Veolia entity."""

    @decoratorexceptionDebug
    def __init__(self, coordinator, config_entry):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_unique_id = f"{self.config_entry.entry_id}_{self.name}"
        self._attr_unit_of_measurement = VOLUME_LITERS
        self._attr_icon = "mdi:water"

    @property
    @decoratorexceptionDebug
    def device_info(self):
        """Return device registry information for this entity."""
        return {
            "identifiers": {(self.config_entry.entry_id, DOMAIN)},
            "manufacturer": NAME,
            "name": NAME,
        }

    @property
    @decoratorexceptionDebug
    def extra_state_attributes(self):
        """Return the state attributes."""
        historyConsumption = self.coordinator.data["historyConsumption"]
        last_report = datetime.strptime(historyConsumption[0][0], FORMAT_DATE)
        return {"last_report": last_report, "historyConsumption": historyConsumption}
