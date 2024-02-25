import random


def generate_random_map():
    map_grid = [[1 for _ in range(15)] for _ in range(15)]  # Increase map size

    def is_valid_cell(x, y):
        return 0 <= x < 15 and 0 <= y < 15

    def backtrack(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + 2 * dx, y + 2 * dy
            if is_valid_cell(new_x, new_y) and map_grid[new_x][new_y] == 1:
                map_grid[new_x][new_y] = 0
                map_grid[x + dx][y + dy] = 0
                backtrack(new_x, new_y)

    start_x, start_y = random.randint(0, 7) * 2, random.randint(0, 7) * 2
    map_grid[start_x][start_y] = 0
    backtrack(start_x, start_y)

    # Introduce more randomness by breaking some walls
    for i in range(15):
        for j in range(15):
            if random.random() < 0.6:  # Adjust probability for openness
                map_grid[i][j] = 0

    # Check for dead ends and convert them into corridors
    for i in range(15):
        for j in range(15):
            if map_grid[i][j] == 0:
                neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                num_openings = sum(1 for x, y in neighbors if is_valid_cell(x, y) and map_grid[x][y] == 0)
                if num_openings == 1:
                    map_grid[i][j] = 0  # Convert dead end into corridor

    return map_grid
