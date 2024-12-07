from settings import *

class DepthFirst():
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
        ##### Draw each node the computer is visiting as it is searching SIMULTNEOUSLY
        pygame.draw.rect(self.app.screen, TAN, (i * 24 + 240, j * 24, 24, 24), 0)
        self.draw_text("Visited : " + str(self.sobuocduyet), self.screen, [265,-10], 30, BLACK, FONT, centered = False)

        ##### Redraw start/end nodes on top of all routes
        pygame.draw.rect(self.app.screen, TOMATO,
                         (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.app.screen, ROYALBLUE,
                         (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        # Redraw grid (for aesthetic purposes lol)
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

    def checkValid(self, move):
        if move not in self.wall_pos and move not in self.visited:
            self.visited.append(move)
            return True
        return False

    def findEnd(self, first_in):
        if first_in == (self.end_node_x, self.end_node_y):
            return True
        return False
    def dfs_execute(self):
        stack = []
        first_in = (self.start_node_x, self.start_node_y)
        stack.append(first_in)

        moves_stack = []
        moves_first_in = ''
        moves_stack.append(moves_first_in)

        while len(stack) > 0:
            last_out = stack[-1]  # Lấy phần tử trên cùng của stack mà không xóa nó
            moves_last_out = moves_stack[-1]

            i, j = last_out

            # Kiểm tra nếu đạt được nút đích
            if self.findEnd((i, j)):
                self.route = moves_last_out
                self.route_found = True
                break

            # Tạo danh sách các bước có thể đi
            possible_moves = ['U', 'R', 'D', 'L']

            # Lặp qua từng hướng di chuyển
            move_found = False
            for m in possible_moves:
                new_i, new_j = i, j  # Sao chép vị trí hiện tại

                # Thay đổi vị trí dựa trên hướng di chuyển
                if m == 'L':
                    new_i -= 1
                elif m == 'R':
                    new_i += 1
                elif m == 'U':
                    new_j -= 1
                elif m == 'D':
                    new_j += 1

                # Kiểm tra nếu di chuyển hợp lệ
                if self.checkValid((new_i, new_j)):
                    stack.append((new_i, new_j))
                    moves_stack.append(moves_last_out + m)
                    self.draw_all_paths(new_i, new_j)
                    move_found = True
                    break

            # Nếu không tìm thấy bước di chuyển mới, quay lui
            if not move_found:
                stack.pop()
                moves_stack.pop()

            if self.route_found:
                break


    # def dfs_execute(self):
    #     stack = []
    #     first_in = (self.start_node_x, self.start_node_y)
    #     stack.append(first_in)

    #     moves_stack = []
    #     moves_first_in = ''
    #     moves_stack.append(moves_first_in)

    #     while len(stack) > 0:
    #         last_out = stack.pop()
    #         moves_last_out = moves_stack.pop()

    #         for m in ['U', 'R', 'D', 'L']:
    #             i, j = last_out
    #             if m == 'L':
    #                 i -= 1
    #             elif m == 'R':
    #                 i += 1
    #             elif m == 'U':
    #                 j -= 1
    #             elif m == 'D':
    #                 j += 1

    #             move_update = moves_last_out + m

    #             if self.findEnd((i, j)):
    #                 self.route = move_update
    #                 self.route_found = True
    #                 break

    #             if self.checkValid((i, j)):
    #                 stack.append((i, j))
    #                 moves_stack.append(move_update)
    #                 self.draw_all_paths(i, j)
    #                 break

    #         if self.route_found:
    #             break






