import src.Table as Table
import src.Player as pl
import numpy as np
import pygame
import time

def plain_load_icons(player_number, resolution):
        size = get_cell_size(player_number, resolution)
        water_icon    = pygame.transform.scale(pygame.image.load('imgs/water.png'), size)
        mountain_icon = pygame.transform.scale(pygame.image.load('imgs/mountain.png'), size)
        desert_icon   = pygame.transform.scale(pygame.image.load('imgs/desert.jpg'), size)
        forest_icon   = pygame.transform.scale(pygame.image.load('imgs/tree.png'), size)
        plain_icon    = pygame.transform.scale(pygame.image.load('imgs/tree.png'), size)
        undiscover_icon = pygame.transform.scale(pygame.image.load('imgs/undiscovered.png'), size)
        player1_cap = pygame.transform.scale(pygame.image.load('imgs/base_capitol1.jpg'), size)
        player1_city = pygame.transform.scale(pygame.image.load('imgs/base_city1.jpg'), size)
        player2_cap = pygame.transform.scale(pygame.image.load('imgs/base_capitol2.jpg'), size)
        player2_city = pygame.transform.scale(pygame.image.load('imgs/base_city2.jpg'), size)
        player3_cap = pygame.transform.scale(pygame.image.load('imgs/base_capitol3.jpg'), size)
        player3_city = pygame.transform.scale(pygame.image.load('imgs/base_city3.jpg'), size)
        player4_cap = pygame.transform.scale(pygame.image.load('imgs/base_capitol4.jpg'), size)
        player4_city = pygame.transform.scale(pygame.image.load('imgs/base_city4.jpg'), size)


        return {'undiscover_icon': undiscover_icon,
                'water_icon': water_icon,
                'desert_icon': desert_icon,
                'mountain_icon': mountain_icon,
                'forest_icon': forest_icon,
                'plain_icon': plain_icon,
                'player1_cap': player1_cap,
                'player1_city': player1_city,
                'player2_cap': player2_cap,
                'player2_city': player2_city,
                'player3_cap': player3_cap,
                'player3_city': player3_city,
                'player4_cap': player4_cap,
                'player4_city': player4_city,}



def get_cell_size(player_number, resolution):
    cell_number = 4*player_number
    return (resolution[0]//cell_number, resolution[1]//cell_number)

def display_map(screen, map, icon_dict, player_number, resolution):
    value_to_icon = {-1: 'undiscover_icon', 0: 'water_icon', 3: 'desert_icon',
                     1: 'mountain_icon', 2: 'forest_icon', 4: 'plain_icon',
                     100: 'player1_cap', 101: 'player1_city', 102: 'p1_settler_icon', 103: 'p1_explorer_icon',
                     200: 'player2_cap', 201: 'player2_city', 202: 'p2_settler_icon', 203: 'p2_explorer_icon',
                     300: 'player3_cap', 301: 'player3_city', 302: 'p3_settler_icon', 303: 'p3_explorer_icon',
                     400: 'player4_cap', 401: 'player4_city', 402: 'p4_settler_icon', 403: 'p4_explorer_icon',
                     }

    values = []
    size = get_cell_size(player_number, resolution)

    ### Retrieve Cell object with wanted sequence
    for row in range(map.map.shape[0]):
        for i in range(4):
            for col in range(map.map.shape[1]):
                for j in range(4):
                    if map.map[row, col].discovered:
                        values.append(map.map[row, col].mapPiece[i, j])
                    else:
                        values.append(-1)

    ### Draw basic Cell
    for n, v in enumerate(values):
        r, c = n//(4*map.map.shape[0]), n%(4*map.map.shape[0])
        where = (c*size[1], r*size[0])
        screen.blit(icon_dict[value_to_icon[v.cell]], where)

        ### Add units if presents TODO
        # if len(v.units) != 0:
        #     screen.blit(###TODO)

        ### Add resources if presents TODO
        # if len(v.resources) != 0:
        #     screen.blit(##TODO)




if __name__ == '__main__':

    ### Vars
    DISPLAY_SIZE = (900, 900)
    N_PLAYERS = 4

    ### Other vars
    position = [(0, 0), (0, 3), (3, 3), (3, 0)]
    player_type = ['romans', 'arabs', 'chinese', 'greeks']
    rotations = [180, 90, 0, 0]

    ### Display
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)

    ### TITLE and ICON
    pygame.display.set_caption('Civilization Table Game')
    icon = pygame.image.load('imgs/logo.jpg')
    pygame.display.set_icon(icon)

    ### GRAPHICS_ICON
    plain_icon_dict = plain_load_icons(player_number=N_PLAYERS, resolution=DISPLAY_SIZE)


    ### MAP
    map = Table.Map(number_of_players=len(player_type))
    for n, player_id in enumerate(player_type):
        map.set_player(player_id=player_id, rotation=rotations[n], row=position[n][0], column=position[n][1])
    for i in range(len(player_type)):
        for j in range(len(player_type)):
            if (i, j) not in position:
                map.set_random_mapPiece(row=i, column=j)

    ### PLAYERS
    players = [pl.Player(player_type[i], starting_cordinates=position[i], rotation=rotations[i]) for i in range(N_PLAYERS)]

    ### DISCOVER EXAMPLE
    map.map[1, 0].discovered = True
    map.map[1, 3].discovered = True
    map.map[2, 0].discovered = True
    map.map[3, 2].discovered = True

    ### Display map
    display_map(screen, map, plain_icon_dict, N_PLAYERS, DISPLAY_SIZE)
    pygame.display.update()

    ### Create background color
    screen.fill((200, 200, 200))
    pygame.display.update()

    ### GAME SESSION
    running = True
    while running:
        time.sleep(1)
        ### CREATE EVENT QUIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        time.sleep(1)

        ### Set CAPITOLS
        for user in players:
            user.found_city(map, user.starting_cordinates, where=(2, 2), is_capitol=True)
            pygame.display.update()

        ### Set UNITS
        for user in players:
            user.create_units('settler', map, tesseract=[0, 0], where=(1, 1))
            user.create_units('explored', map, tesseract=[0, 0], where=(1, 1))
