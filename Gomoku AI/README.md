# Notes as I go (for version control)  
3.28.21: 2:41am
- runs, seemingly computes best move, but is slow in depths > 2
- zobrist table reimplemented but does not carry over across depth increases, so could be better
- after implementing improved board evaluation functions
- added colors for the game pieces (always on, maybe add color-mode option later)
- code needs to be cleaned up for comments and extra unnecessary functions
- changed getValidMoves to only include spots in center and spots within a certain distance of other pieces
- before further improving the valid moves function (if I do this it should speed up the runtime)
- added a slight highlight to the most recently played piece when printing the game board