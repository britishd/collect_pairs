def check_params(provider_url: str, protocol: str, factory_address: str, amount: str):
    if not provider_url:
        raise ValueError('Add PROVIDER to env file')
    
    if not protocol:
        raise ValueError('Add PROTOCOL to env file')
    
    if not factory_address:
        raise ValueError('Add FACTORY to env file')
    
    if not amount:
        raise ValueError('Add AMOUNT to env file')
