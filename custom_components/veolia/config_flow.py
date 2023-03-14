"""Adds config flow for Veolia."""
import logging

from homeassistant import config_entries
import voluptuous as vol

from .VeoliaClient import BadCredentialsException, VeoliaClient
from .const import CONF_ABO_ID, CONF_PASSWORD, CONF_USERNAME, DOMAIN
from .debug import decoratorexceptionDebug

_LOGGER: logging.Logger = logging.getLogger(__package__)


class VeoliaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for veolia."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    @decoratorexceptionDebug
    def __init__(self):
        """Initialize."""
        self._errors = {}

    @decoratorexceptionDebug
    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            valid = await self._test_credentials(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if valid:
                if user_input[CONF_ABO_ID] != "":
                    title = f"{user_input[CONF_USERNAME]} - {user_input[CONF_ABO_ID]}"
                else:
                    title = f"{user_input[CONF_USERNAME]}"
                return self.async_create_entry(title=title, data=user_input)
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        user_input = {}
        # Provide defaults for form
        user_input[CONF_USERNAME] = ""
        user_input[CONF_PASSWORD] = ""
        user_input[CONF_ABO_ID] = ""

        return await self._show_config_form(user_input)

    @decoratorexceptionDebug
    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                    vol.Optional(CONF_ABO_ID, default=user_input[CONF_ABO_ID]): str,
                }
            ),
            errors=self._errors,
        )

    @decoratorexceptionDebug
    async def _test_credentials(self, username, password):
        """Return true if credentials is valid."""
        try:
            client = VeoliaClient(username, password)
            await self.hass.async_add_executor_job(client.login)
            return True
        except BadCredentialsException:
            pass
        return False
