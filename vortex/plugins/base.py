import abc
class BasePlugin(abc.ABC):
    @abc.abstractmethod
    def run(self, args): pass
