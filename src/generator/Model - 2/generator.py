import random
import time

class MapGenerator:
    def __init__(self, width=68, height=15, seekers=10, collectibles=10):
        self.width = width
        self.height = height
        self.seekers = seekers
        self.collectibles = collectibles
        self.map = []

    def generateMap(self):
        """ Generate a random map with walls, empty spaces, seekers, and collectibles """
        while True:
            self.map = [['#' for _ in range(self.width)] for _ in range(self.height)]

            # Randomly place empty spaces
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    if random.random() < 0.6:  # Adjust this value for density
                        self.map[y][x] = ' '

            # Place start and end positions
            start = (1, 1)
            end = (self.width - 2, self.height - 2)
            self.map[start[1]][start[0]] = 'S'
            self.map[end[1]][end[0]] = 'E'

            # Place seekers with a time limit
            self.start_time = time.time()
            placed_seekers = 0
            while placed_seekers < self.seekers and (time.time() - self.start_time) < 5:
                if self.placeSeekers():
                    placed_seekers += 1

            # Place collectibles
            for _ in range(self.collectibles):
                self.placeCollectibles()

            # Ensure the map is clearable
            if self.isMapClearable(start, end, self.getAssetPositions()):
                break

    def placeSeekers(self):
        """ Place a seeker in the map, avoiding positions between close walls """
        while True:
            if (time.time() - self.start_time) > 5:
                break
                return False
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.map[y][x] == ' ' and self.isBetweenClosedWalls(x, y) and self.seekersInVicinity(x, y):
                self.map[y][x] = '$'
                return True

        return False 


    def placeCollectibles(self):
        """ Place a collectible in the map, ensuring it is reachable """
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.map[y][x] == ' ':
                self.map[y][x] = 'C'
                return

    def isBetweenClosedWalls(self, x, y):
        """ Check if a position is between two close walls horizontally with less than 3 spaces """
        k = 1
        while self.map[y][x - k] != '#':
            if self.map[y][x - k] == '$':
                return False
            k += 1
        l = 1
        while self.map[y][x + l] != '#':
            if self.map[y][x + l] == '$':
                return False
            l += 1

        return True if k > 4 or l > 4 else False

    def seekersInVicinity(self, x, y):
        """ Function to check if a seeker is within a 2-block radius of another seeker """

        # Define the range to check (two-block radius in all directions)
        start_row = max(0, x - 2)
        end_row = min(self.width - 1, x + 2)
        start_col = max(0, y - 2)
        end_col = min(self.height - 1, y + 2)

        # Check the surrounding cells within the two-block radius
        for i in range(start_row, end_row + 1):
            for j in range(start_col, end_col + 1):
                if (i == x and j == y):
                    continue
                if self.map[j][i] == '$':
                    return False
        return True

    def getAssetPositions(self):
        """ Get positions of all seekers and collectibles """
        assets = []
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in ('$','C'):
                    assets.append((x,y))
        return assets

    def isMapClearable(self, start, end, assets):
        """ Check if the map is clearable from start to end, collecting all assets """
        def bfs(start, goals):
            queue = [start]
            visited = set()
            found = set()

            while queue:
                x, y = queue.pop(0)
                if (x, y) in goals:
                    found.add((x, y))
                if len(found) == len(goals):
                    return True
                if (x, y) not in visited:
                    visited.add((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.map[ny][nx] in (' ', 'S', 'E', '$', 'C') and (nx, ny) not in visited:
                            queue.append((nx, ny))
            return False

        return bfs(start, {end} | set(assets))

    def printMap(self):
        """ Print the map """
        for row in self.map:
            print("".join(row))

if __name__ == '__main__':
    random_map = MapGenerator()
    random_map.generateMap()
    random_map.printMap()
