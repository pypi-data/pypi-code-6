class registry:
    """A memory key/value registry"""

    storage = {}

    @staticmethod
    def set(key, value):
        """Sets a value in the registry"""
        registry.storage[key] = value

    @staticmethod
    def get(key):
        """Gets a value from the registry"""
        if key in registry.storage:
            return registry.storage[key]
        else:
            return None

    @staticmethod
    def test(key):
        """Checks to see if there's a key in the registry"""
        return key in registry.storage

    @staticmethod
    def flush():
        """Removes all values from the registry"""
        registry.storage = {}