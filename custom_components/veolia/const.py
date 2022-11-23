"""Constants for Veolia."""

from homeassistant.components.sensor import DOMAIN as SENSOR

NAME = "Veolia"
DOMAIN = "veolia"
PLATFORMS = [SENSOR]
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
API = "api"
COORDINATOR = "coordinator"

FORMAT_DATE = "%Y-%m-%dT%H:%M:%S%z"
