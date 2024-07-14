import random

class Maze:
    def __init__(self) -> None:
        self.dimensions = (68, 15)
        self.points = 10
        self.level = []

    def emptyLevel(self):
        """ Function to create an empty map"""
        self.level = [['#' for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]
        return self.level

    def establishRoutes(self):
        """ 
        Function to carve out routes across
        an empty map.
        """
        
        # Helper function to determine a pivot to start at
        def getPivotPosition(self):
            return (random.randint(1, (self.dimensions[0] - 1) // 2) * 2, random.randint(1, (self.dimensions[1] - 1) // 2) * 2)
        
        # Helper function to carve passage way in the maze
        def carvePassageWay(x, y):
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 1 <= nx < self.dimensions[0] - 1 and 1 <= ny < self.dimensions[1] - 1 and self.level[ny][nx] == '#':
                    self.level[ny - dy][nx - dx] = ' '
                    self.level[ny][nx] = ' '
                    carvePassageWay(nx, ny)

        start = getPivotPosition(self)
        level[start[1]][start[0]] = ' '
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        carvePassageWay(start[0], start[1])
        return level
    
    def getAssetPosition(self, asset):
        
        def getPivotPosition(self):
            return (random.randint(1, self.dimensions[0] - 2), random.randint(1, self.dimensions[1] - 2))
        
        asset_position_determined = True

        while asset_position_determined:
            asset_postion = getPivotPosition(self)

            if self.level[asset_postion[1]][asset_postion[0]] == " ":
                self.level[asset_postion[1]][asset_postion[0]] = asset
                return asset_postion
            
    def isMazeClearable(self, start_position, end_position, coins):

        def areAssetsReachable(start_position, end_position, collectabels = set()):
            frontier = [start_position]
            visited = set()

            while frontier:

                current_position = frontier.pop()

                if current_position == end_position:
                    return True
                
                if current_position not in visited:

                    visited.add(current_position)

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_position = (current_position[0] + dx, current_position[1] + dy)

                        if new_position in collectabels: continue

                        if 0 <= new_position[0] < self.dimensions[0] and 0 <= new_position[1] < self.dimensions[1]:

                            if self.level[new_position[1]][new_position[0]] != "#" and new_position not in visited:
                                frontier.append(current_position)

            return False


        if not areAssetsReachable(start_position, end_position):
            return False
        for coin in coins:
            if not areAssetsReachable(start_position, end_position, coin):
                return False
        return True


if __name__ == '__main__':
    while True:
        maze = Maze()
        level = maze.emptyLevel()
        level = maze.establishRoutes()
        start_position = maze.getAssetPosition("S")
        end_position = maze.getAssetPosition("E")
        coins = [maze.getAssetPosition("$") for _ in range(maze.points)]

        if maze.isMazeClearable(start_position, end_position, coins):
            break
    for row in level:
        print("".join(row))
