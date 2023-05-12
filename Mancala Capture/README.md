# Mancala (Capture)
<img src="/Images/Mancala%20Capture/sampleMancalaBoard.jpeg" alt = "Mancala game board in Game Pigeon's UI" width="40%" align = "right">  

### The Basics
Mancala Capture is a version of Mancala. Players each have 6 pits 
and a bank. Each pit starts out with a certain number of pieces. 
The objective of the game is to end up with more pieces in your bank 
than your opponent. To play your turn, you choose a pit on your side 
of the board, and pick up all the pieces in that pit. You go down the 
board, placing one piece in each pit that you pass. You place pieces 
in your bank, but not your opponent's. If your last piece from that 
turn ends in your bank, you get another turn. If the last piece ends 
in an empty pit on your side, and there are pieces in the mirrored pit 
on your opponent's side, you earn every piece from your opponent's pit, 
and send them all to your bank. If you end in a non-empty pit, your turn 
is over. For further explanation, see [this website][How to play Mancala GP].  

### How to use
First, download the files in this folder. The contents of each file 
are as follows:
* `board_functions.py`: Contains basic functions for evaluating the 
state of the board
* `constants.py`: Constants relevant to the board setup and terminal output.
You can modify some of these values.
* `mancala_client.py`: Contains the logic for the UI and user input, as 
well as the game runner
* `Player.py`: Super class that players must implement. If you choose to
use your own A.I., you must inherit from this class
* `strategy.py`: Contains the A.I. strategy logic

You can invoke the tool by running
```
> python3 mancala_client.py
```
Once you do this, you will see some info about how to interact with the 
tool, further explained in the [Gameplay Features](#gameplay-features) section. 
You will be asked if you would like to go first. By default, your pockets 
will be displayed on the left side in green, with your bank at the bottom. 
You will then be prompted to either enter your move, or press `enter` for the
A.I. to play.

<img src="/Images/Mancala%20Capture/mancalaCaptureBoardOutput.png" alt = "Mancala board output" width="40%" align = "left">

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

### Gameplay Features
At the input prompt, you can enter one of several commands.
#### Save the game: `s`
Save the game by typing `s`. This will create a save file named
`saved_game.txt` which contains save data for the current game state.
When you start a new game, if a save state is detected, you will be
asked if you would like to resume that game. 
#### See previous moves: `h`
Inputting `h` will allow you to see previous moves that have been 
played. You will be prompted for how many turns ago you want to view. 
Press `enter` to repeatedly step one move ahead, or `e` to exit back 
to play mode.
#### Quit: `q`
Inputting `q` will quit the game. 

### Dueling AIs Mode
Do you have your own Mancala Capture AI? Challenge mine! This program
includes the ability for you to challenge it with a rival AI. To
use this functionality, include a command line argument `-d` or
`-aiDuel` followed by the name of your Python file. For example, if
your AI was located in `myAiFile.py`, you would run:
```
> python3 mancala_client.py -d myAiFile
```

In order for your AI to be eligible, it must meet a few requirements:
* AI logic must be contained in a class named `Strategy`
* AI must be a subclass of `Player`, found in `Player.py`
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

[How to play Mancala GP]: https://allthings.how/how-to-play-mancala-on-imessage/
[Minimax Wikipedia]: https://en.wikipedia.org/wiki/Minimax
[AB Pruning Wikipedia]: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
[AB Pruning Youtube]: https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013