# Game Pigeon Solvers  
Created by Kyle Gerner  
### What is this?  
This repo contains tools that will make it easy to win at the Game 
Pigeon games specified. You'll be practically unbeatable! For a brief 
overview of each game, and the features of the AI that I've built for 
it, see the [Overview][Overview section]  
section.
### What is Game Pigeon?
[Game Pigeon][GamePigeon Wikipedia] is a mobile gaming app for iOS 
devices. The app allows iMessage users to play each other in mini-games 
such as chess, mancala, anagrams, battleship and more.  

### Why did I make this?
My friend and I are pretty competitive, and one way we compete is in 
these Game Pigeon games. Each game we bet $1 on the outcome. Some of 
these games rely on strategy and recognition, which means you can 
write programs to give you the upper hand.  

The first program I wrote was for the [Anagrams][Anagrams Directory] 
game, back in February 2020. After that, I wrote the Java version of 
the solver for the avalanche mode in [Mancala][Mancala Avalanche Directory], 
shortly followed by the Python version. Next, I wrote the [Word Hunt][Word Hunt Directory] 
tool in February 2021. I also wrote the [Word Bites][Word Bites Directory] 
tool and [Connect 4 A.I.][Connect 4 Directory] 
in March 2021. I wrote the [Gomoku A.I.][Gomoku Directory] 
over the course of a few months from March to May 2021. This was by 
far the most complex project out of all of these, and it is easily 
the one I am most proud of. I also quickly coded a [Tic-Tac-Toe A.I.][Tic Tac Toe Directory] 
one night in June since it was essentially just a watered-down version 
of the Connect 4 and Gomoku AIs. In August and September 2021, my 
friend and I started playing Sea Battle (a Battleship spin-off), so 
naturally, I had to quickly write a [Sea Battle A.I.][Sea Battle Directory] 
to gain the upper hand. Then, in July 2022, we started playing Othello. 
As you can probably guess, I made an [Othello A.I.][Othello Directory] 
too. In late 2022, we started playing Mancala (Capture mode). I of course 
had to write a [Mancala Capture A.I.][Mancala Capture Directory].


Whenever we start competing in a new game, you'll see a new A.I. pop 
up in this repository! ☺

---

## Overview

To start, download this project and run 
```
> python3 ai_runner.py 
```
You will be prompted to choose from the list of games. If you would like 
to quickstart into a specific game, add the `--game=[name]` flag. To find 
the `name` of a game, check the `README.md` file of the corresponding 
game.  

You will find the list of available AIs below:


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
played move. <sub>Note: may not work on all CLIs </sub>
- Save state functionality for if you want to exit the program and 
come back later 
- Ability to see all the previous moves that have been played, one by
  one, displayed on the game board.
- Progress bar will be displayed as the AI is evaluating moves
- Output to the terminal will be updated in place instead of printing 
lines and lines of output across turns. This can be disabled if you 
would like to have all output to the terminal preserved
- Modifiable AI parameters, including max AI search depth (# moves 
to look ahead), max number of moves to evaluate from each board 
state, and max neighbor distance (for determining valid moves)  

[Check it out!][Gomoku Directory]

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
pieces from enemy pieces. <sub>Note: may not work on all CLIs </sub>
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

[Check it out!][Othello Directory]

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
your next guess. <sub>Note: may not work on all CLIs </sub>
- A super beautiful colorful output of scores for each coordinate 
on the board, making use of a color gradient to distinguish the 
levels of certainty that a coordinate contains a ship (seriously, 
it's super aesthetic looking, just look at the images in the README!)
- Save state functionality for if you want to exit the program and
  come back later
- Board sizes of 8x8, 9x9, or 10x10
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!][Sea Battle Directory]

---

## 🎮 Connect 4
The objective of the game is to get 4 of your pieces to line up in 
succession. There are 7 columns for you to play, and the piece will 
be dropped to the lowest free space in the column you choose.
### 🧠 AI Features
- Minimax algorithm using Alpha-Beta Pruning
- Dueling AI functionality allows you to challenge this AI with
your own Connect 4 AI
- Save state functionality for if you want to exit the program and
  come back later
- Ability to see all the previous moves that have been played, one by
  one, displayed on the game board.
- Color-coded output on the game board to easily distinguish 
friendly pieces from enemy pieces. Includes a green coloring of 
the most recently played column, grey coloring of unavailable 
columns, and a blue border to match the classic look of the 
physical game rig. <sub>Note: may not work on all CLIs </sub>
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!][Connect 4 Directory]

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

[Check it out!][Word Hunt Directory]

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

[Check it out!][Word Bites Directory]

---

## 🎮 Mancala Capture
The classic version of Mancala. Players earn points by moving pebbles 
around the board and dropping them in their bank. You can capture your 
opponent's pebbles by landing on an empty pocket on your side of the 
board.
### 🧠 AI Features
- Minimax algorithm using Alpha-Beta Pruning
- Dueling AI functionality allows you to challenge this AI with
your own Mancala Capture AI
- Save state functionality for if you want to exit the program and
  come back later
- Ability to see all the previous moves that have been played, one by
  one, displayed on the game board.
- Color-coded output on the game board to easily distinguish 
friendly pockets from enemy pockets. <sub>Note: may not work 
on all CLIs </sub>
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!][Mancala Capture Directory]

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

[Check it out!][Mancala Avalanche Directory]

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

[Check it out!][Anagrams Directory]

--- 

## 🎮 Tic Tac Toe
On a 3x3 board, the objective is to get 3 of your pieces to line up 
in succession.
### 🧠 AI Features
- Minimax algorithm using Alpha-Beta Pruning
- Dueling AI functionality allows you to challenge this AI with
your own Tic Tac Toe AI
- Save state functionality for if you want to exit the program and
  come back later
- Ability to see all the previous moves that have been played, one by
  one, displayed on the game board.
- Color-coded output on the game board to easily distinguish 
friendly pieces from enemy pieces. <sub>Note: may not work 
on all CLIs </sub>
- Output to the terminal will be updated in place instead of 
printing lines and lines of output across turns. This can be 
disabled if you would like to have all output to the terminal 
preserved  

[Check it out!][Tic Tac Toe Directory]


[Overview section]: https://github.com/k-gerner/Game-Pigeon-Solvers#overview
[GamePigeon Wikipedia]: https://en.wikipedia.org/wiki/GamePigeon
[Anagrams Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/anagrams
[Mancala Avalanche Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/mancalaavalanche
[Word Hunt Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/wordhunt
[Word Bites Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/wordbites
[Connect 4 Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/connect4
[Gomoku Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/gomoku
[Tic Tac Toe Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/tictactoe
[Sea Battle Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/seabattle
[Othello Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/othello
[Mancala Capture Directory]: https://github.com/k-gerner/Game-Pigeon-Solvers/tree/master/mancalacapture
