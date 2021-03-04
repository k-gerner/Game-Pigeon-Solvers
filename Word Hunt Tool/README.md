# Word Hunt  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Word%20Hunt/sampleWordHuntBoard.jpeg" alt = "sample board" width="300" height="455" align = "right">     

### The Basics  
In Word Hunt, players are presented with a 4x4 board of letter tiles. In order to earn points, players must connect adjacent tiles on the board to form English words. The longer the word, the more points the player earns. Whoever scores more points in 80 seconds wins.
### How to use
First, download the `wordHuntTool.py`, `classes.py`, and `letters10.txt` files and place them all in the same directory. You can invoke the tool by running  
```
> python3 wordHuntTool.py
```
Once you do this, you will be prompted about the maximum word length. The default length is 10, which means the tool will look for words that are between 3 and 10 letters long, inclusive.  

Next, you will be prompted about which display mode you would like to use: `Diagram Mode`, or `List Mode`. Typing `i` will give you more information about each of them. 
#### Diagram Mode
Diagram mode will display each word one at a time, along with a visual representation of the board which shows the user the path they should take to connect the letters. Longer words will be displayed first.  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Word%20Hunt/sampleDiagramMode2.png" alt = "sample diagram mode" width = "30%"> 
    
#### List Mode
List mode will display every possible word on the board all at once, along with the index on the board at which the first letter is located. Longer words will be displayed first.  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Word%20Hunt/sampleListMode.png" alt = "sample list mode" align = "left" width = "30%">  
