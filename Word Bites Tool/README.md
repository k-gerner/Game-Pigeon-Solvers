# Word Bites  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Word%20Bites/sampleWordBitesBoard.jpeg" alt = "sample board" width="40%" align = "right">     

### The Basics  
In Word Bites, players are presented with a 9x8 board of open space. Scattered around the board are several letter tiles, which can be either 1 or 2 letters long, and can be oriented vertically or horizontally. In order to earn points, players must connect pieces on the board to form English words. The longer the word, the more points the player earns. Whoever scores more points in 80 seconds wins.
### How to use
First, download the `wordBitesTool.py` and `letters9.txt` files and place them both in the same directory. You can invoke the tool by running  
```
> python3 wordBitesTool.py
```
Once you do this, you will be prompted about which display mode you would like to use: `Diagram Mode`, or `List Mode`. Typing `i` will give you more information about each of them.  
After this, you will be asked to input the letter tiles in 3 different categories: single letters, horizontal pieces, and vertical pieces. Then, the program will calculate and display the best piece combinations.
#### Diagram Mode
Diagram mode will display each word one at a time, along with a visual representation of how to arrange the board pieces. Longer words will be displayed first.  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Word%20Bites/sampleDiagramMode.png" alt = "sample diagram mode" width = "30%"> 
    
#### List Mode
List mode will display every possible word on the board all at once, along with the orientation of the word, either saying `V` for vertical, or `H` for horizontal. Longer words will be displayed first.  

<img src="https://github.com/k-gerner/Game-Pigeon-Solvers/blob/master/Images/Word%20Bites/sampleListMode.png" alt = "sample list mode" align = "left" width = "30%">  
