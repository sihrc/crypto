class CryptoError(Exception):
    """
    Base error for Crypto
    """
    pass

class NotPopulatedYet(CryptoError):
    pass

class ContractError(CryptoError):
    pass
