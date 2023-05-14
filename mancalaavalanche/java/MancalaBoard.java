import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

/**
 * Class that represents the game board for Mancala (avalanche)
 * 
 * @author Kyle Gerner
 * @version 5.11.2020
 *
 */
public class MancalaBoard {

    private int[] spaces;
    private final int BOARDRANGE = 13; // board will be size 14 to include
                                       // opponent's store, but that store will
                                       // never be used. I included the
                                       // opponent's store just so I could
                                       // visualize the array better


    /**
     * Constructor
     * 
     * @param userArr
     *            array of user data
     * @param oppArr
     *            array of opponent data
     */
    public MancalaBoard(int[] userArr, int[] oppArr) {
        spaces = new int[14]; // 6 on each side, 1 for user store
        // 0 - 5 = user spaces
        // 6 = user store
        // 7 - 12 = opponent spaces
        // 13 = opponent store
        for (int i = 0; i < 6; i++) {
            spaces[i] = userArr[i];
            spaces[12 - i] = oppArr[i];
        }
        spaces[13] = -1; // should never be accessed
    }


    /**
     * Calls the findBestMoveCaller method with this board's 'spaces' field
     * 
     * @param oneByOne
     *            whether or not we want the instructions to be printed one by
     *            one
     */
    public void findBestMove(boolean oneByOne) {
        Queue<Integer> bestIndexes = new LinkedList<Integer>();
        int maxScore = findBestMoveCaller(spaces, bestIndexes);
        String spotOrders =
            "\n\nThe spaces you should choose, in order, are (from top):\n";
        int numMoves = 0;
        for (int i : bestIndexes) {
            spotOrders += numMoves+1 + ":  Spot # " + (i + 1) + "\n";
            numMoves++;
        }
        spotOrders += "\nPoints scored this round: " + maxScore
            + "\n# of moves: " + numMoves;
        performMoves(bestIndexes);
        printBoard();
        if (oneByOne) {
            System.out.println("Press enter to receive a new instruction.");
            String[] strArr = spotOrders.split("\\s*\n\\s*");
            System.out.print(strArr[0] + strArr[1]);
            Scanner scan = new Scanner(System.in);
            int i = 2;
            while (i < strArr.length - 1) {
                scan.nextLine();
                System.out.print(strArr[i]);
                i++;
            }
            System.out.println("\n" + strArr[strArr.length - 1]);
        }
        else
            System.out.println(spotOrders);
    }


    /**
     * Finds the best sequence of moves for the user and prints the instructions
     * 
     * @param spots
     *            version of the board array we are checking
     * @param bestChoices
     *            the indexes of the best choices of spaces that lead to highest
     *            scores
     * @return score of best choice
     */
    private int findBestMoveCaller(int[] spots, Queue<Integer> bestChoices) {
        if (isUserSideEmpty(spots))
            return 0;
        int maxScore = -1;
        Queue<Integer> indexVisits = new LinkedList<Integer>();
        for (int i = 0; i < 6; i++) {
            int thisScore = 0;
            // int numRocks = spots[i];
            Queue<Integer> thisVisits = new LinkedList<Integer>();
            thisVisits.add(i);
            thisScore = bestMoveHelper(thisScore, i, spots.clone(), thisVisits);
            if (thisScore > maxScore) {
                maxScore = thisScore;
                indexVisits.clear();
                while (!thisVisits.isEmpty()) {
                    indexVisits.add(thisVisits.poll());
                }
            }
        } // end for
        for (int j : indexVisits)
            bestChoices.add(j);
        return maxScore;

    }


    /**
     * Recursive helper method for finding the best move
     * 
     * @param score
     *            current score of the run
     * @param currInd
     *            current index on the board
     * @param spots
     *            the array of the board
     * @param q
     *            a queue that holds the visits that have the highest score
     * @return end score of the run
     */
    private int bestMoveHelper(
        int score,
        int currInd,
        int[] spots,
        Queue<Integer> q) {
        // int currInd = i;
        // int prevInd = currInd == 0 ? 12 : currInd - 1;
        int numRocks = spots[currInd];
        spots[currInd] = 0;
        // int[] spacesCopy = spaces.clone();
        // Queue<Integer> thisRunVisits = new LinkedList<Integer>();
        while (numRocks > 0) {
            // prevInd = currInd;
            currInd = (currInd + 1) % BOARDRANGE;
            spots[currInd]++; // place a rock into space;
            numRocks--;
            // next want to check if I end my run on a spot with more rocks
            if (numRocks == 0 && spots[currInd] > 1 && currInd != 6) {
                numRocks = spots[currInd];
                spots[currInd] = 0;
            }
            // check if placed into user's store/bank
            if (currInd == 6) {
                score++;
            }
        }

        if (currInd == 6) { // if ended in my store/bank
            if (!isUserSideEmpty(spots))
                score += findBestMoveCaller(spots, q);
        }

        return score;
    }


    /**
     * Performs the specified moves on the actual board for this MancalaBoard
     * 
     * @param movesList
     */
    private void performMoves(Queue<Integer> movesList) {
        int currInd = movesList.poll();
        int numRocks = spaces[currInd];
        spaces[currInd] = 0;

        while (numRocks > 0) {
            // prevInd = currInd;
            currInd = (currInd + 1) % BOARDRANGE;
            spaces[currInd]++; // place a rock into space;
            numRocks--;
            // next want to check if I end my run on a spot with more rocks
            if (numRocks == 0 && spaces[currInd] > 1 && currInd != 6) {
                numRocks = spaces[currInd];
                spaces[currInd] = 0;
            }
            // check if placed into user's store/bank
            if (numRocks == 0 && currInd == 6) {
                if (isUserSideEmpty(spaces))
                    break;
                currInd = movesList.poll();
                numRocks = spaces[currInd];
                spaces[currInd] = 0;
            }
        }

    }


    /**
     * Checks the user's side of the board is empty
     * 
     * @param arr
     *            array we are checking
     * @return true if user's side has 0 rocks in every slot
     */
    public boolean isUserSideEmpty(int[] arr) {
        for (int i = 0; i < 6; i++) {
            if (arr[i] > 0)
                return false;
        }
        return true;
    }


    /**
     * Prints the board in a user-friendly format
     */
    public void printBoard() {
        System.out.println("Current board:\n");
        System.out.println("       ?       <---- Opponent Store");
        String horizBreak = "----------------";
        System.out.println(horizBreak);
        for (int i = 0; i < 6; i++) {
            String line = "   " + spaces[i] + "   |   " + spaces[12 - i] + "\n";
            System.out.println(line + horizBreak);
        }
        System.out.println("       " + spaces[6] + "       <---- Your Store\n");
    }


    /**
     * Converts int array to readable string
     * 
     * @param arr
     *            array of integers
     * @return String representation of array
     */
    public String arrToStr(int[] arr) {
        String s = "[";
        for (int i = 0; i < arr.length - 1; i++)
            s += arr[i] + ", ";
        s += arr[arr.length - 1] + "]";
        return s;
    }

}
