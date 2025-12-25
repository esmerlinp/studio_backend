import os
from .payment_providers import StripeProvider

def get_current_provider():
    provider_name = os.getenv('PAYMENT_PROVIDER', 'STRIPE').upper()
    
    providers = {
        'STRIPE': StripeProvider(),
        # 'AZUL': AzulService()
    }
    
    return providers.get(provider_name, StripeProvider())