from tools import dataset


class Observable:
    def __init__(self):
        self._observers = {}

    def add_observer(self, attribute, callback):
        if attribute not in self._observers:
            self._observers[attribute] = []
        self._observers[attribute].append(callback)

    def remove_observer(self, attribute, callback):
        if attribute in self._observers:
            self._observers[attribute].remove(callback)

    def _notify_observers(self, attribute, value):
        if attribute in self._observers:
            for callback in self._observers[attribute]:
                callback(attribute, value)


class PetModel(Observable):
    def __init__(self):
        super().__init__()
        self.__load_Pet_infos__()

    def __load_Pet_infos__(self):
        self._infos = dataset.load_from_json('./configs/infos.json')
        self._play = dataset.load_from_json('./configs/play.json')
        self._launch = dataset.load_from_json('./configs/launch.json')
        self._config = dataset.load_from_json('./configs/config.json')

    def get_attributes(self, name):
        return self.infos.get(name, None)

    def set_attributes(self, name, value):
        if name in self.infos:
            self.infos[name] = value
            self._notify_observers(name, value)
        else:
            raise KeyError(f"{name} is not a valid attribute")

    def save_Pet_infos(self):
        try:
            dataset.save_Pet_info('./configs/infos.json', self.infos)
        except FileNotFoundError:
            dataset.save_Pet_info('infos.json', self.infos)

    def update_config(self):
        try:
            dataset.save_Pet_info('./configs/config.json', self._config)
        except FileNotFoundError:
            dataset.save_Pet_info('config.json', self._config)

    def over_time(self):
        self.infos["mood"] = max(self.infos["mood"] - 1, 0)
        self.infos["hunger"] = max(self.infos["hunger"] - 1, 0)
        self.save_Pet_infos()

    @property
    def infos(self):
        return self._infos

    @property
    def play(self):
        return self._play

    @property
    def launch(self):
        return self._launch

    @property
    def config(self):
        return self._config

