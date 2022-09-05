# Othello
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Othello/sampleOthelloBoard.jpg" alt = "Othello game board in Game Pigeon's UI" width="30%" align = "right">  

### The Basics
The overall objective of the game is to end the game with more pieces 
on the board than the opponent. Each turn, a player will play one 
piece. A player can only play a piece in spaces that trap enemy 
pieces between this new piece, and an existing friendly piece on the 
board, with no empty spaces in between. The enemy pieces between this 
new piece and the nearest existing friendly piece are "captured," and 
converted to friendly pieces. This applies in any direction 
(horizontal, vertical, diagonal).    

Note: In Game Pigeon, this game is labeled as "Reversi." However, the 
rules used are actually the rules for Othello, which is why this A.I. 
is for Othello instead of Reversi.

### How to use  
First, download the files in this folder. The contents of each file are as follows:  
* `OthelloClient.py`: Contains the logic for the UI and user input, as 
well as the game runner
* `strategy.py`: Contains the A.I. strategy logic, as well as some 
functions for manipulating a game board
* `config.json`: Contains constants that affect the A.I. logic, 
accessibility settings, and more. More information in the [Configuration](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Othello#configuration) section.
* `README.md`: You're reading it right now!  

You can invoke the tool by running 
```
> python3 OthelloClient.py
```
Once you do this, you will see some info about how to interact with the 
tool, further explained in the [Additional Features](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Othello#additional-features) section. 
You will be asked if you would like to see the rules, and then you will 
be prompted to choose which color you want to be, BLACK (`0`) or WHITE 
(`O`). Whoever is BLACK will go first. You will then be prompted to 
either enter your move, or press `enter` for the A.I. to play.  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Othello/othelloGameBoard.png" alt = "sample board output" width="40%">  

### How it works
The A.I. works by using a move selection algorithm known as [Minimax](https://en.wikipedia.org/wiki/Minimax), 
and uses a pruning technique known as [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). 
Minimax works by assuming that the opponent will make the best 
possible move at each turn. By doing this, the A.I. can look several 
moves ahead. Then, it can pick the best possible outcome.

Alpha-Beta pruning works by keeping track of the best already explored 
option along the path to the root for the maximizer (alpha), and the 
best already explored option along the path to the root for the 
minimizer (beta). A good explanatory video can be found [here](https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013).  

The A.I. evaluates board states by looking at the positions of pieces 
on the board. Spaces in the corners and edges are weighted positively 
(especially the corners), whereas spaces that are one space inside 
the edge are weighted negatively. All other coordinates are weighted 
neutrally. The A.I. also keeps track of the number of full (or 
almost full) rows/columns/diagonals for each color. Additionally, 
the number of pieces each player has is taken into account, but only 
late in the game (<15 moves remaining). As the end of the game gets 
closer, the weight attributed to the number of pieces increases 
exponentially. 

It may be surprising that the A.I. doesn't prioritize more pieces 
earlier in the game. The reason for this is because, in the 
early/mid-game, it is more important to have available moves than it 
is to have more pieces. When playing against this A.I., you may 
notice that you will often have many more pieces than the A.I. does, 
up until only about 10 moves remain. It is worth noting that this 
metric could be employed to make a decent heuristic to evaluate 
boards, however I chose not to implement this in order to hopefully 
save some time when evaluating board states.  

### Configuration  

I chose to implement a (hopefully) more straightforward way of modifyi
ng the constants used for the A.I. and game rules. The `config.json` 
file contains the default values for these constants, as well as a 
brief explanation of what each constant represents, and the suggested 
values. Edit this file if you want to modify any of the settings. The 
modifiable settings are:  
* `aiMaxSearchDepth`: The maximum moves ahead the AI will look to 
determine its move. Recommended: 5-7
* `aiMaxValidMovesToEvaluateEachTurn`: The maximum moves that the AI 
will consider. Smaller numbers will be faster but may cause the AI to 
miss the best move. Recommended: 12-20
* `boardDimension`: The height/width of the board. Recommended: 8
* `colorblindMode`: Use Blue/Orange instead of Green/Red for piece colorings
* `eraseMode`: Condense the output into a single, self-updating game 
board (instead of printing out the game board and instructions on 
new lines each move)

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Othello/colorblindGameBoard.png" alt = "colorblind board output" width="40%">

### Additional Features
At the input prompt, you can enter one of several commands.
#### Save the game: `s`
Save the game by typing `s`. This will create a save file named
`saved_game.txt` which contains save data for the current game state.
When you start a new game, if a save state is detected, you will be
asked if you would like to resume that game. 
#### See previous moves: `h`
When it is your turn, inputting `h` will allow you to see previous 
moves that have been played. You will be prompted for how many turns 
ago you want to view. Press `enter` to repeatedly step one move 
ahead, or `e` to exit back to play mode.
#### Quit: `q`
Inputting `q` will quit the game.  

### Dueling AIs Mode
Do you have your own Othello AI? Challenge mine! This program
includes the ability for you to challenge it with a rival AI. To
use this functionality, include a command line argument `-d` or
`-aiDuel` followed by the name of your Python file. For example, if
your AI was located in `myAiFile.py`, you would run:
```
> python3 OthelloClient.py -d myAiFile
```

In order for your AI to be eligible, it must meet a few requirements:
* AI logic must be contained in a class named `OthelloStrategy`
* AI must be a subclass of `Player`, found in `Player.py`
* AI must have a function named `getMove` that accepts a game board
  as a parameter, and returns the chosen move coordinates in the form of
  a tuple in the format `(rowNumber, columnNumber)`

### ✨ New in Version 2.0
* Do you have an Othello 4 AI of your own? Now you can challenge my
  AI with yours! See the [Dueling AIs Mode](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Othello%20AI#dueling-ais-mode)
  section for more information!
* Saving the game is now much more streamlined. The save state will
now be written to a text file. When you start a new game, if a save
state is detected, you will be asked if you would like to resume that
game.

\
\
\
\
If you made it this far, you should check out my other A.I.s and 
solvers! I'm especially proud of my [Gomoku A.I.](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Gomoku%20AI)!