# Word Hunt  

<img src="/images/Word%20Hunt/sampleWordHuntBoard.jpeg" alt = "sample board" width="40%" align = "right">     

### The Basics  
In Word Hunt, players are presented with a board of letter tiles. 
In order to earn points, players must connect adjacent tiles on the 
board to form English words. The longer the word, the more points 
the player earns. Whoever scores more points in 80 seconds wins.
### How to use
First, download this project. You can invoke the tool by running  
```
> python3 ai_runner.py --game=wordhunt
```
Once you do this, you will be prompted for which board layout to use. 
There are four options: 4x4 (default), 5x5, Donut, and Cross.   

<img src="/images/Word%20Hunt/board_layout_prompt.png" alt = "board layout prompt" width = "40%"> 

Next, you will be prompted about which display mode you would like to 
use: `Diagram Mode` (default), or `List Mode`. Typing `i` will give you 
more information about each of them. 
#### Diagram Mode
Diagram mode will display each word one at a time, along with a 
visual representation of the board which shows the user the path 
they should take to connect the letters. Longer words will be 
displayed first.  

<img src="/images/Word%20Hunt/sample_4x4_diagram_with_prompt.png" alt = "sample diagram mode" width = "40%"> 
    
#### List Mode
List mode will display every possible word on the board ten words at a time, 
along with the index on the board at which the first letter is located.
Longer words will be displayed first. A diagram showing the location of the
tile indices will also be displayed.  

<img src="/images/Word%20Hunt/sampleListMode.png" alt = "sample list mode" width = "40%">  

### Optional Command Line Arguments
* `--board` - Allows the user to specify which board layout they would like 
  to use. Options are `4x4`, `5x5`, `donut`, and `cross`.
* `--display` - Allows the user to specify which display mode they would 
  like to use. Options are `diagram` and `list`.
* `--maxWordLength` - Allows the user to specify the maximum word length 
  they would like to use. Default is 10, with a range of 3-10.

### ✨ New in Latest Version
* Added support for three new board sizes (5x5, Donut, and Cross)! See 
  images below for examples of each board type.
* Added support for an optional `--board` flag.
* Added support for an optional `--display` flag.
* You will now not be prompted for the max word length. If you wish to use
  a length different than the default (10), you can specify it with the 
  `--maxWordLength` flag (range 3-10).

<img src="/images/Word%20Hunt/sample_4x4_diagram.png" alt = "4x4 board" width = "40%" align="left">
<img src="/images/Word%20Hunt/sample_5x5_diagram.png" alt = "5x5 board" width = "40%" align="left">  
<img src="/images/Word%20Hunt/sample_donut_diagram.png" alt = "donut board" width = "40%" align="left">
<img src="/images/Word%20Hunt/sample_cross_diagram.png" alt = "cross board" width = "40%" align="left">  