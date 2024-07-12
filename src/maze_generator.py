import random

class Maze:
    def __init__(self) -> None:
        self.dimensions = (68, 15)

    def emptyLevel(self):
        """ Function to create an empty map"""
        level = [['#' for _ in range(self.dimensions[0])] for _ in range(self.dimensions[1])]
        return level

    def establishRoutes(self, level):
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
                if 1 <= nx < self.dimensions[0] - 1 and 1 <= ny < self.dimensions[1] - 1 and level[ny][nx] == '#':
                    level[ny - dy][nx - dx] = ' '
                    level[ny][nx] = ' '
                    carvePassageWay(nx, ny)

        start = getPivotPosition(self)
        level[start[1]][start[0]] = ' '
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        carvePassageWay(start[0], start[1])
        return level
    
    def getAssetPosition(self, level, asset):
        
        def getPivotPosition(self):
            return (random.randint(1, self.dimensions[0] - 2), random.randint(1, self.dimensions[1] - 2))
        
        asset_position_determined = True

        while asset_position_determined:
            asset_postion = getPivotPosition(self)

            if level[asset_postion[1]][asset_postion[0]] == " ":
                level[asset_postion[1]][asset_postion[0]] = asset
                return level, asset_postion


if __name__ == '__main__':
    maze = Maze()
    level = maze.emptyLevel()
    level = maze.establishRoutes(level)
    level, asset_position = maze.getAssetPosition(level, "S")
    for row in level:
        print("".join(row))
