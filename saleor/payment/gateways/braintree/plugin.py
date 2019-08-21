from typing import TYPE_CHECKING, List

from django.utils.translation import pgettext_lazy

from saleor.extensions import ConfigurationTypeField
from saleor.extensions.base_plugin import BasePlugin

from . import authorize, capture, list_client_sources, process_payment, refund, void

if TYPE_CHECKING:
    from . import GatewayResponse, PaymentData, GatewayConfig, CustomerSource


class BraintreeGatewayPlugin(BasePlugin):
    PLUGIN_NAME = "Braintree Gateway"
    CONFIG_STRUCTURE = {
        "Public API key": {
            "type": ConfigurationTypeField.STRING,
            "help_text": pgettext_lazy(
                "Plugin help text", "Provide Braintree public API key"
            ),
            "label": pgettext_lazy("Plugin label", "Public API key"),
        },
        "Secret API key": {
            "type": ConfigurationTypeField.STRING,
            "help_text": pgettext_lazy(
                "Plugin help text", "Provide Braintree secret API key"
            ),
            "label": pgettext_lazy("Plugin label", "Secret API key"),
        },
        "Merchant ID": {
            "type": ConfigurationTypeField.STRING,
            "help_text": pgettext_lazy(
                "Plugin help text", "Provide Braintree merchant ID"
            ),
            "label": pgettext_lazy("Plugin label", "Merchant ID"),
        },
        "Use sandbox": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": pgettext_lazy(
                "Plugin help text",
                "Determines if Saleor should use Braintree sandbox API.",
            ),
            "label": pgettext_lazy("Plugin label", "Use sandbox"),
        },
        "Store customers card": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": pgettext_lazy(
                "Plugin help text",
                "Determines if Saleor should store cards on payments in Braintree customer.",
            ),
            "label": pgettext_lazy("Plugin label", "Store customers card"),
        },
        "Automatic payment capture": {
            "type": ConfigurationTypeField.BOOLEAN,
            "help_text": pgettext_lazy(
                "Plugin help text",
                "Determines if Saleor should automaticaly capture payments.",
            ),
            "label": pgettext_lazy("Plugin label", "Automatic payment capture"),
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = None

    @classmethod
    def _get_default_configuration(cls):
        defaults = None
        return defaults

    def _get_gateway_config(self):
        return GatewayConfig()

    def authorize_payment(
        self, payment_information: PaymentData, previous_value
    ) -> GatewayResponse:
        return authorize(payment_information, self._get_gateway_config())

    def capture_payment(
        self, payment_information: PaymentData, previous_value
    ) -> GatewayResponse:
        return capture(payment_information, self._get_gateway_config())

    def refund_payment(
        self, payment_information: PaymentData, previous_value
    ) -> GatewayResponse:
        return refund(payment_information, self._get_gateway_config())

    def void_payment(
        self, payment_information: PaymentData, previous_value
    ) -> GatewayResponse:
        return void(payment_information, self._get_gateway_config())

    def process_payment(
        self, payment_information: PaymentData, previous_value
    ) -> GatewayResponse:
        return process_payment(payment_information, self._get_gateway_config())

    def list_payment_sources(
        self, customer_id: str, previous_value
    ) -> List[CustomerSource]:
        sources = list_client_sources(self._get_gateway_config(), customer_id)
        previous_value.extend(sources)
        return previous_value