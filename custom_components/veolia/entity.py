"""VeoliaEntity class."""

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import UnitOfVolume
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DAILY, DOMAIN, HISTORY, ICON, NAME
from .debug import decoratorexceptionDebug


class VeoliaEntity(CoordinatorEntity, SensorEntity):
    """Representation of a Veolia entity."""

    @decoratorexceptionDebug
    def __init__(self, coordinator, config_entry):
        """Initialize the entity."""
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.name}"
        # return self.config_entry.entry_id

    @property
    @decoratorexceptionDebug
    def device_info(self):
        """Return device registry information for this entity."""
        return {
            "identifiers": {(DOMAIN, self.config_entry.entry_id)},
            "manufacturer": NAME,
            "name": NAME,
        }

    @property
    def device_class(self):
        """Return the device_class of the sensor."""
        return SensorDeviceClass.WATER

    @property
    def unit_of_measurement(self):
        """Return the unit_of_measurement of the sensor."""
        return UnitOfVolume.LITERS

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    def _base_extra_state_attributes(self):
        """Return the base extra state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
            "last_report": self.coordinator.data[DAILY][HISTORY][0][0],
        }
