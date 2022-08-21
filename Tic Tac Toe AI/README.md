# Tic-Tac-Toe  
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Tic%20Tac%20Toe/sampleBoardOutput.png" alt = "sample board" width="30%" align = "right">  

(This is not a Game Pigeon game, but it is similar enough to my other AI's ([Connect 4](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Connect%204%20AI) and [Gomoku](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Gomoku%20AI)) in terms of implementation, so I decided to code it up real quick)  

### The Basics  
In Tic-Tac-Toe, the objective is to get 3 of your pieces in a row on the board, in any direction.  
### How to use  
First, download `tictactoe_client.py` and `strategy.py` files and place them both in the same directory. You can invoke the tool by running  
```
> python3 tictactoe_client.py
```
Once you do this, you will be asked whether you want to play as `X` or `O`.  

Whoever is `X` will go first. Your pieces will be colored <span style="color:lightgreen">green</span>, and the AI's pieces will be colored <span style="color:red">red</span>. If it is your turn, you will enter the name of the spot you want to play (e.g. `B2`). Then, you will be prompted to press `enter` to have the A.I. play its best move. At any point, if you want to quit, you can simply type `q` as your move input.

### How it works
The A.I. works by using a move selection algorithm known as [Minimax](https://en.wikipedia.org/wiki/Minimax), and uses a pruning technique known as [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning). Minimax works by assuming that the opponent will make the best possible move at each turn. By doing this, the A.I. can look several moves ahead. Then, it can pick the best possible outcome.  

Alpha-Beta pruning works by keeping track of the best already explored option along the path to the root for the maximizer (alpha), and the best already explored option along the path to the root for the minimizer (beta). A good explanatory video can be found [here](https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013).


### ✨ New in Version 1.1  
* The game will now be played on a single game board instead of printing a new board after each turn. This can be turned off with the command line argument `-e` or `-eraseModeOff`.
