def read_grid(filename):

    # CODE IS SELF EXPLANATORY
    # STILL CAN'T UNDERSTAND
    # HERE YOU GO ->


    # open file
    with open(filename, 'r') as file:

        # read file
        grid = [list(line.strip()) for line in file.readlines()]

    # return file
    return grid

# IF YOU JUST READ ALL THESE COMMENTS YOU ARE EITHER
# DUMB 
# Or
# TOO BORED WITH LIFE
