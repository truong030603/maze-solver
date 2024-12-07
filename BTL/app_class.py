import sys

import pygame

from settings import *
from buttons import *
from bfs_class import *
from dfs_class import *
from ucs_class import *
from astar_class import *
from greedy_class import *
from bidirectional_class import *
from visualize_path_class import *
from ids import *
from maze_class import *
import time

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
        self.grid_square_length = 24 # Kích thước của mỗi ô vuông là 24 x 24
        self.load()
        self.start_end_checker = 0
        self.mouse_drag = 0

        # Tọa độ nút bắt đầu và kết thúc
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None
        self.sobuocduyet = 0
        self.sobuocduongdi = 0
        self.toadoduyet = []
        # Danh sách nút tường (danh sách đã bao gồm tọa độ của các đường viền)
        self.wall_pos = wall_nodes_coords_list.copy()

        # Khởi tạo lớp mê cung
        self.maze = Maze(self, self.wall_pos)

        # Xác định các nút Menu chính

        self.bfs_button = Buttons(self, WHITE, 400, MAIN_BUTTON_Y_POS_1, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Breadth-First Search')
        self.dfs_button = Buttons(self, WHITE, 648, MAIN_BUTTON_Y_POS_1, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Depth-First Search')
        self.ids_button = Buttons(self, WHITE, 620, 450, 250, MAIN_BUTTON_HEIGHT, 'Iterative-Depending Search')
        self.ucs_button = Buttons(self, WHITE, 900, MAIN_BUTTON_Y_POS_1, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Uniform-Cost Search')
        self.astar_button = Buttons(self, WHITE, 400, MAIN_BUTTON_Y_POS_2, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'A-Star Search')
        self.greedy_button = Buttons(self, WHITE, 648, MAIN_BUTTON_Y_POS_2, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Greedy Search')
        self.bidirectional_button = Buttons(self, WHITE, 900, MAIN_BUTTON_Y_POS_2, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Bidirectional Search')

        # Define Grid-Menu buttons
        self.start_end_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT+200, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT2, 'Start/End Node')
        self.wall_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER+200, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT2, 'Wall Node')
        self.reset_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*2 + BUTTON_SPACER*2+200, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT2, 'Reset')
        self.start_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*3 + BUTTON_SPACER*3+200, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT2, 'Visualize Path')
        self.main_menu_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 4 + BUTTON_SPACER * 4+200, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT2, 'Main Menu')
        self.maze_generate_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 5 + BUTTON_SPACER * 5+200, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT2, 'Generate Maze')
        self.reset_path = Buttons(self, AQUAMARINE, 20, 265+230, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT2, 'Reset Path')

        #123
        self.algorithm_dfs = Buttons(self, AQUAMARINE, 20, 20+238, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'DFS')
        self.algorithm_bfs = Buttons(self, AQUAMARINE, 20, 20+30*1+238, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'BFS')
        self.algorithm_ucs = Buttons(self, AQUAMARINE, 20, 20+30*2+238, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'UCS')
        self.algorithm_ids = Buttons(self, AQUAMARINE, 20, 20+30*3+238, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'IDS')
        self.algorithm_astar = Buttons(self, AQUAMARINE, 20, 20+30*4+238, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'A-Star')
        self.algorithm_greedy = Buttons(self, AQUAMARINE, 20, 20+30*5+238, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Greedy')
        self.algorithm_bidirectional = Buttons(self, AQUAMARINE, 20, 20+30*6+238, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Bidirectional')

    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'start visualizing':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main_menu()
            if self.state == 'grid window reset Path':
                self.grid_events_resetPath()
            if self.state == 'grid window selectAlgorithm':
                self.grid_events_selectAlgorithmions()

        pygame.quit()
        sys.exit()

#################################### SETUP FUNCTIONS #########################################

##### Loading Images
    def load(self):
        self.main_menu_background = pygame.image.load('BTL/mecung.jpg')
        DEFAULT_IMAGE_SIZE = (1550, 820)
        self.main_menu_background = pygame.transform.scale(self.main_menu_background, DEFAULT_IMAGE_SIZE)
        DEFAULT_IMAGE_SIZE1 = (230, 230)
        self.grid_background = pygame.image.load('BTL/LOGO (1).jpg')
        self.grid_background = pygame.transform.scale(self.grid_background, DEFAULT_IMAGE_SIZE1)

##### Draw Text
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

##### Setup for Main Menu
    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))
        # Draw Buttons
        self.ucs_button.draw_button(AQUAMARINE)
        self.bfs_button.draw_button(AQUAMARINE)
        self.dfs_button.draw_button(AQUAMARINE)
        self.ids_button.draw_button(AQUAMARINE)
        self.astar_button.draw_button(AQUAMARINE)
        self.greedy_button.draw_button(AQUAMARINE)
        self.bidirectional_button.draw_button(AQUAMARINE)

##### Setup for Grid
    def sketch_hotbar(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)
        self.screen.blit(self.grid_background, (0, 0))

    def sketch_grid(self):
        # Vẽ map
        pygame.draw.rect(self.screen, BLACK, (240, 0, WIDTH, HEIGHT), 0)
        pygame.draw.rect(self.screen, WHITE, (264, 24, GRID_WIDTH, GRID_HEIGHT), 0)

        # Draw grid
        # There are 52 square pixels across on grid [ WITHOUT BORDERS! ]
        # There are 30 square pixels vertically on grid [ WITHOUT BORDERS! ]
        #Vẽ dường viền
        for x in range(52):
            pygame.draw.line(self.screen, BLACK, (GS_X + x*self.grid_square_length, GS_Y),
                             (GS_X + x*self.grid_square_length, GE_Y))
        for y in range(30):
            pygame.draw.line(self.screen, BLACK, (GS_X, GS_Y + y*self.grid_square_length),
                             (GE_X, GS_Y + y*self.grid_square_length))

    def sketch_grid_resetPath(self):
        index = 0
         # Giả sử self.toadoduyet có cấu trúc (x, y)
        self.toadoduyet = [(x, y) for x, y in self.toadoduyet if (x, y) != (self.start_node_x, self.start_node_y)]

        # Làm tương tự cho end_node
        self.toadoduyet = [(x, y) for x, y in self.toadoduyet if (x, y) != (self.end_node_x, self.end_node_y)]


        while index < len(self.toadoduyet):
            toado = self.toadoduyet[index]
            x, y = toado
            if toado not in self.wall_pos:
                pygame.draw.rect(self.screen, WHITE, (x * 24 + 240, y * 24, 24, 24), 0)
            del self.toadoduyet[index]
        pygame.draw.rect(self.screen, BLACK, (240, 0, WIDTH-240, 25), 0)
        pygame.draw.rect(self.screen, BLACK, (240, 768-25, WIDTH-240, 25), 0)
        # Draw grid
        # There are 52 square pixels across on grid [ WITHOUT BORDERS! ]
        # There are 30 square pixels vertically on grid [ WITHOUT BORDERS! ]
        #Vẽ dường viền
        for x in range(52):
            pygame.draw.line(self.screen, BLACK, (GS_X + x*self.grid_square_length, GS_Y),
                             (GS_X + x*self.grid_square_length, GE_Y))
        for y in range(30):
            pygame.draw.line(self.screen, BLACK, (GS_X, GS_Y + y*self.grid_square_length),
                             (GE_X, GS_Y + y*self.grid_square_length))
        

    def sketch_grid_buttons(self):
        # Draw buttons
        self.draw_text('Select function : ', self.screen, [90, 480], 14, RED, FONT, centered=True)
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)
        self.main_menu_button.draw_button(STEELBLUE)
        self.maze_generate_button.draw_button(STEELBLUE)
        self.reset_path.draw_button(STEELBLUE)
        # if self.algorithm_state == 'bfs':
        #     self.draw_text("Breadth-First Search", self.screen, [10,735], 20, VIOLETRED, FONT, centered = False)
        # elif self.algorithm_state == 'dfs':
        #     self.draw_text("Depth-First Search", self.screen, [10,735], 20, VIOLETRED, FONT, centered = False)
        # elif self.algorithm_state == 'astar':
        #     self.draw_text("A-Star Search", self.screen, [50,735], 20, VIOLETRED, FONT, centered = False)
        # elif self.algorithm_state == 'ids':
        #     self.draw_text("IDS", self.screen, [100,735], 20, VIOLETRED, FONT, centered = False)
        # elif self.algorithm_state == 'ucs':
        #     self.draw_text("Uniform-Cost Search", self.screen, [10,735], 20, VIOLETRED, FONT, centered = False)
        # elif self.algorithm_state == 'greedy':
        #     self.draw_text("Greedy Search", self.screen, [50,735], 20, VIOLETRED, FONT, centered = False)
        # elif self.algorithm_state == 'bidirectional':
        #     self.draw_text("Bidirectional Search", self.screen, [10,735], 20, VIOLETRED, FONT, centered = False)
    
    def sketch_grid_buttons_selectAlgorithm(self):
        # Draw buttons
        self.draw_text('Choose algorithm :', self.screen, [100, 240], 14, RED, FONT, centered=True)
        self.algorithm_bfs.draw_button(STEELBLUE)
        self.algorithm_dfs.draw_button(STEELBLUE)
        self.algorithm_ucs.draw_button(STEELBLUE)
        self.algorithm_ids.draw_button(STEELBLUE)
        self.algorithm_astar.draw_button(STEELBLUE)
        self.algorithm_greedy.draw_button(STEELBLUE)
        self.algorithm_bidirectional.draw_button(STEELBLUE)
    
    def grid_window_buttons_selectAlgorithm(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.algorithm_bfs.isOver(pos):
                self.algorithm_state = 'bfs'    
                self.state = 'grid window selectAlgorithm'
                
            elif self.algorithm_dfs.isOver(pos):
                self.algorithm_state = 'dfs'
                self.state = 'grid window selectAlgorithm'
            elif self.algorithm_ucs.isOver(pos):
                self.algorithm_state = 'ucs'
                self.state = 'grid window selectAlgorithm'
            elif self.algorithm_ids.isOver(pos):
                self.algorithm_state = 'ids'
                self.state = 'grid window selectAlgorithm'
            elif self.algorithm_astar.isOver(pos):
                self.algorithm_state = 'astar'
                self.state = 'grid window selectAlgorithm'
            elif self.algorithm_greedy.isOver(pos):
                self.algorithm_state = 'greedy'
                self.state = 'grid window selectAlgorithm'
            elif self.algorithm_bidirectional.isOver(pos):
                self.algorithm_state = 'bidirectional'
                self.state = 'grid window selectAlgorithm'
                
          

        # Get mouse position and check if it is hovering over button
        if event.type == pygame.MOUSEMOTION:
            if self.algorithm_bfs.isOver(pos):
                self.algorithm_bfs.colour = RED
            elif self.algorithm_dfs.isOver(pos):
                self.algorithm_dfs.colour = RED
            elif self.algorithm_ucs.isOver(pos):
                self.algorithm_ucs.colour = RED
            elif self.algorithm_ids.isOver(pos):
                self.algorithm_ids.colour = RED
            elif self.algorithm_astar.isOver(pos):
                self.algorithm_astar.colour = RED
            elif self.algorithm_greedy.isOver(pos):
                self.algorithm_greedy.colour = RED
            elif self.algorithm_bidirectional.isOver(pos):
                self.algorithm_bidirectional.colour = RED
            else:
                self.algorithm_bfs.colour, self.algorithm_dfs.colour,self.algorithm_ucs.colour,self.algorithm_ids.colour,self.algorithm_astar.colour,self.algorithm_greedy.colour,self.algorithm_bidirectional.colour =\
                    STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

##### Function for the buttons on grid window. Became too repetitive so, I made it a function.
    # Checks for state when button is clicked and changes button colour when hovered over.
    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.isOver(pos):
                self.state = 'draw walls'
            elif self.reset_button.isOver(pos):
                self.execute_reset()
            elif self.start_button.isOver(pos):
                self.state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                self.back_to_menu()
            elif self.maze_generate_button.isOver(pos):
                self.execute_reset()
                self.state = 'draw walls'
                self.maze.generateSolid()
                self.state = 'draw S/E'
            elif self.reset_path.isOver(pos):
                self.resetPath()

        # Get mouse position and check if it is hovering over button
        if event.type == pygame.MOUSEMOTION:
            if self.start_end_node_button.isOver(pos):
                self.start_end_node_button.colour = MINT
            elif self.wall_node_button.isOver(pos):
                self.wall_node_button.colour = MINT
            elif self.reset_button.isOver(pos):
                self.reset_button.colour = MINT
            elif self.start_button.isOver(pos):
                self.start_button.colour = MINT
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.colour = MINT
            elif self.maze_generate_button.isOver(pos):
                self.maze_generate_button.colour = MINT
            elif self.reset_path.isOver(pos):
                self.reset_path.colour = MINT
            else:
                self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, \
                self.start_button.colour, self.main_menu_button.colour, self.maze_generate_button.colour,self.reset_path.colour = \
                    STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE,STEELBLUE

    def grid_button_keep_selectAlgorithm(self):
        if self.algorithm_state == 'bfs':
            self.algorithm_bfs.colour = RED
        elif self.algorithm_state == 'dfs':
            self.algorithm_dfs.colour = RED
        elif self.algorithm_state == 'ucs':
            self.algorithm_ucs.colour = RED
        elif self.algorithm_state == 'ids':
            self.algorithm_ids.colour = RED
        elif self.algorithm_state == 'astar':
            self.algorithm_astar.colour = RED
        elif self.algorithm_state == 'greedy':
            self.algorithm_greedy.colour = RED
        elif self.algorithm_state == 'bidirectional':
            self.algorithm_bidirectional.colour = RED

    def grid_button_keep_colour(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.colour = MINT

        elif self.state == 'draw walls':
            self.wall_node_button.colour = MINT

    def execute_reset(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None


        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()
        self.maze = Maze(self, self.wall_pos)
        # Switch States
        self.state = 'grid window'
        #self.state = 'resetduongdi'

    def resetPath(self):

        # Start and End Nodes Coordinates
        # self.start_node_x = None
        # self.start_node_y = None
        # self.end_node_x = None
        # self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.maze = Maze(self, self.wall_pos)
        # Switch States
        self.state = 'grid window reset Path'


    def back_to_menu(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()
        self.maze = Maze(self, self.wall_pos)
        # Switch States
        self.state = 'main menu'


#################################### EXECUTION FUNCTIONS #########################################

##### MAIN MENU FUNCTIONS

    def main_menu_events(self):
        # Draw Background
        pygame.display.update()
        self.sketch_main_menu()
        self.draw_text('made by: nhom 13 (tham khao nhieu nguon)', self.screen, [900, 720], 24, WHITE, FONT, centered=False)

        # Check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'
                if self.dfs_button.isOver(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'
                if self.ids_button.isOver(pos):
                    self.algorithm_state = 'ids'
                    self.state = 'grid window'
                if self.ucs_button.isOver(pos):
                    self.algorithm_state = 'ucs'
                    self.state = 'grid window'
                if self.astar_button.isOver(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'
                if self.greedy_button.isOver(pos):
                    self.algorithm_state = 'greedy'
                    self.state = 'grid window'
                if self.bidirectional_button.isOver(pos):
                    self.algorithm_state = 'bidirectional'
                    self.state = 'grid window'

            # Get mouse position and check if it is hovering over button
            if event.type == pygame.MOUSEMOTION:
                if self.bfs_button.isOver(pos):
                    self.bfs_button.colour = AQUAMARINE
                elif self.dfs_button.isOver(pos):
                    self.dfs_button.colour = AQUAMARINE
                elif self.ids_button.isOver(pos):
                    self.ids_button.colour = AQUAMARINE
                elif self.ucs_button.isOver(pos):
                    self.ucs_button.colour = AQUAMARINE
                elif self.astar_button.isOver(pos):
                    self.astar_button.colour = AQUAMARINE
                elif self.greedy_button.isOver(pos):
                    self.greedy_button.colour = AQUAMARINE
                elif self.bidirectional_button.isOver(pos):
                    self.bidirectional_button.colour = AQUAMARINE
                else:
                    self.bfs_button.colour, self.dfs_button.colour, self.astar_button.colour, self.greedy_button.colour, \
                    self.bidirectional_button.colour,self.ucs_button.colour,self.ids_button.colour = WHITE, WHITE, WHITE, WHITE, WHITE , WHITE,WHITE

##### PLAYING STATE FUNCTIONS #####

    def grid_events(self):
        #print(len(wall_nodes_coords_list))
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        self.sketch_grid_buttons_selectAlgorithm()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)
            self.grid_window_buttons_selectAlgorithm(pos, event)
            self.grid_button_keep_selectAlgorithm()

    def grid_events_resetPath(self):
        #print(len(wall_nodes_coords_list))
        self.sketch_grid_resetPath()
        self.sketch_grid_buttons()
        self.sketch_grid_buttons_selectAlgorithm()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # Grid button function from Helper Funct
            self.grid_window_buttons(pos, event)
            self.grid_window_buttons_selectAlgorithm(pos, event)
            self.grid_button_keep_selectAlgorithm()

    def grid_events_selectAlgorithmions(self):
        #print(len(wall_nodes_coords_list))
        
        self.sketch_grid_buttons()
        self.sketch_grid_buttons_selectAlgorithm()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # Grid button function from Helper Funct grid_events_selectAlgorithmions
            self.grid_window_buttons_selectAlgorithm(pos, event)
            self.grid_window_buttons(pos, event)
            self.grid_button_keep_selectAlgorithm()

##### DRAWING STATE FUNCTIONS #####
    # Check where the mouse is clicking on grid
    # Add in feature to Draw nodes on grid
    # Add in feature so that the drawn nodes on grid translate onto text file
    def draw_nodes(self):
        # Function made in Helper Functions to check which button is pressed and to make it keep colour
        self.grid_button_keep_colour()
        self.sketch_grid_buttons()
        self.sketch_grid_buttons_selectAlgorithm()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)
            self.grid_window_buttons_selectAlgorithm(pos, event)
            self.grid_button_keep_selectAlgorithm()
            # Set boundaries for where mouse position is valid
            if pos[0] > 264 and pos[0] < 1512 and pos[1] > 24 and pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                #print('GRID-COORD:', x_grid_pos, y_grid_pos)

                # Get mouse position and check if it is clicking button. Then, draw if clicking. CHECK DRAG STATE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    # The chunk of code for start/end pos is placed here, because I do not want the drag feature to be available for start/end nodes
                    if self.state == 'draw S/E' and self.start_end_checker < 2:
                        # Choose point colour for grid and record the coordinate of start pos
                        if self.start_end_checker == 0 and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = TOMATO
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            # print(self.start_node_x, self.start_node_y)
                            self.start_end_checker += 1
                            # self.toadoduyet.append((self.start_node_x, self.start_node_y))

                        # Choose point colour for grid and record the coordinate of end pos
                        # Also, check that the end node is not the same point as start node
                        elif self.start_end_checker == 1 and (x_grid_pos+1, y_grid_pos+1) != (self.start_node_x, self.start_node_y) and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = ROYALBLUE
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.start_end_checker += 1
                            # self.toadoduyet.append((self.end_node_x, self.end_node_y))

                        else:
                            continue

                        # Draw point on Grid
                        pygame.draw.rect(self.screen, node_colour, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                # Checks if mouse button is no longer held down
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                # Checks if mouse button is being held down; drag feature
                if self.mouse_drag == 1:
                    # Draw Wall Nodes and append Wall Node Coordinates to the Wall Nodes List
                    # Check if wall node being drawn/added is already in the list and check if it is overlapping start/end nodes
                    if self.state == 'draw walls':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):
                            pygame.draw.rect(self.screen, BLACK, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)
                            self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))
                        # print(len(self.wall_pos))

                for x in range(52):
                    pygame.draw.line(self.screen, BLACK, (GS_X + x * self.grid_square_length, GS_Y),
                                     (GS_X + x * self.grid_square_length, GE_Y))
                for y in range(30):
                    pygame.draw.line(self.screen, BLACK, (GS_X, GS_Y + y * self.grid_square_length),
                                     (GE_X, GS_Y + y * self.grid_square_length))

#################################### VISUALIZATION FUNCTIONS #########################################

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        #print(self.start_node_x, self.start_node_y)
        #print(self.end_node_x, self.end_node_y)

        ### BFS ###

        if self.algorithm_state == 'bfs':
            self.bfs = BreadthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos,self.screen,self.sobuocduyet)
            if self.start_node_x or self.end_node_x is not None:
                start_time = time.time()  # Record the start time
                self.bfs.bfs_execute()
                end_time = time.time()  # Record the end time
                execution_time = end_time - start_time
                self.draw_text("time : " + str(execution_time) +"s", self.screen, [500,-10], 30, RED, FONT, centered = False)

            # Make Object for new path
            if self.bfs.route_found:
                self.draw_path = VisualizePath(self,self.screen, self.start_node_x, self.start_node_y, self.bfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
                self.draw_text('Da tìm thay duong di!', self.screen, [1000,735], 30, SPRINGGREEN, FONT, centered=False)
            else:
                self.draw_text('Khong tìm thay duong di', self.screen, [1000,735], 30, RED, FONT, centered=False)

        ### DFS ###

        elif self.algorithm_state == 'dfs':
            self.dfs = DepthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos,self.screen,self.sobuocduyet)

            if self.start_node_x or self.end_node_x is not None:
                start_time = time.time()  # Record the start time
                self.dfs.dfs_execute()
                end_time = time.time()  # Record the end time
                execution_time = end_time - start_time
                self.draw_text("time : " + str(execution_time) +"s", self.screen, [500,-10], 30, RED, FONT, centered = False)
                
            # Make Object for new path
            if self.dfs.route_found:
                self.draw_path = VisualizePath(self,self.screen, self.start_node_x, self.start_node_y, self.dfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
                self.draw_text('Da tìm thay duong di!', self.screen, [1000,735], 30, SPRINGGREEN, FONT, centered=False)
            else:
                self.draw_text('Khong tìm thay duong di', self.screen, [1000,735], 30, RED, FONT, centered=False)
        ### UCS ###

        elif self.algorithm_state == 'ucs':
            self.ucs = UCSFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos,self.screen,self.sobuocduyet)

            if self.start_node_x or self.end_node_x is not None:
                start_time = time.time()  # Record the start time
                self.ucs.ucs_execute()
                end_time = time.time()  # Record the end time
                execution_time = end_time - start_time
                self.draw_text("time : " + str(execution_time) +"s", self.screen, [500,-10], 30, RED, FONT, centered = False)
                
            # Make Object for new path
            if self.ucs.route_found:
                self.draw_path = VisualizePath(self,self.screen, self.start_node_x, self.start_node_y, self.ucs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
                self.draw_text('Da tìm thay duong di!', self.screen, [1000,735], 30, SPRINGGREEN, FONT, centered=False)
            else:
                self.draw_text('Khong tìm thay duong di', self.screen, [1000,735], 30, RED, FONT, centered=False)

        ### A-STAR ###

        elif self.algorithm_state == 'astar':
            self.astar = AStar(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos,self.screen,self.sobuocduyet)

            if self.start_node_x or self.end_node_x is not None:
                start_time = time.time()  # Record the start time
                self.astar.astar_execute()
                end_time = time.time()  # Record the end time
                execution_time = end_time - start_time
                self.draw_text("time : " + str(execution_time) +"s", self.screen, [500,-10], 30, RED, FONT, centered = False)

            if self.astar.route_found:
                self.draw_path = VisualizePath(self,self.screen, self.start_node_x, self.start_node_y, None, self.astar.route)
                self.draw_path.draw_path()
                self.draw_text('Da tìm thay duong di!', self.screen, [1000,735], 30, SPRINGGREEN, FONT, centered=False)
            else:
                self.draw_text('Khong tìm thay duong di', self.screen, [1000,735], 30, RED, FONT, centered=False)

        ### DIJKSTRA ###

        elif self.algorithm_state == 'greedy':
            self.greedy = GreedyBestFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos,self.screen,self.sobuocduyet)

            if self.start_node_x or self.end_node_x is not None:
                start_time = time.time()  # Record the start time
                self.greedy.greedy_execute()
                end_time = time.time()  # Record the end time
                execution_time = end_time - start_time
                self.draw_text("time : " + str(execution_time) +"s", self.screen, [500,-10], 30, RED, FONT, centered = False)


            if self.greedy.route_found:
                self.draw_path = VisualizePath(self,self.screen, self.start_node_x, self.start_node_y, None, self.greedy.route)
                self.draw_path.draw_path()
                self.draw_text('Da tìm thay duong di!', self.screen, [1000,735], 30, SPRINGGREEN, FONT, centered=False)
            else:
                self.draw_text('Khong tìm thay duong di', self.screen, [1000,735], 30, RED, FONT, centered=False)

        ### BIDRECTIONAL ###

        elif self.algorithm_state == 'bidirectional':
            self.bidirectional = Bidirectional(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos,self.screen,self.sobuocduyet)

            if self.start_node_x or self.end_node_x is not None:
                start_time = time.time()  # Record the start time
                self.bidirectional.bidirectional_execute()
                end_time = time.time()  # Record the end time
                execution_time = end_time - start_time
                self.draw_text("time : " + str(execution_time) +"s", self.screen, [500,-10], 30, RED, FONT, centered = False)

            if self.bidirectional.route_found:
                print(self.bidirectional.route_f)
                print(self.bidirectional.route_r)
                self.draw_path_f = VisualizePath(self,self.screen, self.start_node_x, self.start_node_y, None, self.bidirectional.route_f)
                self.draw_path_r = VisualizePath(self,self.screen, self.end_node_x, self.end_node_y, None, self.bidirectional.route_r)

                # Draw paths on the app
                self.draw_path_f.draw_path()
                self.draw_path_r.draw_path()
                self.draw_text('Da tìm thay duong di!', self.screen, [1000,735], 30, SPRINGGREEN, FONT, centered=False)
            else:
                self.draw_text('Khong tìm thay duong di', self.screen, [1000,735], 30, RED, FONT, centered=False)

        elif self.algorithm_state == 'ids':
            self.ids = IDS(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos,self.screen,self.sobuocduyet)
            if self.start_node_x or self.end_node_x is not None:
                start_time = time.time()  # Record the start time
                self.ids.ids_execute()
                end_time = time.time()  # Record the end time
                execution_time = end_time - start_time
                self.draw_text("time : " + str(execution_time) +"s", self.screen, [500,-10], 30, RED, FONT, centered = False)

            # Make Object for new path
            if self.ids.route_found:
                self.draw_path = VisualizePath(self,self.screen, self.start_node_x, self.start_node_y, self.ids.route, [])

                self.draw_path.get_path_coords()
                self.draw_path.draw_path()
                self.draw_text('Da tìm thay duong di!', self.screen, [1000,735], 30, SPRINGGREEN, FONT, centered=False)
            else:
                self.draw_text('Khong tìm thay duong di', self.screen, [1000,735], 30, RED, FONT, centered=False)

		

        pygame.display.update()
        self.state = 'aftermath'
        self.sobuocduyet = 0
        self.sobuocduongdi = 0

#################################### AFTERMATH FUNCTIONS #########################################

    def reset_or_main_menu(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = MINT
                elif self.start_button.isOver(pos):
                    self.start_button.colour = MINT
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.colour = MINT
                elif self.reset_path.isOver(pos):
                    self.reset_path.colour = MINT
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour, self.main_menu_button.colour,self.reset_path.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.isOver(pos):
                    self.execute_reset()
                elif self.main_menu_button.isOver(pos):
                    self.back_to_menu()
                elif self.reset_path.isOver(pos):
                    self.resetPath()
                
                





























