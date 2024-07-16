import random

class MapGenerator:
    def __init__(self, width=68, height=15, points=15, collectibles=5):
        self.width = width
        self.height = height
        self.points = points
        self.collectibles = collectibles
        self.map = []

    def generateMap(self):
        """ Generate a random map with walls, empty spaces, coins, and collectibles """
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

            # Place coins
            coins = [self.placeCoins() for _ in range(self.points)]

            # Place collectibles
            collectibles = [self.placeCollectables() for _ in range(self.collectibles)]

            # Ensure the map is clearable
            if self.isMapClearable(start, end, coins + collectibles):
                break

    def placeCoins(self):
        """ Place a coin in the map, avoiding positions between close walls """
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.map[y][x] == ' ' and not self.isBetweenClosedWalls(x, y):
                self.map[y][x] = '$'
                return (x, y)

    def placeCollectables(self):
        """ Place a collectible in the map, ensuring it is reachable """
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.map[y][x] == ' ':
                self.map[y][x] = 'C'
                return (x, y)

    def isBetweenClosedWalls(self, x, y):
        """ Check if a position is between two close walls horizontally with less than 3 spaces """
        count = 0
        for i in range(max(0, x-2), min(self.width, x+3)):
            if self.map[y][i] == '#':
                count += 1
            else:
                count = 0
            if count >= 2:
                return True
        return False

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
