#from src.Cities import City

def Civilization2PlayerID():
    return {'romans': 1, 'arabs': 2, 'greeks': 3, 'chinese': 4}

class City():

    def __init__(self, map, tesseract, where, is_capitol, player_id):
        self.player_id = player_id
        self.map = map
        self.row = tesseract[0]
        self.col = tesseract[1]
        self.is_capitol = is_capitol
        self.map.map[self.row, self.col].mapPiece[where[0], where[1]].set_city(player_id, self.is_capitol)
        self.defense = self.get_defense()

    def get_defense(self):
        if not self.is_capitol:
            return 6
        return 10

class Units():

    def __init__(self, type, map, tesseract, where, player_id):
        self.type = type
        self.map = map 
        self.map.map[tesseract[0], tesseract[1]].mapPiece[where[0], where[1]].set_units(player_id, type)


class Player():

    def __init__(self, civilization, starting_cordinates, rotation):
        self.civilizaton = civilization
        self.id = Civilization2PlayerID()[civilization]
        self.starting_cordinates = starting_cordinates
        self.rotation = rotation

        self.cities = []
        self.resources = []
        self.total_gold = 0
        self.technolgy = []
        self.culture = []
        self.government = None
        self.trade = 0
        self.culture_hand = []
        self.coin = 0
        self.units = []

        self.accumulo = 2
        self.movimento = 2
        self.on_water = False
        self.finish_on_water = False
        self.max_cities = 2

    def found_city(self, map, tesseract, where, is_capitol):
        if len(self.cities) < self.max_cities:
            self.cities.append(City(map, tesseract, where, is_capitol, self.id))

    def create_units(self, type, map, tesseract, where):
        unit = Units(type, map, tesseract, where, self.id)
        self.units.append(unit)


    def harvest_trade(self):
        for city in self.cities:
            self.trade += city.get_trade()
