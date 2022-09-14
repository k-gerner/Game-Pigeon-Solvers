# Game Pigeon Solvers  
Created by Kyle Gerner  
### What is this?  
This repo contains tools that will make it easy to win at the Game 
Pigeon games specified. You'll be practically unbeatable! For a brief 
overview of each game, and the features of the AI that I've built for 
it, see the [Overview](https://github.com/k-gerner/Game-Pigeon-Solvers#overview) 
section.
### What is Game Pigeon?
[Game Pigeon](https://en.wikipedia.org/wiki/GamePigeon) is a mobile 
gaming app for iOS devices. The app allows iMessage users to play 
each other in mini-games such as chess, mancala, anagrams, battleship 
and more.  

### Why did I make this?
My friend and I are pretty competitive, and one way we compete is in 
these Game Pigeon games. Each game we bet $1 on the outcome. Some of 
these games rely on strategy and recognition, which means you can 
write programs to give you the upper hand.  

The first program I wrote was for the [Anagrams](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Anagrams%20Tool) 
game, back in February 2020. After that, I wrote the Java version of 
the solver for the avalanche mode in [Mancala](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Mancala%20Avalanche), 
shortly followed by the Python version. Next, I wrote the [Word Hunt](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Word%20Hunt%20Tool) 
tool in February 2021. I also wrote the [Word Bites](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Word%20Bites%20Tool) 
tool and [Connect 4 A.I.](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Connect%204%20AI) 
in March 2021. I wrote the [Gomoku A.I.](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Gomoku%20AI) 
over the course of a few months from March to May 2021. This was by 
far the most complex project out of all of these, and it is easily 
the one I am most proud of. I also quickly coded a [Tic-Tac-Toe A.I.](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Tic%20Tac%20Toe%20AI) 
one night in June since it was essentially just a watered-down version 
of the Connect 4 and Gomoku AIs. In August and September 2021, my 
friend and I started playing Sea Battle (a Battleship spin-off), so 
naturally, I had to quickly write a [Sea Battle A.I.](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Sea%20Battle) 
to gain the upper hand. Then, in July 2022, we started playing Othello. 
As you can probably guess, I made an [Othello A.I.](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Othello%20AI) 
too.  

Whenever we start competing in a new game, you'll see a new A.I. pop 
up in this repository! ☺

---

## Overview 
## 🎮 Gomoku
The objective of Gomoku is to get 5 of your pieces to line up in 
succession. You can think of it like a much more advanced version 
of Tic Tac Toe. The board is much bigger (13x13), and you need 5 
pieces in a row instead of just 3. You may be surprised how much 
strategy is involved a game of Gomoku!
### 🧠 AI Features
- Advanced Minimax algorithm using Alpha-Beta Pruning, transposition 
tables, Zobrist Hashing, Iterative Deepening, and smart 
search-space-selection
- Dueling AI functionality allows you to challenge this AI with 
your own Gomoku AI
- Color-coded output on the game board to easily distinguish friendly 
pieces from enemy pieces, including highlighting the most recently 
played move
- Save state functionality for if you want to exit the program and 
come back later 
- Progress bar will be displayed as the AI is evaluating moves
- Output to the terminal will be updated in place instead of printing 
lines and lines of output across turns. This can be disabled if you 
would like to have all output to the terminal preserved
- Modifiable AI parameters, including max AI search depth (# moves 
to look ahead), max number of moves to evaluate from each board 
state, and max neighbor distance (for determining valid moves)  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Gomoku%20AI)

---

## 🎮 Othello
The objective of Othello is to end the game with more pieces than 
your opponent. You can capture enemy pieces by trapping them between 
two friendly pieces.
### 🧠 AI Features
- Minimax algorithm using Alpha-Beta Pruning
- Dueling AI functionality allows you to challenge this AI with
your own Othello AI
- Color-coded output on the game board to easily distinguish friendly 
pieces from enemy pieces
- Valid moves will be highlighted for you before each turn
- Optional colorblind mode will use a blue/orange color scheme instead 
of green/red
- Save state functionality for if you want to exit the program and 
come back later 
- Ability to see all the previous moves that have been played, one by 
one, displayed on the game board.
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved
- Modifiable AI parameters, including max AI search depth (# moves 
to look ahead), max number of moves to evaluate from each board 
state, and board size  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Othello%20AI)

--- 

## 🎮 Sea Battle
If you've ever played Battleship, Sea Battle is the same thing. You 
take turns guessing where the opponent has their ships laid out on 
a grid. Whoever sinks all the opposing ships first wins! This AI 
assists you by showing you which locations are mathematically most 
likely to contain ships.
### 🧠 AI Features
- Color-coded output on the game board to easily distinguish misses, 
hits, and sinks. Also used to show which locations are ideal for 
your next guess
- A super beautiful colorful output of scores for each coordinate 
on the board, making use of a color gradient to distinguish the 
levels of certainty that a coordinate contains a ship (seriously, 
it's super aesthetic looking, just look at the images in the README!)
- Board sizes of 8x8, 9x9, or 10x10
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Sea%20Battle)

---

## 🎮 Connect 4
The objective of the game is to get 4 of your pieces to line up in 
succession. There are 7 columns for you to play, and the piece will 
be dropped to the lowest free space in the column you choose.
### 🧠 AI Features
- Minimax algorithm using Alpha-Beta Pruning
- Dueling AI functionality allows you to challenge this AI with
your own Connect 4 AI
- Color-coded output on the game board to easily distinguish 
friendly pieces from enemy pieces. Includes a green coloring of 
the most recently played column, grey coloring of unavailable 
columns, and a blue border to match the classic look of the 
physical game rig
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Connect%204%20AI)

---

## 🎮 Word Hunt
You are given a 4x4 grid of letters. To earn points, you connect 
adjacent letters together. This can be in any direction (horizontal, 
vertical, diagonal, and combinations of all three). You can't use 
the same tile on the grid more than once per word though!
### 🧠 AI Features
- Near-instant identification of all valid words present on the 
board up to 10 letters long
- Two output modes: Diagram Mode, and List Mode, both displaying 
words with higher values first
- Diagram mode will display the output as a grid with numbers to 
show the order and locations on the board for which you should drag 
your finger to create the word
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Word%20Hunt%20Tool)

---

## 🎮 Word Bites
Think of Scrabble, except you can play the pieces anywhere, and 
they can come in pairs (both vertical and horizontal). You earn 
points by combining letter pieces together to form words. Some 
pieces can only be played in certain orientations.
### 🧠 AI Features
- Near-instant identification of all valid words that can fit on 
the 9x8 board
- Two output modes: Diagram Mode, and List Mode, both displaying 
words with higher values first
- Diagram mode will display the output as it appears on the game 
board, whether thats in vertical or horizontal orientation
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Word%20Bites%20Tool)

---

## 🎮 Mancala Avalanche
In this version of the classic Mancala game, a player's turn doesn't 
end until they run out of pebbles in an empty pocket. Players earn 
points by moving pebbles around the board and dropping them in 
their bank.
### 🧠 AI Features
- Two different versions that accomplish the same thing: One 
written in Python (recommended), and one written in Java
- Determines the optimal move order for the current board. (Note: 
It will be practically impossible for you to lose)
- Visualization of the board after each turn that replicates what 
the actual game board looks like
- (Python version only) Output to the terminal will be updated in 
place instead of printing lines and lines of output across turns. 
This can be disabled if you would like to have all output to the 
terminal preserved  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Mancala%20Avalanche)

---

## 🎮 Anagrams
You're given 6 or 7 letters that you can arrange in any order you 
want to form words. Longer words earn you more points.
### 🧠 AI Features
- Option for either 6 or 7 letter games
- List mode displays 10 words at a time, displaying words with 
higher values first
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Anagrams%20Tool)

--- 

## 🎮 Tic Tac Toe
On a 3x3 board, the objective is to get 3 of your pieces to line up 
in succession.
### 🧠 AI Features
- Minimax algorithm using Alpha-Beta Pruning
- Dueling AI functionality allows you to challenge this AI with
your own Tic Tac Toe AI
- Color-coded output on the game board to easily distinguish 
friendly pieces from enemy pieces
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!](https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/Tic%20Tac%20Toe%20AI)
