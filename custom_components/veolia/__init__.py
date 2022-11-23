"""
Custom integration to integrate Veolia with Home Assistant.
"""
import asyncio
import logging
import time
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from VeoliaClient import VeoliaClient

from .const import API, CONF_PASSWORD, CONF_USERNAME, COORDINATOR, DAILY, DOMAIN, LAST_REPORT_TIMESTAMP, PLATFORMS

SCAN_INTERVAL = timedelta(minutes=30)


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    session = aiohttp_client.async_create_clientsession(hass)
    hass.data[DOMAIN][API] = VeoliaClient(username, password, session)

    async def _get_consumption():
        """Return the water consumption."""
        api = hass.data[DOMAIN][API]
        last_report_date = api.last_report_date
        last_report_timestamp = time.mktime(
            datetime(last_report_date.year, last_report_date.month, last_report_date.day).timetuple()
        )

        previous_data = hass.data[DOMAIN][COORDINATOR].data
        if (
            previous_data
            and previous_data[LAST_REPORT_TIMESTAMP] == last_report_timestamp
            and 0 < previous_data[DAILY][-1] < 10000
        ):
            return previous_data

        daily_consumption = await api.update()

        return {
            DAILY: daily_consumption,
            LAST_REPORT_TIMESTAMP: last_report_timestamp,
        }

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="veolia consumption update",
        update_method=_get_consumption,
        update_interval=SCAN_INTERVAL,
    )

    hass.data[DOMAIN][COORDINATOR] = coordinator

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    for platform in PLATFORMS:
        hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, platform))

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(API, None)
    await asyncio.gather(*(hass.config_entries.async_forward_entry_unload(entry, component) for component in PLATFORMS))
    return True
