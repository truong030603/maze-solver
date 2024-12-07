from settings import *

class Node:
    def __init__(self, position = None, parent = None):
        self.position = position
        self.parent = parent
        self.G = 0
        self.H = 0
        self.F = 0

class AStar():
    def __init__(self, app, start_node_x, start_node_y, end_node_x, end_node_y, wall_pos,screen,sobuocduyet):
        self.app = app
        self.start_node_x = start_node_x
        self.start_node_y = start_node_y
        self.end_node_x = end_node_x
        self.end_node_y = end_node_y
        self.open_list = []
        self.closed_list = []
        self.wall_pos = wall_pos
        self.route = []
        self.route_found = False
        self.sobuocduyet=sobuocduyet
        self.screen=screen

    def draw_all_paths(self, current):
        i, j = current
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)
        self.draw_text("Visited : " + str(self.sobuocduyet), self.screen, [265,-10], 30, BLACK, FONT, centered = False)
 
        pygame.draw.rect(self.app.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)
        for x in range(52):
            pygame.draw.line(self.app.screen, BLACK, (GS_X + x * 24, GS_Y), (GS_X + x * 24, GE_Y))
        for y in range(30):
            pygame.draw.line(self.app.screen, BLACK, (GS_X, GS_Y + y * 24), (GE_X, GS_Y + y * 24))
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
        
    def generate_children(self, parent, end_node):
        print('generating children')
        parent_pos = parent.position
        for m in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            child_pos = (parent_pos[0] + m[0], parent_pos[1] + m[1])
            if self.check_valid(child_pos):
                child = Node(child_pos, parent)
                self.G_calc(child, parent, m)
                self.H_calc(child, end_node)
                self.F_calc(child)
                # print(f"nút {child_pos} , h = {child.H} ,g={child.G} ,f= {child.F}")
                if self.append_to_open(child)   :
                    self.open_list.append(child)

    def append_to_open(self, child):
        for open_node in self.open_list:

            if child.position == open_node.position and child.F >= open_node.F:
                return False
        return True


    # ham G qua to lan ap ca gia tri H 
    def G_calc(self, child, parent, m):
        # sum_difference = abs(sum(m))
        # if sum_difference == 1:
        #     child.G = parent.G + 1.4
        # elif sum_difference == 0 or sum_difference == 2:
        #     child.G = parent.G + 1
        child.G = parent.G + 1
    def H_calc(self, child, end_node):
        child.H = (((end_node.position[0] - child.position[0]) ** 2) + ((end_node.position[1] - child.position[1] ) ** 2))**0.5
        child.H = child.H * 1.38
    def F_calc(self, child):
        child.F = (child.G + child.H)/2

    def check_valid(self, move):
        if move not in self.wall_pos and move not in self.closed_list:
            return True
        return False

    def findEnd(self, current):
        if current == (self.end_node_x, self.end_node_y):
            return True
        return False

    def astar_execute(self):
        start_node = Node((self.start_node_x, self.start_node_y), None)
        start_node.G = start_node.H = start_node.F = 0
        end_node = Node((self.end_node_x, self.end_node_y), None)
        end_node.G = end_node.H = end_node.F = 0

        self.open_list.append(start_node)

        print(start_node.position)
        print(end_node.position)

        while len(self.open_list) > 0:
            current_node = self.open_list.pop(0)
            print(f"current pop ={current_node.position}")
            if self.findEnd(current_node.position):
                current = current_node
                
                while current is not None:
                    self.route.append(current.position)
                    current = current.parent
                self.route.reverse()  
                self.route.pop(0)
                self.route_found = True
                break

            self.generate_children(current_node, end_node)
            self.draw_all_paths(current_node.position)

            # self.open_list.pop(current_index)
            self.open_list.sort(key= lambda x: x.F)
            for i in self.open_list:
                print(f"h={i.H} :: {i.F}",end=", ")
            print()
            self.closed_list.append(current_node.position)
















