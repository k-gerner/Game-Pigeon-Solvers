# Notes as I go (for version control)  
3.27.21: 8:10pm
- runs, seemingly computes best move, but is slow
- zobrist table reimplemented but does not carry over across depth increases, so could be better
- after implementing improved board evaluation functions
- added colors for the game pieces (always on, maybe add color-mode option later)
- changed the client file a bit to make playerColor global and expanded printBoard function
- code needs to be cleaned up for comments and extra unnecessary functions
- changed getValidMoves to only include spots in center and spots within 4 of other pieces
- before further improving the valid moves function (if I do this it should speed up the runtime)