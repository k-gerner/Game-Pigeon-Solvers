# Sea Battle  
<img src="/images/Sea%20Battle/sampleSeaBattleBoard.png" alt = "sample board" width="30%" align = "right">  

### The Basics  
Sea Battle is essentially "Battleship" with a few rule changes. Each 
player has ships varying from lengths 1 to 4, and they can be placed 
on the board vertically or horizontally. Ships cannot be within 1 
tile of one another. Each player picks a tile to attack. If they miss, 
their turn is over, but if they hit a ship, they keep going until 
they miss. The game is over once one player destroys all the other 
player's ships.  
### How to use
First, download this project. You can invoke the tool by running  
```
> python3 ai_runner.py --game=seabattle
```
You will be presented with the intro screen with some instructions:  

<img src="/images/Sea%20Battle/starting_prompts.png" alt = "starting instructions" width="65%"><br/>  
  
You will be asked which dimension you want to make the board. Sea 
Battle has 8x8, 9x9, and 10x10 modes available. Each mode has a 
different set of ships, as seen below:  

<img src="/images/Sea%20Battle/starting_8board.png" alt = "starting 8x8 board" width="34%" align = "left">
<img src="/images/Sea%20Battle/starting_9board.png" alt = "starting 9x9 board" width="30%" align = "left">
<img src="/images/Sea%20Battle/starting_10board.png" alt = "starting 10x10 board" width="32%"><br/>  

Before each turn, the best moves will be shown on the board in blue. 
To see the scores that the A.I. has calculated for each location on 
the board, you can type `d` to show the space densities table. The 
number mostly corresponds to how many ways a ship could be placed 
at that location, so a higher number means that the space is more 
likely to have a ship. The AI also takes into account the number of 
spaces that would be cleared if the spot were to result in a hit/sink.
While only the optimal move(s) will be shown on the board display, the 
densities table uses a color gradient so that you can easily see the 
good locations on the board if you do not wish to play in one of the
optimal spaces. At the beginning of a 10x10 game, the game board and 
density table will look like this:  

<img src="/images/Sea%20Battle/starting_bestmoves.png" alt = "starting 10x10 board best moves" width="40%" align = "left">
<img src="/images/Sea%20Battle/starting_densities.png" alt = "starting 10x10 space densities" width="45%"><br/>    
  
As the game progresses, ships will be destroyed and removed from the 
ship counter. This will also affect how the densities are computed. 
A 10x10 match in mid-game is shown below, as well as the corresponding 
space densities table. The white `-` represent open spaces (available 
moves), the red `^` represent misses, the yellow `H` represent hits, 
and the green `D` represent destroyed ships.  

<img src="/images/Sea%20Battle/midgame_board.png" alt = "mid-game 10x10 board" width="40%" align = "left">
<img src="/images/Sea%20Battle/midgame_densities.png" alt = "mid-game space densitites" width="45%"><br/>  

After the player selects a move, they will be asked whether the move 
resulted in a miss, hit, or sink. It will then update the board and 
space densities accordingly. If the player chooses a space that is 
not in the optimal move set, the player will be asked to confirm that 
they meant to choose that location. This is to prevent accidental 
incorrect input.  

If at any point you would like to save the game to come back later, 
you can type `s` at a move selection prompt.

### ✨ New in Version 1.3
* You can now save the game by typing `s`. This will create a save 
file named `saved_game.txt` which contains save data for the current 
game state. When you start a new game, if a save state is detected, 
you will be asked if you would like to resume that game.

#### Older Changelog
* v1.2
  * The space densities table will now be displayed in place of the
      board, instead of below it.
  * The space densities table will now default to having colored text.
  * The space densities table will now be displayed by typing `d`
    (formerly `sd` or `sdc`)
  * The game board can be redisplayed by typing `b` (formerly `sb`)
* v1.1
  * The game will now be played on a single game board instead of 
  printing a new board after each turn. This can be turned off with 
  the command line argument `-e` or `-eraseModeOff`.
