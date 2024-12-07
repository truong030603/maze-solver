import pygame
pygame.init()

##### Screen Settings #####
WIDTH = 1536
HEIGHT = 768

GRID_WIDTH = WIDTH - 240 - 24*2
GRID_HEIGHT = HEIGHT - 24*2

#####  Button Settings #####
MAIN_BUTTON_Y_POS_1 = 550
MAIN_BUTTON_Y_POS_2 = 640

# Dimensions of Main-Menu Buttons
MAIN_BUTTON_LENGTH = 200
MAIN_BUTTON_HEIGHT = 70

# Dimensions/Settings of Grid-Menu Buttons
START_END_BUTTON_HEIGHT = 335
BUTTON_SPACER = 20
GRID_BUTTON_LENGTH = 200
GRID_BUTTON_HEIGHT = 20
GRID_BUTTON_HEIGHT2 = 30


##### Colour Settings #####
WHITE = (255,255,255)
AQUAMARINE = (127,255,212)
BLACK = (0,0,0)
ALICE = (240,248,255)
STEELBLUE = (110,123,139)
MINT = (189,252,201)
SPRINGGREEN = (0,255,127)
TOMATO = (255,99,71)
ROYALBLUE = (72,118,255)
TAN = (255,165,79)
RED = (255,0,0)
VIOLETRED = (255,130,171)
TURQUOISE = (30,144,255)
GREEN = (0,128,0)


##### Grid Settings #####
# GS MEANS Grid-Start
GS_X = 264
GS_Y = 24
# GE MEANS Grid-End
GE_X = 1512
GE_Y = 744

##### Font Settings #####
FONT = 'Arial Black'

##### Coordinates of border #####
# wall_nodes_coords_list = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0),
#                           (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0),
#                           (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0), (30, 0),
#                           (31, 0), (32, 0), (33, 0), (34, 0), (35, 0), (36, 0), (37, 0), (38, 0), (39, 0), (40, 0),
#                           (41, 0), (42, 0), (43, 0), (44, 0), (45, 0), (46, 0), (47, 0), (48, 0), (49, 0), (50, 0),
#                           (51, 0), (52, 0), (53, 0), (0, 1), (53, 1), (0, 2), (53, 2), (0, 3), (53, 3), (0, 4), (53, 4),
#                           (0, 5), (53, 5), (0, 6), (53, 6), (0, 7), (53, 7), (0, 8), (53, 8), (0, 9), (53, 9), (0, 10),
#                           (53, 10), (0, 11), (53, 11), (0, 12), (53, 12), (0, 13), (53, 13), (0, 14), (53, 14), (0, 15),
#                           (53, 15), (0, 16), (53, 16), (0, 17), (53, 17), (0, 18), (53, 18), (0, 19), (53, 19), (0, 20),
#                           (53, 20), (0, 21), (53, 21), (0, 22), (53, 22), (0, 23), (53, 23), (0, 24), (53, 24), (0, 25),
#                           (53, 25), (0, 26), (53, 26), (0, 27), (53, 27), (0, 28), (53, 28), (0, 29), (53, 29), (0, 30),
#                           (53, 30), (0, 31), (1, 31), (2, 31), (3, 31), (4, 31), (5, 31), (6, 31), (7, 31), (8, 31),
#                           (9, 31), (10, 31), (11, 31), (12, 31), (13, 31), (14, 31), (15, 31), (16, 31), (17, 31),
#                           (18, 31), (19, 31), (20, 31), (21, 31), (22, 31), (23, 31), (24, 31), (25, 31), (26, 31),
#                           (27, 31), (28, 31), (29, 31), (30, 31), (31, 31), (32, 31), (33, 31), (34, 31), (35, 31),
#                           (36, 31), (37, 31), (38, 31), (39, 31), (40, 31), (41, 31), (42, 31), (43, 31), (44, 31),
#                           (45, 31), (46, 31), (47, 31), (48, 31), (49, 31), (50, 31), (51, 31), (52, 31), (53, 31)]

def create_maze(width, height):
    wall_nodes_coords_list = []

    for x in range(width):
        wall_nodes_coords_list.append((x, 0))
        wall_nodes_coords_list.append((x, height - 1))

    for y in range(height):
        wall_nodes_coords_list.append((0, y))
        wall_nodes_coords_list.append((width - 1, y))

    return wall_nodes_coords_list

# Chiều rộng và chiều cao của mê cung
custom_width = 54
custom_height = 32

# Tạo mê cung dựa trên kích thước mới
wall_nodes_coords_list = create_maze(custom_width, custom_height)