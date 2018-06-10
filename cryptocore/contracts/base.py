class BaseContract(object):
    def validate(self, value):
        raise NotImplementedError()