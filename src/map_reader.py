class MapReader():

    def __init__(self) -> None:
        self.current_stage = 1
        self.stage_path = f"maps\stage_{self.current_stage}.txt"
        self.stage = []

    def readMap(self) -> list[list[str]]:

        with open(self.stage_path, 'r') as file:

            self.stage = [list(row.strip()) for row in file.readlines()]

        return self.stage
    
    def mapDimensions(self):
        return (len(self.stage[0]), len(self.stage))