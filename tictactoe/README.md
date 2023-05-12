# Tic-Tac-Toe  
<img src="/Images/Tic%20Tac%20Toe/sampleBoardOutput.png" alt = "sample board" width="30%" align = "right">  

(This is not a Game Pigeon game, but it is similar enough to my 
other AI's ([Connect 4](/connect4), [Othello](/othello),
and [Gomoku](/gomoku)) in terms of implementation, so I decided 
to knock out an AI for it)  

### The Basics  
In Tic-Tac-Toe, the objective is to get 3 of your pieces in a 
row on the board, in any direction.  
### How to use  
First, download `tictactoe_client.py` and `strategy.py` files and 
place them both in the same directory. If you would like to challenge 
my AI with your own, see the [Dueling AIs Mode](#dueling-ais-mode) 
section. If you would like to challenge the AI yourself, you can 
invoke the tool by running  
```
> python3 tictactoe_client.py
```
Once you do this, you will be asked whether you want to play as `X` 
or `O`. 

Whoever is `X` will go first. Your pieces will be colored 
<span style="color:lightgreen">green</span>, and the AI's pieces 
will be colored <span style="color:red">red</span>. If it is your 
turn, you will enter the name of the spot you want to play (e.g. 
`B2`). Then, you will be prompted to press `enter` to have the A.I. 
play its best move. At any point, if you want to quit, you can simply 
type `q` as your move input.

### How it works
The A.I. works by using a move selection algorithm known as [Minimax](https://en.wikipedia.org/wiki/Minimax), and uses a pruning technique known as [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). Minimax works by assuming that the opponent will make the best possible move at each turn. By doing this, the A.I. can look several moves ahead. Then, it can pick the best possible outcome.  

Alpha-Beta pruning works by keeping track of the best already 
explored option along the path to the root for the maximizer 
(alpha), and the best already explored option along the path to 
the root for the minimizer (beta). A good explanatory video can 
be found [here](https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013).

### Dueling AIs Mode
Do you have your own Tic-Tac-Toe AI? Challenge mine! This program 
includes the ability for you to challenge it with a rival AI. To 
use this functionality, include a command line argument `-d` or 
`-aiDuel` followed by the name of your Python file. For example, if 
your AI was located in `myAiFile.py`, you would run:
```
> python3 tictactoe_client.py -d myAiFile
```

In order for your AI to be eligible, it must meet a few requirements:
* AI logic must be contained in a class named `TicTacToeStrategy`
* AI must be a subclass of `Player`, found in `Player.py`
* AI must have a function named `getMove` that accepts a game board 
as a parameter, and returns the chosen move coordinates in the form of 
a tuple in the format `(rowNumber, columnNumber)`

### Additional Features
- Save the game by typing `s`. This will create a save
  file named `saved_game.txt` which contains save data for the current
  game state. When you start a new game, if a save state is detected,
  you will be asked if you would like to resume that game.
- Inputting `h` will allow you to see previous moves that have been
  played. You will be prompted for how many turns ago you want to view.
  Press `enter` to repeatedly step one move ahead, or `e` to exit back
  to play mode.

### ✨ New in Version 2.1
* You can now save the game by typing `s`. This will create a save
  file named `saved_game.txt`. See the [Additional Features](#additional-features)
  section for more information!
* You can now see previous moves that have been played by typing `h`.
  These will be displayed in place on the board. You will be prompted
  for how many turns ago you want to view. Press `enter` to repeatedly
  step one move ahead, or `e` to exit back to play mode.

#### Older Changelog
* v2.0
  * Do you have a Tic Tac Toe AI of your own? Now you can challenge my
  AI with yours! See the [Dueling AIs Mode](#dueling-ais-mode)
  section for more information!
* v1.1
  * The game will now be played on a single game board instead of 
  printing a new board after each turn. This can be turned off 
  with the command line argument `-e` or `-eraseModeOff`.
