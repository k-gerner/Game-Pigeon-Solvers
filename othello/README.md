# Othello
<img src="/images/Othello/sampleOthelloBoard.jpg" alt = "Othello game board in Game Pigeon's UI" width="30%" align = "right">  

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
First, download this project. The contents of the files for Othello
are as follows:
* `othello_client.py`: Contains the logic for the UI and user input, as 
well as the game runner
* `othello_strategy.py`: Contains the A.I. strategy logic, as well as some 
functions for manipulating a game board
* `othello_player.py`: Contains the base class for Othello Player objects
* `README.md`: You're reading it right now!  

You can invoke the tool by running 
```
> python3 ai_runner.py --game=othello
```
Once you do this, you will see some info about how to interact with the 
tool, further explained in the [Gameplay Features](#gameplay-features) section. 
You will be asked if you would like to see the rules, and then you will 
be prompted to choose which color you want to be, BLACK (`0`) or WHITE 
(`O`). Whoever is BLACK will go first. You will then be prompted to 
either enter your move, or press `enter` for the A.I. to play.  

<img src="/images/Othello/othelloGameBoard.png" alt = "sample board output" width="40%">  

### How it works
The A.I. works by using a move selection algorithm known as [Minimax][Minimax Wikipedia], 
and uses a pruning technique known as [Alpha-Beta Pruning][AB Pruning Wikipedia]. 
Minimax works by assuming that the opponent will make the best 
possible move at each turn. By doing this, the A.I. can look several 
moves ahead. Then, it can pick the best possible outcome.

Alpha-Beta pruning works by keeping track of the best already explored 
option along the path to the root for the maximizer (alpha), and the 
best already explored option along the path to the root for the 
minimizer (beta). A good explanatory video can be found [here][AB Pruning Youtube].  

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

### Gameplay Features
At the input prompt, you can enter one of several commands.
#### Save the game: `s`
Save the game by typing `s`. This will create a save file named
`othello_save.txt` which contains save data for the current game state.
When you start a new game, if a save state is detected, you will be
asked if you would like to resume that game. 
#### See previous moves: `h`
Inputting `h` will allow you to see previous moves that have been 
played. You will be prompted for how many turns ago you want to view. 
Press `enter` to repeatedly step one move ahead, or `e` to exit back 
to play mode.
#### Quit: `q`
Inputting `q` will quit the game.  

### Modifiable Parameters
If you would like to tweak the parameters of the AI, you can modify 
some of them inside of `othello_strategy.py`:
* `MAX_DEPTH`: The maximum moves ahead the AI will look to
  determine its move. Recommended: 5-8
* `MAX_VALID_MOVES_TO_EVALUATE`: The maximum moves that the AI
  will consider. Smaller numbers will be faster but may cause the AI to
  miss the best move. Recommended: 12-20
* `BOARD_DIMENSION`: The height/width of the board. Recommended: 8

### Dueling AIs Mode
Do you have your own Othello AI? Challenge mine! This program
includes the ability for you to challenge it with a rival AI. To
use this functionality, copy your AI strategy file to the `external/aiduel` 
directory, and include a command line argument `-d` or `-aiDuel` 
followed by the name of your Python file. For example, if
your AI was located in `external/aiduel/myAiFile.py`, you would run:
```
> python3 ai_runner.py --game=othello -d myAiFile
```

In order for your AI to be eligible, it must meet a few requirements:
* AI logic must be contained in a class named `OthelloStrategy`
* AI must be a subclass of `OthelloPlayer`, found in `othello_player.py`
* AI must have a function named `getMove` that accepts a game board
  as a parameter, and returns the chosen move coordinates in the form of
  a tuple in the format `(rowNumber, columnNumber)`

### Optional Command Line Arguments

* Erase mode: Condenses the output into a single, self-updating game
  board (instead of printing out the game board and instructions on
  new lines each move). This is **on** by default, but if you would 
like to **disable** this feature and preserve all output to the 
terminal, include the flag `-e` or `-eraseModeOff`.
* Dueling AIs Mode: See the [Dueling AIs Mode](#dueling-ais-mode)
section for more information. Invoked with `-d` or `-aiDuel`.  
* Colorblind mode: Use Blue/Orange instead of Green/Red for piece
  colorings. To enable, include the flag`-cb` or `-colorblindMode`.

<img src="/images/Othello/colorblindGameBoard.png" alt = "colorblind board output" width="40%">


### ✨ New in Version 2.1
* You will now be able to see the board history while in AI Duel mode.
* At the end of the game, the average time taken per move will be 
displayed for each player.

#### Older Changelog
* v2.0
  * Do you have an Othello 4 AI of your own? Now you can challenge my
      AI with yours! See the [Dueling AIs Mode](#dueling-ais-mode)
      section for more information!
  * Saving the game is now much more streamlined. The save state will
    now be written to a text file. When you start a new game, if a 
  save state is detected, you will be asked if you would like to 
  resume that game.
  * The modifiable parameters are now located in `strategy.py` instead
    of a separate JSON file. Additionally, eraseMode and colorblindMode
    are now optional command line arguments.
  * The code structure of the client has been refactored to match the
    other clients in this repository.

\
\
\
\
If you made it this far, you should check out my other A.I.s and 
solvers! I'm especially proud of my [Gomoku A.I.](/gomoku)!

[Minimax Wikipedia]: https://en.wikipedia.org/wiki/Minimax
[AB Pruning Wikipedia]: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
[AB Pruning Youtube]: https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013
