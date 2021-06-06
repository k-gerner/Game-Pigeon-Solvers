# Tic-Tac-Toe  
<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Tic%20Tac%20Toe/sampleBoardOutput.png" alt = "sample board" width="40%" align = "right">  

(This is not a Game Pigeon game, but it is similar enough to my other AI's ([Connect 4](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Connect%204%20AI) and [Gomoku](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Gomoku%20AI)) in terms of implementation, so I decided to code it up real quick)  

### The Basics  
In Tic-Tac-Toe, the objective is to get 3 of your pieces in a row on the board, in any direction.  
### How to use  
First, download `tictactoe_client.py` and `strategy.py` files and place them both in the same directory. You can invoke the tool by running  
```
> python3 tictactoe_client.py
```
Once you do this, you will be asked whether you want to play as `X` or `O` (`X` will go first).  

Next, you will be prompted about which display mode you would like to use: `Diagram Mode`, or `List Mode`. Typing `i` will give you more information about each of them. Your pieces will be colored <span style="color:lightgreen">green</span>, and the AI pieces will be colored <span style="color:red">red</span>. If it is your turn, you will enter the name of the spot you want to play (e.g. `B2`). Then, you will be prompted to press `enter` to have the A.I. play its best move. At any point, if you want to quit, you can simply type `q` as your move input.
