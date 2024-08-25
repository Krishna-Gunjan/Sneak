
# Sneak

A 2D game where you have to navigate through structures while avoiding seekers who can hear you if make too much noise. Coins are scattered through the map waiting to be collected.


## Demo

This game was made stricty for windows and some file path problems may arise on diffrent versions. 

To fix such issues you can manually change the paths defined. Sorry for the inconvience due to me being a sloppy dev.

TO RUN THE GAME: execute the main file from inside the parent repository `Sneak`. 

`python main.py src\main.py`     


## Features

- Infinite maps

- Customisable (change the number of seeker/coins/noise radius expansion rate)

- Fullscreen mode

- Interactive

- Rage Quit

- Press `1` to take screenshot

## BUGS

#### 1: Are all levels beatable?

 Due to infinte map generation, sometime there is a small chance that the map generated is impossible to beat. Such maps are usually those where a seeker is set in a long column with no branches to hide in.

 In such cases, press `R` to reset the game

#### 2. My map is not loading/ taking too much time.

This game uses random asset placing and can some time take lots of time to generate new maps on old pcs. 
At average it only takes 5 seconds to generate a map. In case your map is not loading, you can make the following changes to `src\generator\Model - 2\generator.py`

    1. reducing the number of seekers
    2. reducing the number of coins
    3. lessening the maze density

#### 3. Too Easy or too hard.

You can make changes to `src\generator\Model - 2\generator.py` by increasing the number of seekers or coins or lessening them.

for a change, you can change the `initial_circle_radius` or change the code to increase or decrease the circle radius upon movement.

#### 4. I am not familiar with python, how can I make code changes?

I have tried to make the code as readable as possible by adding proper comments, spacing, coding style, pattern and naming. So, even a little programming knowledge and common sense can allow you to mend the game by yourself.

#### 5. Can I rewrite src\generator\Model - 2\generator.py

NO... unless you are a 10x dev don't even touch it. Only god knows how that code work. It's a piece, I copy pasted from ChatGPT but only the initial code. I have made many changes and trust me when I say this. ChatGPT can't do ANYTHING about it.
