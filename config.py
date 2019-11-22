import yaml


class Config(object):
    _profile = None
    benchmark = None
    controller = None

    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            self._config = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.set_profile()
        self._set_benchmark()
        self._set_controller()

    @property
    def time_steps(self):
        return self._get_property('time_steps')

    @property
    def profile(self):
        return self._profile

    @property
    def servers(self):
        return self._get_property('servers')

    @property
    def log_path(self):
        return self._get_property('log_path')

    @property
    def error_path(self):
        return self._get_property('error_path')

    @property
    def connection_retry(self):
        return self._get_property('connection_retry')

    @property
    def thread_life_limit(self):
        return self._get_property('thread_life_limit')

    def _set_benchmark(self):
        benchmark = self._get_property('benchmark')
        self.benchmark = Benchmark(benchmark)

    def _set_controller(self):
        controller = self._get_property('controller')
        self.controller = Controller(controller)

    def set_profile(self):
        profile_path = self._get_property('profile_path')
        f = open(profile_path, "r")
        profile = f.read()
        p_list = map(int, profile.split(','))
        self._profile = list(p_list)

    def _get_property(self, property_name):
        if property_name not in self._config.keys():  # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]


class Benchmark(object):
    def __init__(self, values):
        self.threads = values['threads']
        self.clients = values['clients']
        self.data_volume = values['data_volume']
        self.ratio = values['ratio']
        self.port = values['port']
        self.expiry_range = values['expiry_range']


class Controller(object):
    def __init__(self, values):
        self.thread_life_limit = values['thread_life_limit']
        self.control_frequency = values['control_frequency']
        self.execute_frequency = values['execute_frequency']
        self.stop_tolerance = values['stop_tolerance']
        self.early_finish_tolerance = values['early_finish_tolerance']
