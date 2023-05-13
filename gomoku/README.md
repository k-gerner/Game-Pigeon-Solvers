# Gomoku
<img src="/images/Gomoku/sampleGomokuBoard.jpg" alt = "sample board" width="30%" align = "right">  

### Table of contents
1. [The Basics](#the-basics)  
2. [How to use](#how-to-use)  
3. [Features](#features)  
4. [How it works](#how-it-works)  
     i. [Minimax and Alpha-Beta Pruning](#minimax-and-alpha-beta-pruning)  
     ii. [Zobrist Hashing and Transposition Tables](#zobrist-hashing-and-transposition-tables)  
     iii. [Determining valid moves](#determining-valid-moves)  
     iv. [Iterative Deepening and evaluating board states](#iterative-deepening-and-evaluating-board-states) 
5. [Dueling AIs Mode](#dueling-ais-mode)
6. [Further Reading](#further-reading)  

### The Basics 
In Gomoku, the objective is to get 5 of your pieces to line up in 
succession. The player can choose any spot on the board to play 
their piece. Each player places one piece per turn. One easy way 
to think of this is that it is basically Tic-Tac-Toe, except it is 
played on a much bigger board, and you need 5 pieces in a row to 
win instead of 3.

### How to use 
First, download this project. If you would like to challenge
my AI with your own, see the [Dueling AIs Mode](#dueling-ais-mode)
section. If you would like to challenge the AI yourself, you can 
invoke the tool by running  
```
> python3 ai_runner.py --game=gomoku
```
Once you do this, you will be asked how big you want the board to 
be. This number should be an odd number. By default, the board is 
13x13. Next, you will be asked which color you want to be (black 
or white). Whoever is black will go first. Each empty space on 
the board is represented by a `.` in the slot. Black and white 
will be represented by `X` and `O` respectively. Your pieces will 
be colored <span style="color:lightgreen">green</span>, and the 
AI pieces will be colored <span style="color:red">red</span>. If 
it is your turn, you will enter the name of the spot you want to 
play (e.g. `E7`). Then, you will be prompted to press `enter` to 
have the A.I. play its best move. At any point, if you want to 
quit, you can simply type `q` as your move input.

If you want to use this to beat someone else in Gomoku, just enter 
their moves as the `player` and then use the A.I.'s moves as your own.  

There is some customization available as well. Inside of `gomoku_strategy.py` 
you can change certain parameters that will change how the A.I. finds 
the best move:
- `MAX_NEIGHBOR_DIST` - This parameter is the maximum distance from 
other pieces that the A.I. should consider as valid moves. This 
helps cut down on the number of moves it has to check. By default, 
this value is set to `2` since there are hardly any situations 
where you would want to play far away from any other pieces on the 
board.  
- `MAX_NUM_MOVES_TO_EVALUATE` - This parameter is the maximum 
number of moves the A.I. should consider at once. This also helps 
cut down on the number of moves it has to check. The A.I. works by 
making an educated guess for which spots are likely to have a good 
outcome, before manually checking the selected spots. Because this 
is just an educated guess, it could be wrong, so a larger number 
increases the odds that it will check the best move. However, a 
larger number will also increase the amount of time that it takes 
to search for the best move. By default, this value is set to `15`.  
- `MAX_DEPTH` - This parameter is the number of moves the A.I. 
should look ahead. A higher number means that the A.I. will look 
further in the future, and thus may be able to make a better move. 
However, a larger number will also cause the search to take longer. 
By default, this value is set to `6`. I will show you about how 
long each search takes on my 2015 Macbook Pro at depths 4, 5, and 6:
    - `MAX_DEPTH = 4` &#8594; `2s`  
    - `MAX_DEPTH = 5` &#8594; `8s`  
    - `MAX_DEPTH = 6` &#8594; `30s`  

<img src="/images/Gomoku/gomokuStartingPrompts.png" alt = "starting prompts" width="40%" align = left>  
<img src="/images/Gomoku/gomokuBoardOutput.png" alt = "sample board output" width="20%">  
  
### Features 
- As mentioned above, you can change several parameters to fine-tune the A.I. yourself. 
For more information about that, see the bottom of the [How to use](#how-to-use) section. 
- Save the game by typing `s`. This will create a save file named 
`gomoku_save.txt` which contains save data for the current game state. 
When you start a new game, if a save state is detected, you will be 
asked if you would like to resume that game.
- Inputting `h` will allow you to see previous moves that have been
  played. You will be prompted for how many turns ago you want to view.
  Press `enter` to repeatedly step one move ahead, or `e` to exit back
  to play mode.
- Do you have a Gomoku AI of your own? Try out Dueling AIs mode! See
  the [Dueling AIs Mode](#dueling-ais-mode) section for more
  information!
- The board will update in place by default. If you instead would like
  a new board to be printed after each move, you can add the command
  line argument `-e` or `-eraseModeOff`.
- Each move on the board is color-coded to make it easier to 
distinguish between friendly and enemy pieces.
- The most recently played move is highlighted slightly grey.
- Once the A.I. chooses a move, there are two things printed out:
  - `Time taken` - How long it took the A.I. to calculate its best move.
  - `AI played in spot __` - Says which spot on the board the A.I. just played.
- During the A.I. evaluation, a progress bar is shown for each 
depth of the search. This will display how far along the A.I. is 
with calculating the best move by giving a percentage as well as 
a fraction. It will also show you which depth it is currently 
searching.
<img src="/images/Gomoku/gomokuProgressBar.png" alt = "progress bar" width="50%">

### How it works  
#### Minimax and Alpha-Beta Pruning
The A.I. works by using a move selection algorithm known as [Minimax][Minimax Wikipedia], 
and uses a pruning technique known as [Alpha-Beta Pruning][AB Pruning Wikipedia]. 
Minimax works by assuming that the opponent will make the best possible move 
at each turn. By doing this, the A.I. can look several moves ahead. Then, it 
can pick the best possible outcome for itself.  

Alpha-Beta pruning works by keeping track of the best already 
explored option along the path to the root for the maximizer 
(alpha), and the best already explored option along the path to 
the root for the minimizer (beta). A good explanatory video can 
be found [here][AB Pruning Youtube]. 
With Alpha-Beta pruning, we can significantly cut down on the 
number of board states that we have to evaluate.

#### Zobrist Hashing and Transposition Tables
Another method I used to speed up the algorithm was a technique 
known as [Zobrist Hashing][Zobrist Hashing Wikipedia]
in conjunction with [Transposition Tables][Transposition Tables Wikipedia]. 
Zobrist Hashing is essentially a way to represent a state of the 
board with a unique hash value. We create a `key` value for each 
position on the board for each player color. For a given board 
state, we look at each space with a piece on it, get all the keys 
for those pieces, and then use the `XOR` operation on all of them 
together. The result will be the unique hash value for that board 
state. We will map this value to the score that we have evaluated 
for this board state. This means that if we ever see this same 
board later in the search, we do not have to recalculate the score 
for it, since we already have it stored. Here is an example where 
this may be useful:

Say we have two players playing on a 3x3 board. Let's denote the 
spaces as `A`, `B`, ... `I`. Say we are evaluating the board after 
the following sequence:  

- P1 turn 1: `A`  
- P2 turn 1: `B`  
- P1 turn 2: `C`  
- P2 turn 2: `D`  
- P1 turn 3: `E`  
- P2 turn 3: `F`  

Let's say the hash value for this board after 6 moves is 74032. 
Note that we will also be storing hash values for this board after 
depths 3, 4, and 5. Let's also assume that this board is deemed 
the best possible outcome for after P1's second turn. In other 
words, if we have the board where P1 is in spots `A` and `C`, and 
P2 is in spot `B`, then the "best" board outcome for `depth = 6` 
would be where P1 is also in `E`, and P2 is also in `D` and `F`. 
Now let's look at a different sequence:  

- P1 turn 1: `C`  
- P2 turn 1: `B`  
- P1 turn 2: `A`  
- P2 turn 2: `F`  
- P1 turn 3: `E`  
- P2 turn 3: `D`  

Notice that these two boards have the pieces played in the same 
spots, but they were played in a different order. The hash value 
for the second board will also be 74032, so instead of having to 
recalculate the score of the board (which takes a relatively long 
time), we can just look up the hash value in the transposition 
table, and get the score from there. **However**, we actually 
wouldn't even need to look past P1's second move. As stated 
earlier, we have already found and evaluated the best board for 
when P1 is in `A` and `C`, and P2 is in `B`. The score of the best 
board-state after these 3 moves would have been stored in the 
transposition table. Therefore, after P1's second turn, since the 
hash value has already been stored and mapped to the score of the 
best possible board, once we see that positions `A` and `C` are 
filled by P1 and `B` is filled by P2, we can stop traversing 
further down the move tree, and simply return the score that we 
have already found. This saves a huge amount of time, since each 
level down the tree has exponentially more possible board-states 
than the previous level.  

#### Determining valid moves
The next way to cut down on the execution time would be to decrease 
the number of spaces that we have to include in our search. How do 
we determine whether a move is valid in Gomoku? The naive approach 
would be to consider every empty space on the board as a valid move. 
While this is technically correct, there are certain spots that 
don't need to be considered. This approach may be feasible for a 
game like Tic-Tac-Toe which has 9 spaces. For example, there would 
be 9 * 8 * 7 = 392 possible sequences for the first 3 moves. 
However, Gomoku requires some more thought, since it has a much 
bigger board, meaning for a 13x13 board, there would be 4,741,464 
possible sequences for the first 3 moves.  

The first approach I took to narrowing the search area was to only 
include spots that were within 2 spaces of an already-played space. 
This significantly cut down the search area at the beginning of 
the game, but after a few moves the search area could easily include 
90 to 100 spaces.  

To fix this, I figured that I would have to somehow choose the 
spaces that I thought were *likely* to produce a good outcome. One 
might think that in order to do this, I should evaluate the board 
after testing each of these moves, and then choose the highest 
scoring moves from there to look further. Probably the biggest issue 
with that is that evaluating the entire board takes a long time. I 
have to look at every single 5 or 6 piece section on the board 
(horizontal, vertical, and both diagonal directions), see if it 
contains a sequence I have deemed as a "threat sequence," and then 
sum up the scores for all of them.  

I didn't want to waste all that time evaluating the entire board 
with each possible valid move, so I decided to take a more detailed 
approach to determine how likely a move was to give me a good 
outcome in the future. To do this, I looked at the area around 
each valid move. At most, I would look at the 9x9 square 
surrounding the valid move. I evaluated all four directions 
(horizontal, vertical, and both diagonal directions), and used 
that information to give each valid move a heuristic score. Some 
things I looked for were how many pieces of my color were in each 
4-deep direction before reaching an enemy piece or the board border, 
how many empty spaces there were, if there were any traps that could 
be a result of this move being played, etc. By tweaking the weight 
assigned to each characteristic, I was able to achieve a fairly 
accurate group of the most promising locations on the board. This 
allowed me to decrease the number of moves I needed to check by a 
great amount, since I only chose the top 15 valid moves from this.  

#### Iterative Deepening and evaluating board states
After getting my final list of valid moves for a given board, I was 
able to use the Minimax algorithm to check the possible board states 
`d` moves ahead. In order to prioritize moves that would lead to a 
win sooner rather than later, I implemented 
[Iterative Deepening][Iterative Deepening Wikipedia], 
which allowed me to perform searches at each depth `d` from `1` to 
`MAX_DEPTH`. Once I reached the maximum depth for a given `d`, I had 
to evaluate the entire board. As I mentioned before, to do this I 
had to look at every single 5 or 6 piece section on the board 
(horizontal, vertical, and both diagonal directions) and give the 
board an evaluation score. This was a costly operation, so the fewer 
boards I have to evaluate, the better.  

One helpful tool I used to determine which sections of my code needed 
to be improved was a profiler. By running `python3 -m cProfile -s time ai_runner.py --game=gomoku`, 
I could see which methods were taking up the most time, and how many 
times they were called.  

### Dueling AIs Mode
Do you have your own Gomoku AI? Challenge mine! This program
includes the ability for you to challenge it with a rival AI. To
use this functionality, copy your AI strategy file to the `external/aiduel` 
directory, and include a command line argument `-d` or `-aiDuel` 
followed by the name of your Python file. For example, if
your AI was located in `external/aiduel/myAiFile.py`, you would run:
```
> python3 ai_runner.py --game=gomoku -d myAiFile
```

In order for your AI to be eligible, it must meet a few requirements:
* AI logic must be contained in a class named `GomokuStrategy`
* AI must be a subclass of `GomokuPlayer`, found in `gomoku_player.py`
* AI must have a function named `getMove` that accepts a game board
  as a parameter, and returns the chosen move coordinates in the form of
  a tuple in the format `(rowNumber, columnNumber)`


#### Any more questions?
Any further clarification that is needed can come from viewing the 
code. I was pretty liberal with my use of comments that describe 
certain sections of the code that may be complicated, so those 
should provide some clarification.  
  
### Further reading
#### Transposition Tables
https://stackoverflow.com/questions/20009796/transposition-tables  
https://stackoverflow.com/questions/29990116/alpha-beta-prunning-with-transposition-table-iterative-deepening  
https://ai.stackexchange.com/questions/8403/transposition-table-is-only-used-for-roughly-17-of-the-nodes-is-this-expected  
http://blog.gamesolver.org/solving-connect-four/07-transposition-table/  

#### Zobrist Hashing  
https://levelup.gitconnected.com/zobrist-hashing-305c6c3c54d0  

#### General strategy and Miscellaneous
https://stackoverflow.com/questions/6952607/what-would-be-a-good-ai-strategy-to-play-gomoku  
https://webdocs.cs.ualberta.ca/~mmueller/courses/2014-AAAI-games-tutorial/slides/AAAI-14-Tutorial-Games-3-AlphaBeta.pdf  
https://medium.com/@LukeASalamone/creating-an-ai-for-gomoku-28a4c84c7a52

### ✨ New in Version 2.1
* You can now see previous moves that have been played by typing `h`. 
These will be displayed in place on the board. You will be prompted 
for how many turns ago you want to view. Press `enter` to repeatedly 
step one move ahead, or `e` to exit back to play mode.
* At the end of the game, the average time taken per move will be
  displayed for each player.

#### Older Changelog
* v2.0
  * Do you have a Gomoku AI of your own? Now you can challenge my
      AI with yours! See the [Dueling AIs Mode](#dueling-ais-mode)
      section for more information!
  * Saving the game is now much more streamlined. The save state will
    now be written to a text file. When you start a new game, if a save
    state is detected, you will be asked if you would like to resume that
    game.
* v1.1
  * The game will now be played on a single game board instead of 
  printing a new board after each turn. This can be turned off with 
  the command line argument `-e` or `-eraseModeOff`.
  * Printing the current save state will now be invoked with `s` 
  instead of `p`. Also, the output is now less verbose.

Thanks for checking out my Gomoku AI! I hope you enjoy!  

[Minimax Wikipedia]: https://en.wikipedia.org/wiki/Minimax
[AB Pruning Wikipedia]: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
[AB Pruning Youtube]: https://www.youtube.com/watch?v=xBXHtz4Gbdo&ab_channel=CS188Spring2013
[Zobrist Hashing Wikipedia]: https://en.wikipedia.org/wiki/Zobrist_hashing
[Transposition Tables Wikipedia]: https://en.wikipedia.org/wiki/Transposition_table
[Iterative Deepening Wikipedia]: https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
