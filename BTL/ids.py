from settings import *
import pygame

class IDS:
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos, screen, sobuocduyet):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.wall_pos = set(wall_pos)
        self.route = None
        self.route_found = False
        self.sobuocduyet = sobuocduyet
        self.screen = screen

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
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)
        self.draw_text("Visited : " + str(self.sobuocduyet), self.screen, [265, -10], 30, BLACK, FONT,
                       centered=False)
        pygame.draw.rect(self.app.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)
        for x in range(52):
            pygame.draw.line(self.app.screen, BLACK, (GS_X + x * 24, GS_Y), (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, BLACK, (GS_X, GS_Y + y * 24), (GE_X, GS_Y + y * 24))
        self.sobuocduyet = self.sobuocduyet + 1
        self.draw_text("Visited : " + str(self.sobuocduyet), self.screen, [265, -10], 30, TAN, FONT,
                       centered=False)
        pygame.display.flip()
        pygame.time.delay(5)
        pygame.display.update()

    def check_valid(self, move):
        return move not in self.wall_pos

    def find_end(self, first_in):
        return first_in == (self.end_node_x, self.end_node_y)

    def ids_execute(self):
        _depth_max = 20
        _ready_stack = [(0, (self.start_node_x, self.start_node_y), [])]
        visited = set()

        while _ready_stack:
            _stack = _ready_stack[:]
            _ready_stack.clear()

            while _stack:
                _depth, _current_node, path = _stack.pop()

                if _current_node not in visited:
                    visited.add(_current_node)
                    for m in ['L', 'U', 'D', 'R']:
                        i, j = _current_node
                        if m == 'L':
                            i -= 1
                        elif m == 'R':
                            i += 1
                        elif m == 'U':
                            j -= 1
                        elif m == 'D':
                            j += 1

                        if self.check_valid((i, j)):
                            if self.find_end((i, j)):
                                self.route_found = True
                                path += [m]
                                self.route = path[:]
                                return

                            self.draw_all_paths(i, j)

                            if _depth + 1 < _depth_max:
                                _stack.append((_depth + 1, (i, j), path + [m]))
                            else:
                                _ready_stack.append((_depth + 1, (i, j), path + [m]))

            _depth_max += 20

# Rest of your code...
