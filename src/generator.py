import random

"""
THIS IS A PROTOTYPE CODE 

IT DOES NOT WORK AS INTENDED AND IS TO 
BE USED AS FRAMEWORK FOR FUTURE CHANGES

RULES:
1. Don't touch it
2. Don't ask how it works
3. Follow all rules
"""

def create_map():
    width, height = 69, 15
    num_enemies = 10

    def print_map(map_grid):
        for row in map_grid:
            print(''.join(row))

    def place_item(map_grid, item):
        while True:
            x, y = random.randint(1, width - 2), random.randint(1, height - 2)
            if map_grid[y][x] == ' ':
                map_grid[y][x] = item
                return x, y

    def generate_paths(map_grid):
        def carve_passage(x, y):
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2 # Why times 2? don't know it just works T-T

                if 1 <= nx < width - 1 and 1 <= ny < height - 1 and map_grid[ny][nx] == '#':
                    map_grid[ny - dy][nx - dx] = ' '
                    map_grid[ny][nx] = ' '
                    carve_passage(nx, ny)

        start_x, start_y = random.randint(1, (width - 1) // 2) * 2, random.randint(1, (height - 1) // 2) * 2
        map_grid[start_y][start_x] = ' '
        carve_passage(start_x, start_y)

    def is_reachable(map_grid, start, end, avoid=set()): # base case, when no avoid
        stack = [start]
        visited = set()
        while stack:
            x, y = stack.pop()
            if (x, y) == end:
                return True
            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in avoid:
                        continue
                    if 0 <= nx < width and 0 <= ny < height and map_grid[ny][nx] != '#' and (nx, ny) not in visited:
                        stack.append((nx, ny))
        return False

    def ensure_reachability(map_grid, start, end, enemies):
        avoid = set(enemies)
        return is_reachable(map_grid, start, end, avoid)

    while True:
        map_grid = [['#' for _ in range(width)] for _ in range(height)]
        generate_paths(map_grid)
        start = place_item(map_grid, 'S') # messed up, no work
        end = place_item(map_grid, 'E') # same 
        enemies = [place_item(map_grid, '$') for _ in range(num_enemies)] #why would you think this would work? ofc its broken
        if ensure_reachability(map_grid, start, end, enemies):
            break

    print_map(map_grid)
    return map_grid

create_map()


# code works (not as intenteded but works)
