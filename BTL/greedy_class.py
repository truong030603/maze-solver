from settings import *

class GreedyBestFirst():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos,screen,sobuocduyet):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = wall_pos
        self.visited = [(self.start_node_x, self.start_node_y, None)]  # Add None for parent
        self.route = []
        self.route_found = False
        self.sobuocduyet=sobuocduyet
        self.screen=screen

    def heuristic(self, current_node):
        # Simple Euclidean distance heuristic
        return ((current_node[0] - self.end_node_x) ** 2 + (current_node[1] - self.end_node_y) ** 2) ** 0.5

    def draw_all_paths(self, i, j):
        self.app.toadoduyet.append((i, j))
        # Similar drawing logic as in DFS
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)
        self.draw_text("Visited : " + str(self.sobuocduyet), self.screen, [265,-10], 30, BLACK, FONT, centered = False)
        pygame.draw.rect(self.app.screen, TOMATO,
                         (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE,
                         (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)
        for x in range(52):
            pygame.draw.line(self.app.screen, BLACK, (GS_X + x * 24, GS_Y),
                             (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, BLACK, (GS_X, GS_Y + y * 24),
                             (GE_X, GS_Y + y * 24))
        self.sobuocduyet = self.sobuocduyet + 1
        self.draw_text("Visited : " + str(self.sobuocduyet), self.screen, [265,-10], 30, TAN, FONT, centered = False)
        pygame.display.flip()
        pygame.time.delay(5)
        pygame.display.update()

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)
        
    def checkValid(self, move):
        if move not in self.wall_pos and move not in self.visited:
            self.visited.append(move)
            return True
        return False

    def findEnd(self, current_node):
        if current_node[0] == self.end_node_x and current_node[1] == self.end_node_y:
            return True
        return False

    def greedy_execute(self):
        priority_queue = [(self.start_node_x, self.start_node_y, None)]  # Add None for parent
        while priority_queue:
            priority_queue.sort(key=lambda x: self.heuristic(x),reverse=False)
            current_node = priority_queue.pop(0)
            for m in ['L', 'R', 'U', 'D']:
                i, j, _ = current_node  # Ignore the parent for now
                if m == 'L':
                    i -= 1
                elif m == 'R':
                    i += 1
                elif m == 'U':
                    j -= 1
                elif m == 'D':
                    j += 1

                if self.findEnd((i, j)):
                    priority_queue.append((i, j, current_node))
                    priority_queue.sort(key=lambda x: self.heuristic(x),reverse=False)
                    current_node = priority_queue.pop(0)
                    current = current_node
                    while current is not None:
                        self.route.append((current[0], current[1]))
                        current = current[2]  # Access the parent
                    self.route.reverse()  # Reverse the route to have it from start to end
                    self.route.pop(0)  # Remove the start node from the route
                    self.route_found = True
                    break

                if self.checkValid((i, j)):
                    priority_queue.append((i, j, current_node))  # Include the current_node as parent
                    self.draw_all_paths(i, j)

            if self.route_found:
                break
