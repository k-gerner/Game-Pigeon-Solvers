# Sea Battle  
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/sampleSeaBattleBoard.png" alt = "sample board" width="30%" align = "right">  

### The Basics  
Sea Battle is essentially "Battleship" with a few rule changes. Each player has ships varying from lengths 1 to 4, and they can be placed on the board vertically or horizontally. Ships cannot be within 1 tile of one another. Each player picks a tile to attack. If they miss, their turn is over, but if they hit a ship, they keep going until they miss. The game is over once one player destroys all of the other player's ships.  
### How to use
First, download the `sea_battle_tool.py` file. You can invoke the tool by running  
```
> python3 sea_battle_tool.py
```
You will be presented with the intro screen with some instructions:  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/starting_prompts.png" alt = "starting instructions" width="60%"><br/>  
  
You will be asked which dimension you want to make the board. Sea Battle has 8x8, 9x9, and 10x10 modes available. Each mode has a different set of ships, as seen below:  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/starting_8board.png" alt = "starting 8x8 board" width="34%" align = "left">
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/starting_9board.png" alt = "starting 9x9 board" width="30%" align = "left">
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/starting_10board.png" alt = "starting 10x10 board" width="32%"><br/>  

You will be prompted to press `enter` to receive the best moves each turn, which will be colored blue. To see the scores that the A.I. has calcuated for each location on the board, you can type `sdc` to show the space densities table (or `sd` to display with no color). The number mostly corresponds to how many ways a ship could be placed at that location, so a higher number means that the space is more likely to have a ship. While only the optimal move(s) will be shown on the board display, the densities table uses a color gradient so that you can easily see the good locations on the board if you do not wish to play in one of the optimal spaces. At the beginning of a 10x10 game, the game board and density table will look like this:  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/starting_bestmoves.png" alt = "starting 10x10 board best moves" width="40%" align = "left">
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/starting_densities.png" alt = "starting 10x10 space densities" width="45%"><br/>    
  
As the game progresses, ships will be destroyed and removed from the ship counter. This will also affect how the densities are computed. A 10x10 match in mid-game is shown below, as well as the corresponding space densities table. The white `-` represent open spaces (available moves), the red `^` represent misses, the yellow `H` represent hits, and the green `D` represent destroyed ships.  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/midgame_board.png" alt = "mid-game 10x10 board" width="40%" align = "left">
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Sea%20Battle/midgame_densities.png" alt = "mid-game space densitites" width="45%"><br/>  

After the player selects a move, they will be asked whether the move resulted in a miss, hit, or sink. It will then update the board and space densities accordingly. If the player chooses a space that is not in the optimal move set, the player will be asked to confirm that they meant to choose that location. This is to prevent accidental incorrect input.
