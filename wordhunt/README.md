# Word Hunt  

<img src="/images/Word%20Hunt/sampleWordHuntBoard.jpeg" alt = "sample board" width="40%" align = "right">     

### The Basics  
In Word Hunt, players are presented with a 4x4 board of letter tiles. 
In order to earn points, players must connect adjacent tiles on the 
board to form English words. The longer the word, the more points 
the player earns. Whoever scores more points in 80 seconds wins.
### How to use
First, download this project. You can invoke the tool by running  
```
> python3 ai_runner.py --game=wordhunt
```
Once you do this, you will be prompted about the maximum word length. 
The default length is 10, which means the tool will look for words 
that are between 3 and 10 letters long, inclusive.  

Next, you will be prompted about which display mode you would like to 
use: `Diagram Mode`, or `List Mode`. Typing `i` will give you more 
information about each of them. 
#### Diagram Mode
Diagram mode will display each word one at a time, along with a 
visual representation of the board which shows the user the path 
they should take to connect the letters. Longer words will be 
displayed first.  

<img src="/images/Word%20Hunt/sampleDiagramMode2.png" alt = "sample diagram mode" width = "40%"> 
    
#### List Mode
List mode will display every possible word on the board all at once, 
along with the index on the board at which the first letter is located.
Longer words will be displayed first.  

<img src="/images/Word%20Hunt/sampleListMode.png" alt = "sample list mode" width = "40%">  

### ✨ New in Version 1.1
* The output will now be updated in place, instead of printing 
additional output to the terminal. This can be turned off with the 
command line argument `-e` or `-eraseModeOff`.
* In List mode, 10 words will be displayed at a time, instead of 
displaying all at once.
