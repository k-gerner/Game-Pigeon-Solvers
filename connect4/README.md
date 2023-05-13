# Connect 4 (Four in a Row)  
<img src="/images/Connect%204/sampleConnect4Board.jpeg" alt = "sample board" width="40%" align = "right">  

### The Basics  
Four in a Row is another name for Connect 4. In Connect 4, the 
objective of the game is to get four of your pieces to line up in 
succession (hence the name). The player can choose one of seven 
columns to play their piece, which is placed in the column and lands 
at the lowest open slot.
### How to use
First, download this project. If you would like to challenge
my AI with your own, see the [Dueling AIs Mode](#dueling-ais-mode)
section. If you would like to challenge the AI yourself, you can 
invoke the tool by running
```
> python3 ai_runner.py --game=connect4
```
Once you do this, you will be asked which color you want to be, RED 
(`o`) or YELLOW (`@`). Whoever is YELLOW will go first. Each empty 
space on the board is represented by a `.` in the slot. If it is 
your turn, you will enter the column number (1-7) of which column 
you want to play. Then, you will be prompted to press `enter` to 
have the A.I. play its best move.  

If you want to use this to beat someone else in Connect 4, just enter 
their moves as the `player` and then use the A.I.'s moves as your own.  

<img src="/images/Connect%204/sampleProgramBoardColor.png" alt = "sample board output" width="20%">  

### How it works  
The A.I. works by using a move selection algorithm known as [Minimax][Minimax Wikipedia], 
and uses a pruning technique known as [Alpha-Beta Pruning][AB Pruning Wikipedia]. 
Minimax works by assuming that the opponent will make the best possible 
move at each turn. By doing this, the A.I. can look several moves 
ahead. Then, it can pick the best possible outcome.  

Alpha-Beta pruning works by keeping track of the best already explored 
option along the path to the root for the maximizer (alpha), and the 
best already explored option along the path to the root for the 
minimizer (beta). A good explanatory video can be found [here][AB Pruning Youtube].

### Dueling AIs Mode
Do you have your own Connect 4 AI? Challenge mine! This program
includes the ability for you to challenge it with a rival AI. To
use this functionality, copy your AI strategy file to the `external/aiduel` 
directory, and include a command line argument `-d` or `-aiDuel` 
followed by the name of your Python file. For example, if
your AI was located in `external/aiduel/myAiFile.py`, you would run:
```
> python3 ai_runner.py --game=connect4 -d myAiFile
```

In order for your AI to be eligible, it must meet a few requirements:
* AI logic must be contained in a class named `Connect4Strategy`
* AI must be a subclass of `Connect4Player`, found in `connect4_player.py`
* AI must have a function named `getMove` that accepts a game board
as a parameter, and returns the chosen move as an `int` representing 
the index of the column (0-6)

### Additional Features 
- Save the game by typing `s`. This will create a save
  file named `connect4_save.txt` which contains save data for the current
  game state. When you start a new game, if a save state is detected,
  you will be asked if you would like to resume that game.
- Inputting `h` will allow you to see previous moves that have been
  played. You will be prompted for how many turns ago you want to view.
  Press `enter` to repeatedly step one move ahead, or `e` to exit back
  to play mode.

### ✨ New in Version 2.1
* You can now save the game by typing `s`. This will create a save
  file named `connect4_save.txt`. See the [Additional Features](#additional-features)
section for more information!
* You can now see previous moves that have been played by typing `h`.
  These will be displayed in place on the board. You will be prompted
  for how many turns ago you want to view. Press `enter` to repeatedly
  step one move ahead, or `e` to exit back to play mode.
* At the end of the game, the average time taken per move will be
  displayed for each player.

#### Older Changelog
* v2.0
  * Do you have a Connect 4 AI of your own? Now you can challenge my
    AI with yours! See the [Dueling AIs Mode](#dueling-ais-mode)
    section for more information!
* v1.1
  * The game will now be played on a single game board instead of 
  printing a new board after each turn. This can be turned off with 
  the command line argument `-e` or `-eraseModeOff`.
  * The column number of the most recently played move will be 
  colored green.
  * The column numbers of columns that are full will be colored grey.

[Minimax Wikipedia]: https://en.wikipedia.org/wiki/Minimax
[AB Pruning Wikipedia]: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
[AB Pruning Youtube]: https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013
