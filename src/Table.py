import numpy as np
from scipy.ndimage.interpolation import rotate

"""
Map: made of MapPiece
"""
class Map():

    def __init__(self, number_of_players=4):

        self.n_players = number_of_players
        self.map = np.empty((self.n_players, self.n_players), dtype=object)

    def set_player(self, player_id, rotation, row, column):
        self.map[row, column] = MapPiece(mapPiece_type=player_id, rotation=rotation)

    def set_random_mapPiece(self, row, column):
        self.map[row, column] = MapPiece(mapPiece_type='random')


    ### Not needed
    def __str__(self):
        # return str(self.map)
        string = ''
        for row in range(self.map.shape[0]):
            for j in range(4):
                for col in range(self.map.shape[1]):
                    for i in range(4):
                        string='{} {}'.format(string, str(self.map[row, col].mapPiece[j, i]))
                        if i == 3:
                            string = string + '  '
                    if col == self.map.shape[1]-1:
                        string = string+'\n'
                if j == 3:
                    string = string+'\n'

        return string

"""
4x4 Cell block
"""
class MapPiece():

    def __init__(self, mapPiece_type='random', rotation=0):
        self.char_mapPiece_dict = self.getCharMapPieceDict()

        if mapPiece_type != 'random':
            self.mapPiece = self.retrieve_player_mapPiece(player_id=mapPiece_type, rotation=rotation)
            self.discovered = True

        else:
            self.mapPiece = self.retrieve_random_mapPiece()


    def retrieve_player_mapPiece(self, player_id, rotation):
        self.discovered = True
        matrix = rotate(self.char_mapPiece_dict[player_id], angle=rotation)
        mapPiece = np.empty(matrix.shape, dtype=object)
        for r in range(matrix.shape[0]):
            for c in range(matrix.shape[1]):
                mapPiece[r, c] = Cell(base_type=matrix[r, c], show=self.discovered)
        return mapPiece

    def retrieve_random_mapPiece(self):
        self.discovered = False
        matrix = np.random.randint(0, 5, (4, 4))
        mapPiece = np.empty(matrix.shape, dtype=object)
        for r in range(matrix.shape[0]):
            for c in range(matrix.shape[1]):
                mapPiece[r, c] = Cell(base_type=matrix[r, c], show=self.discovered)
        return mapPiece

    def discover_cell(self, rotation):
        self.discovered = True
        self.mapPiece = rotate(self.mapPiece, angle=rotation)

    def getCharMapPieceDict(self):
        return {'arabs': np.array([[0, 0, 0, 0],
                                      [1, 1, 1, 1],
                                      [2, 2, 3, 3],
                                      [0, 0, 0, 1]]),
                'romans': np.array([[0, 0, 0, 0],
                                     [1, 4, 1, 1],
                                     [2, 4, 4, 3],
                                     [0, 0, 0, 1]]),
                'chinese': np.array([[3, 3, 3, 0],
                                     [1, 1, 1, 1],
                                     [2, 2, 3, 3],
                                     [0, 0, 0, 1]]),
                'greeks': np.array([[3, 3, 3, 4],
                                     [1, 4, 1, 1],
                                     [2, 2, 4, 3],
                                     [4, 4, 0, 1]]),
                }


"""
Cell class
"""
class Cell():

    def __init__(self, base_type, show, resource=None, wonder=None):
        self.cell_number_to_type = self.getCellNumber2Type() #Not needed
        self.cell = base_type
        self.resource = resource
        self.wonder =  wonder
        self.show = show
        self.units = []

    """
    Not needed
    """
    def __str__(self):
        if self.show:
            if not self.resource and len(self.units) == 0:
                return str(self.cell_number_to_type[self.cell]+'   ')
            if self.resource and len(self.units) == 0:
                return str(self.cell_number_to_type[self.cell]+'  '+self.resource)
        return str(-1)

    def set_building(self, building_id):
        self.cell = building_id
        self.resource = None

    def set_city(self, player_id, is_capitol):
        if is_capitol:
            self.cell = player_id*100
        else:
            self.cell = player_id*100+1
        self.resources = None

    def set_units(self, player_id, type):
        self.units.append([player_id, type])

    #Not needed
    def getCellNumber2Type(self):
        return {0: 'W', 1: 'M', 2: 'F', 3: 'D', 4: 'P'}
