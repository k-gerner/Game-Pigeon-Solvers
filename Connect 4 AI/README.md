# Connect 4 (Four in a Row)  
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Connect%204/sampleConnect4Board.jpeg" alt = "sample board" width="40%" align = "right">  

### The Basics  
Four in a Row is another name for Connect 4. In Connect 4, the objective of the game is to get four of your pieces to line up in succession (hence the name). The player can choose one of seven columns to play their piece, which is placed in the column and lands at the lowest open slot.
### How to use
First, download the `connect4_client.py` and `strategy.py` files and place them both in the same directory. You can invoke the tool by running  
```
> python3 connect4_client.py
```
Once you do this, you will be asked which color you want to be, RED (`o`) or YELLOW (`@`). Whoever is YELLOW will go first. Each empty space on the board is represented by a `.` in the slot. If it is your turn, you will enter the column number (1-7) of which column you want to play. Then, you will be prompted to press `enter` to have the A.I. play its best move.  

If you want to use this to beat someone else in Connect 4, just enter their moves as the `player` and then use the A.I.'s moves as your own.  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Connect%204/sampleProgramBoardColor.png" alt = "sample board output" width="20%">  

### How it works  
The A.I. works by using a move selection algorithm known as [Minimax](https://en.wikipedia.org/wiki/Minimax), and uses a pruning technique known as [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). Minimax works by assuming that the opponent will make the best possible move at each turn. By doing this, the A.I. can look several moves ahead. Then, it can pick the best possible outcome.  

Alpha-Beta pruning works by keeping track of the best already explored option along the path to the root for the maximizer (alpha), and the best already explored option along the path to the root for the minimizer (beta). A good explanatory video can be found [here](https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013).