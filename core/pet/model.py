from tools import dataset


class PetModel:
    def __init__(self):
        try:
            infos = dataset.load_Pet_info('./configs/infos.json')
        except FileNotFoundError:
            infos = dataset.load_Pet_info('infos.json')
        self.__dict__.update(infos)

    def save_Pet_infos(self):
        try:
            dataset.save_Pet_info('./configs/infos.json', self.__dict__)
        except FileNotFoundError:
            dataset.save_Pet_info('infos.json', self.__dict__)

    def over_time(self):
        self.mood = max(self.mood - 1, 0)
        self.hunger = max(self.hunger - 1, 0)
        # print('pet.mood:', self.mood, 'pet.hunger:', self.hunger)
        self.save_Pet_infos()

