# Anagrams  

<img src="/Images/Anagrams/sampleAnagramsBoard.jpeg" alt = "sample board" width="40%" align = "right">   

### The Basics  
In Anagrams, players are given a set of either 6 or 7 letters. The 
objective of the game is to arrange the given letters into valid 
English words.  
### How to use  
First, download the `anagrams_client.py` and `letters7.txt` files and 
place them all in the same directory. You can invoke the tool by 
running  
```
> python3 anagrams_client.py
```  
Once you do this, you will be asked how many letters are given (either 
6 or 7). Next, you will be prompted for the letters on the board. 
After entering them, there will be 10 words displayed at a time, 
unless you type 'a' to see the entire list at once.  

<img src="/Images/Anagrams/sampleAnagramsOutput.png" alt = "sample output" width = "30%">

### ✨ New in Version 1.1
* The results will now be displayed in place (10 at a time), erasing 
the previously displayed output when the user requests to see 
additional words. This can be turned off with the command line 
argument `-e` or `-eraseModeOff`.
