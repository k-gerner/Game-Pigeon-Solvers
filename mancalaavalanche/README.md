# Mancala (Avalanche)  

<img src="/images/Mancala%20Avalanche/sampleMancalaBoard.jpeg" alt = "sample board" width="40%" align = "right"> 

### The Basics  
Mancala Avalanche is a version of Mancala. Players each have 6 pits 
and a bank. Each pit starts out with a certain number of pieces. 
The objective of the game is to end up with more pieces in your bank 
than your opponent. To play your turn, you choose a pit on your side 
of the board, and pick up all the pieces in that pit. You go down the 
board, placing one piece in each pit that you pass. You place pieces 
in your bank, but not your opponent's. If your last piece from that 
turn ends in your bank, you get another turn. If the last piece ends 
in another pit, you pick up every piece from that pit, and repeat 
the process (unless the pit was empty, in which case your turn is 
over). For further explanation, see [this website][How to play Mancala GP].  

### Python Version  
*Note*: This code is likely not as optimized as it could be, as I 
wrote it as an exercise to refamiliarize myself with Python.
#### How to use
First, download this project. Then, run the following command:  
```
> python3 ai_runner --game=mancala-avalanche
```  
You will be prompted for which mode you would like to use (have the 
moves presented all at once, or one at a time). Next, you will be 
prompted to enter your side of the board (separated by spaces), 
followed by the opponent's side of the board. You will be presented 
with a visualization of the board as you have inputted it. Pressing 
enter will calculate the best possible move set for that given board. 
You will then repeat this process until the game is over, or you choose 
to quit the program.

<img src="/images/Mancala%20Avalanche/mancalaBoardOutput.png" alt = "sample board output" width = "30%">  

#### ✨ New in Version 1.1
* The output will now be updated in place, instead of printing 
* additional output to the terminal. This can be turned off with the 
* command line argument `-e` or `-eraseModeOff`.

### Java Version  
#### How to use
First, go into the [Java Version](/mancalaavalanche/java) 
directory and download the `MancalaAvalanche.java` and 
`MancalaBoard.java` files. Then, run the following command:  
```
> javac MancalaAvalanche.java
```  
This compiles the code. Once you have done this once, you won't have 
to do it again, unless you make changes to either one of the `.java` 
files. Now, to run the program, run the following command:  
```
> java MancalaAvalanche
```  
You will be prompted for which mode you would like to use (have the 
moves presented all at once, or one at a time). Next, you will be 
prompted to enter your side of the board (comma separated), followed 
by the opponent's side of the board. Make sure your input is a comma 
separated list with exactly 6 numbers. You will be presented with a 
visualization of the board as you have inputted it. Pressing enter 
will calculate the best possible move set for that given board.

[How to play Mancala GP]: https://allthings.how/how-to-play-mancala-on-imessage/
