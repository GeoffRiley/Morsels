from weakref import WeakSet


def instance_tracker(inst_name: str = 'instances'):
    class MixinTracker():
        _instances = WeakSet()

        def __new__(cls, *args, **kwargs):
            instance = super().__new__(cls)
            cls._instances.add(instance)
            return instance

    setattr(MixinTracker, inst_name, MixinTracker._instances)
    return MixinTracker
