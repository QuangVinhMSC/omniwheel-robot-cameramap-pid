import pygame
import sys
import numpy as np
import random
import time
# Kích thước của mỗi ô trong grid
CELL_SIZE = 5
# Số hàng và số cột của grid
GRID_ROWS = 100
GRID_COLS = 100
# Kích thước của khung vuông hiển thị
DISPLAY_WIDTH = GRID_COLS * CELL_SIZE
DISPLAY_HEIGHT = GRID_ROWS * CELL_SIZE
# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def draw_tobot_point(screen, robot_pos):
    # Vẽ điểm ban đầu màu xanh tại vị trí (50, 50)
    pygame.draw.circle(screen, GREEN, (robot_pos[0] * CELL_SIZE + CELL_SIZE // 2, robot_pos[1] * CELL_SIZE + CELL_SIZE // 2), 2)
def apply_function(points):
    # Đây là nơi để định nghĩa hàm mà bạn muốn thực thi sau khi nhấn Apply
    print("Function applied")
    points_divided = [(x // 5, y // 5) for x, y in points]
    print("Points:", points_divided)

def draw_line(screen, start, end):
    pygame.draw.line(screen, RED, start, end, 1)

def get_robot_point():
    # Giả sử bạn có một danh sách các tọa độ và bạn muốn lấy ngẫu nhiên một trong số chúng
    coordinates = [(50, 50), (60, 60), (70, 70)]  # Các tọa độ của điểm ban đầu
    # Cập nhật liên tục tọa độ của điểm ban đầu sau mỗi khoảng thời gian
    while True:
        # Lấy một tọa độ ngẫu nhiên từ danh sách
        initial_point = random.choice(coordinates)
        yield initial_point
        # Chờ 1 giây trước khi lấy tọa độ mới
        time.sleep(1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Interactive Grid")

    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    running = True
    drawing = True
    points = []
    robot_point_gen = get_robot_point()
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = event.pos
             
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    if grid[row][col] == 0 and len(points) < 100:  # Kiểm tra điều kiện để điểm không vượt quá 100
                        grid[row][col] = 1
                        points.append((col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                        if drawing and len(points) >= 2:
                            draw_line(screen, points[-2], points[-1])
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    apply_function(points)

        screen.fill(WHITE)
        robot_pos = next(robot_point_gen())
        # Vẽ grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        # Vẽ các điểm
        for point in points:
            pygame.draw.circle(screen, RED, point, 2)
        draw_tobot_point(screen, robot_pos)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
