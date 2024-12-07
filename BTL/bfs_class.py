from settings import *

class BreadthFirst():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos,screen,sobuocduyet):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.visited = [(self.start_node_x, self.start_node_y)]
        self.route = None
        self.route_found = False
        self.sobuocduyet=sobuocduyet
        self.screen=screen

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def draw_all_paths(self, i, j):
        self.app.toadoduyet.append((i, j))
        print(self.app.toadoduyet)
        ##### Draw each node the computer is visiting as it is searching SIMULTNEOUSLY
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)
        self.draw_text("Visited : " + str(self.app.sobuocduyet), self.screen, [265,-10], 30, BLACK, FONT, centered = False)
        ##### Redraw start/end nodes on top of all routes
        pygame.draw.rect(self.app.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        # Redraw grid (for aesthetic purposes lol)
        for x in range(52):
            pygame.draw.line(self.app.screen, BLACK, (GS_X + x * 24, GS_Y), (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, BLACK, (GS_X, GS_Y + y * 24), (GE_X, GS_Y + y * 24))
        self.app.sobuocduyet = self.app.sobuocduyet + 1
        self.draw_text("Visited : " + str(self.app.sobuocduyet), self.screen, [265,-10], 30, TAN, FONT, centered = False)
        pygame.display.flip()  
        pygame.time.delay(5) 
        pygame.display.update()

    def checkValid(self, move):
        if move not in self.wall_pos and move not in self.visited:
            self.visited.append(move)
            return True
        return False

    def findEnd(self, first_out):
        if first_out == (self.end_node_x, self.end_node_y):
            return True
        return False

    def bfs_execute(self):
        print(self.wall_pos)
        queue = [(self.start_node_x, self.start_node_y)]
        moves_queue = ['']
        first_out = ''
        first_moves = ''

        while len(queue) > 0:
            # Parent variables of parent nodes at the given time
            first_out = queue.pop(0)
            first_moves = moves_queue.pop(0)    
            for m in ['L', 'R', 'U', 'D']:
                i, j = first_out
                if m == 'L':
                    i -= 1
                elif m == 'R':
                    i += 1
                elif m == 'U':
                    j -= 1
                elif m == 'D':
                    j += 1

                # Make new variable "latest_moves" for adding onto the queue again, because you don't want the 'parent' variable to change
                latest_moves = first_moves + m
                if self.checkValid((i, j)):
                    self.draw_all_paths(i, j)
                    queue.append((i, j))
                    moves_queue.append(latest_moves)

                if self.findEnd((i, j)):
                    self.route = latest_moves
                    self.route_found = True
                    break

            if self.route_found:
                break

