# Tạo một danh sách các tọa độ các nút biên cho mê cung với width và height tùy ý
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
custom_width = 30
custom_height = 10

# Tạo mê cung dựa trên kích thước mới
wall_nodes_coords_list = create_maze(custom_width, custom_height)

# Tạo một ma trận để biểu diễn mê cung
maze = [[' ' for _ in range(custom_width)] for _ in range(custom_height)]

# Đánh dấu các ô biên trong mê cung
for x, y in wall_nodes_coords_list:
    maze[y][x] = '#'

# In mê cung lên console
for row in maze:
    print(' '.join(row))