import java.util.Scanner;

/**
 * I made this program to tell me what the best move to make in Mancala
 * Avalanche game mode is for the Mancala game on the Game Pigeon iMessage app
 * thing
 * 
 * @author Kyle Gerner
 * @version 5.11.2020
 */
public class MancalaAvalanche {

    static Scanner scan;


    public static void main(String[] args) {
        scan = new Scanner(System.in); // Create a Scanner object
        String sectionBreak =
            "----------------------------------------------------------------";
        System.out.println(
            "Welcome to Mancala Avalanche Helper (made by Kyle G. 5/11/2020\n"
                + sectionBreak);
        System.out.println("Which mode?\n1 = All instructions at once\n2 = Instructions one by one\nq = Quit\n");
        String mode = scan.nextLine();
        String instrPlayer =
            "Enter your side from top to bottom in the format  1,2,3,4,5,6:";
        String instrOpp =
            "Enter the opponent's side from top to bottom in the format  1,2,3,4,5,6:";
        boolean oneByOne = mode.contentEquals("2");
        String userInput = "y"; // scan.nextLine(); // Read user input
        while (userInput.contentEquals("y") && !mode.contentEquals("q")) {
            System.out.println(instrPlayer);
            int[] userArray = makeArrayFromInput(scan.nextLine()); // pieces in
                                                                   // each cup
                                                                   // on user
                                                                   // side
            System.out.println(instrOpp);
            int[] oppArray = makeArrayFromInput(scan.nextLine()); // pieces in
                                                                  // each cup on
                                                                  // opponent
                                                                  // side

            MancalaBoard board = new MancalaBoard(userArray, oppArray);
            // System.out.println("Initial Board:\n");
            System.out.println();
            board.printBoard();

            System.out.println(sectionBreak);

            System.out.println(
                "Now calculating best moves. Press enter to continue.");
            userInput = scan.nextLine();

            board.findBestMove(oneByOne);

            System.out.println(sectionBreak + "\n" + sectionBreak + "\n"
                + sectionBreak);

            System.out.print("Continue to next round? (y/n):  ");

            userInput = scan.nextLine();
            
        }
        System.out.println("Thanks for stopping by! Hope you won!");
    }


    /**
     * Fills an array with the data from user input
     * 
     * @param line
     *            line of user input
     * @return array filled with integer values from input
     */
    private static int[] makeArrayFromInput(String line) {
        String[] strArr = line.split("\\s*,\\s*");
        while (strArr.length != 6) {
            System.out.println("Incorrect format. Try again:");
            String newTry = scan.nextLine();
            strArr = newTry.split("\\s*,\\s*");
        }
        int[] arr = new int[6];
        for (int i = 0; i < 6; i++) {
            try{
                arr[i] = Integer.parseInt(strArr[i]);
            }
            catch(Exception e){
                System.out.println("There was an issue with your input. Please re-run the program and enter input in the correct format.");
                System.exit(0);
            }
        }
        return arr;

    } // end makeArrayFromInput
}
