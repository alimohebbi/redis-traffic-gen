import yaml

pass


class Config(object):
    _profile = None

    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            self._config = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.set_profile()

    def set_profile(self):
        profile_path = self.get_property('profile_path')
        f = open(profile_path, "r")
        profile = f.read()
        p_list = map(int, profile.split(','))
        self._profile = list(p_list)

    def get_property(self, property_name):
        if property_name not in self._config.keys():  # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]

    @property
    def thread_count(self):
        return self.get_property('thread_count')

    @property
    def clients(self):
        return self.get_property('clients_per_thread')

    @property
    def time_steps(self):
        return self.get_property('time_steps')

    @property
    def profile(self):
        return self._profile
