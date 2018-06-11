from .base import BaseContract
from ..errors import ContractError

class DictContract(BaseContract):
    def __init__(self, required_keys=None, optional_keys=None):
        required_keys = required_keys or []
        optional_keys = optional_keys or []

        self.fields = required_keys + optional_keys
        self.required_keys = set(required_keys)
        self.accepted_keys = set(self.fields)

    def validate(self, value):
        if not isinstance(value, dict):
            raise ContractError("{value} is not {_type} type".format(
                value=value,
                _type=type
            ))

        keys_provided = set(value.keys())
        missing = self.required_keys - keys_provided
        if missing:
            raise ContractError(
                "DictContract missing keys {}".format(missing)
            )

        unaccepted_keys = keys_provided - self.accepted_keys
        if unaccepted_keys:
            raise ContractError(
                "DictContract keys not allowed {}".format(unaccepted_keys)
            )

        return True and super().validate(value)
