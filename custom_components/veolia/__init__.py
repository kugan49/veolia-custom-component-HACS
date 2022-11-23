"""
Custom integration to integrate Veolia with Home Assistant.
"""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import API, CONF_PASSWORD, CONF_USERNAME, COORDINATOR, DOMAIN, PLATFORMS
from .debug import decoratorexceptionDebug
from .VeoliaClient import VeoliaClient

SCAN_INTERVAL = timedelta(minutes=30)

_LOGGER = logging.getLogger(__name__)


@decoratorexceptionDebug
async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


@decoratorexceptionDebug
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    session = aiohttp_client.async_create_clientsession(hass)
    hass.data[DOMAIN][API] = VeoliaClient(username, password, session)

    @decoratorexceptionDebug
    async def _get_consumption():
        """Return the water consumption."""
        api = hass.data[DOMAIN][API]
        daily_consumption = await hass.async_add_executor_job(api.update)
        _LOGGER.debug(f"daily_consumption = {daily_consumption}")
        return daily_consumption

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


@decoratorexceptionDebug
async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(API, None)
    await asyncio.gather(*(hass.config_entries.async_forward_entry_unload(entry, component) for component in PLATFORMS))
    return True
