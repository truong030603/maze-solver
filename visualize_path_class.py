from settings import *

class VisualizePath():
    def __init__(self,app, surface, start_node_x, start_node_y, path, path_coords):
        self.app = app
        self.surface = surface
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.path = path
        self.path_coords = path_coords
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)
    # For BFS and DFS mainly
    def get_path_coords(self):
        i = self.start_node_x
        j = self.start_node_y
        for move in self.path:
            if move == 'L':
                i -= 1
            elif move == 'R':
                i += 1
            elif move == 'U':
                j -= 1
            elif move == 'D':
                j += 1
            self.path_coords.append((i,j))

    def draw_path(self):
        self.path_coords.pop()
        for (x_pos, y_pos) in self.path_coords:
            self.draw_text("Number of browsing steps : " + str(self.app.sobuocduongdi), self.app.screen, [1000,-10], 30, BLACK, FONT, centered = False)
            pygame.draw.rect(self.surface, SPRINGGREEN, (x_pos*24 + 240, y_pos*24, 24, 24), 0)
            self.app.sobuocduongdi = self.app.sobuocduongdi + 1
            self.draw_text("Number of browsing steps : " + str(self.app.sobuocduongdi), self.app.screen, [1000,-10], 30, SPRINGGREEN, FONT, centered = False)
            pygame.display.flip()  
            pygame.time.delay(20) 
