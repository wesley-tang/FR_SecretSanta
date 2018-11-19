package matcher;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

/**
 * Creates a program that creates secret Santa matchups for Lizzi's Flight
 * Rising Art Trade Event!
 * 
 */
public class FR_Secret_Santa {
	// Name of the file containing users to match
	private static final String FILE_NAME = "./submissions.tsv";


	// Name = 0, ID# = 1, Draw = 2, Receive = 3, Backup? = 4, Post Link = 5
	private static final int NAME_INDEX = 0;
	private static final int ID_INDEX = 1;
	private static final int DRAW_INDEX = 2;
	private static final int RECEIVE_INDEX = 3;
	private static final int REF_INDEX = 5;
	

	// Main program to call the matcher
	public static void main(String[] args) {
		ArrayList<String[]> responses = new ArrayList<String[]>();

		// Loading responses from the file
		responses = load();
//
//		// Removing the top text
//		responses.remove(0);

		// Continue matching if not everyone is matched
		while (matchAll(responses).size() != responses.size()) {
			System.out.println("Whoops - not all matchups made - try again.");
		}
		System.out.println("\n~~ DONE ~~");
	}

	// The whole match making function
	private static ArrayList<Pair<String[], String[]>> matchAll(ArrayList<String[]> responses) {
		// Lists
		ArrayList<String[]> dragonDraw = new ArrayList<String[]>();
		ArrayList<String[]> gijinkaDraw = new ArrayList<String[]>();
		ArrayList<String[]> dragonDrawPref = new ArrayList<String[]>();
		ArrayList<String[]> gijinkaDrawPref = new ArrayList<String[]>();

		ArrayList<String[]> dragonRec = new ArrayList<String[]>();
		ArrayList<String[]> gijinkaRec = new ArrayList<String[]>();
		ArrayList<String[]> dragonRecPref = new ArrayList<String[]>();
		ArrayList<String[]> gijinkaRecPref = new ArrayList<String[]>();

		ArrayList<String[]> noDraw = new ArrayList<String[]>();
		ArrayList<String[]> noRec = new ArrayList<String[]>();

		ArrayList<Pair<String[], String[]>> matchups = new ArrayList<Pair<String[], String[]>>();

		// Generating lists for drawing/receiving preferences
		for (String[] response : responses) {
			if (response[DRAW_INDEX].equals("No Preference"))
				noDraw.add(response);
			else if (response[DRAW_INDEX].equals("Dragon/Feral Art Preferred"))
				dragonDrawPref.add(response);
			else if (response[DRAW_INDEX].equals("Dragon/Feral Art Only"))
				dragonDraw.add(response);
			else if (response[DRAW_INDEX].equals("Human Art Preferred"))
				gijinkaDrawPref.add(response);
			else
				gijinkaDraw.add(response);

			// Generating receiving preference lists
			if (response[RECEIVE_INDEX].equals("No Preference"))
				noRec.add(response);
			else if (response[RECEIVE_INDEX].equals("Dragon/Feral Art Preferred"))
				dragonRecPref.add(response);
			else if (response[RECEIVE_INDEX].equals("Dragon/Feral Art Only"))
				dragonRec.add(response);
			else if (response[RECEIVE_INDEX].equals("Human Art Preferred"))
				gijinkaRecPref.add(response);
			else
				gijinkaRec.add(response);
		}

		// Printing stats
		System.out.println("\n\nDrawing:");
		System.out.println("Gijinka Only: " + gijinkaDraw.size() + "\tDragon Only: " + dragonDraw.size());
		System.out.println(
				"Gijinka Preferred: " + gijinkaDrawPref.size() + "\tDragon Preferred: " + dragonDrawPref.size());
		System.out.println("No Preference: " + noDraw.size());

		System.out.println("\nReceiving:");
		System.out.println("Gijinka Only: " + gijinkaRec.size() + "\tDragon Only: " + dragonRec.size());
		System.out
				.println("Gijinka Preferred: " + gijinkaRecPref.size() + "\tDragon Preferred: " + dragonRecPref.size());
		System.out.println("No Preference: " + noRec.size());
		System.out.println("Total participants: " + responses.size() + "\n\n");

		// Write statistics file
		BufferedWriter out;
		try {
			out = new BufferedWriter(new FileWriter("./matchup_STATS.txt"));
			out.write("Drawing:");
			out.write("\nGijinka Only: " + gijinkaDraw.size() + "\tDragon Only: " + dragonDraw.size());
			out.write("\nGijinka Preferred: " + gijinkaDrawPref.size() + "\tDragon Preferred: " + dragonDrawPref.size());
			out.write("\nNo Preference: " + noDraw.size());

			out.write("\n\nReceiving:");
			out.write("\nGijinka Only: " + gijinkaRec.size() + "\tDragon Only: " + dragonRec.size());
			out.write("\nGijinka Preferred: " + gijinkaRecPref.size() + "\tDragon Preferred: " + dragonRecPref.size());
			out.write("\nNo Preference: " + noRec.size());
			out.write("\nTotal participants: " + responses.size());
			out.close();

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		// Match dragon only responses
		matchups.addAll(matchup(dragonDraw, dragonRec));

		// Merge remaining dragon only responses to the dragon preference
		// responses
		dragonDrawPref.addAll(dragonDraw);
		dragonRecPref.addAll(dragonRec);

		// Match gijinka only responses
		matchups.addAll(matchup(gijinkaDraw, gijinkaRec));

		// Merge remaining gijinka only responses to the gijinka preference
		// responses
		gijinkaDrawPref.addAll(gijinkaDraw);
		gijinkaRecPref.addAll(gijinkaRec);

		// Match dragon preference responses
		matchups.addAll(matchup(dragonDrawPref, dragonRecPref));

		// Merge remaining dragon responses with the no prefs
		noDraw.addAll(dragonDrawPref);
		noRec.addAll(dragonRecPref);

		// Match gijinka preference responses
		matchups.addAll(matchup(gijinkaDrawPref, gijinkaRecPref));

		// Merge remaining gijinka responses with the no prefs
		noDraw.addAll(gijinkaDrawPref);
		noRec.addAll(gijinkaRecPref);

		// Match all remaining responses
		matchups.addAll(matchup(noDraw, noRec));

		// Write the results into a file
		write(matchups);

		return matchups;
	}

	// Matchup random pairs given two lists
	private static ArrayList<Pair<String[], String[]>> matchup(ArrayList<String[]> list1, ArrayList<String[]> list2) {
		ArrayList<Pair<String[], String[]>> matchups = new ArrayList<Pair<String[], String[]>>();

		if (list1.size() <= list2.size())
			// Matchup first from list1 with a random one from the other list
			while (!list1.isEmpty()) {
				// Choose a random person that isn't themselves
				int rand = ThreadLocalRandom.current().nextInt(0, list2.size());
				// If the person is themselves, or they are a bad matchup, keep rerolling
				while (list1.get(0).equals(list2.get(rand)) || badMatch(list1.get(0)[NAME_INDEX], list2.get(rand)[NAME_INDEX])) {
					// Case where there is only the same person left, let them
					// fall to the next category
					if (list1.size() == 1 && list2.size() == 1)
						return matchups;
					else
						rand = ThreadLocalRandom.current().nextInt(0, list2.size());
				}

				matchups.add(new Pair<String[], String[]>(list1.get(0), list2.get(rand)));

				list1.remove(0);
				list2.remove(rand);
			}
		else
			while (!list2.isEmpty()) {
				int rand = ThreadLocalRandom.current().nextInt(0, list1.size());
				while (list2.get(0).equals(list1.get(rand)) || badMatch(list1.get(0)[NAME_INDEX], list2.get(rand)[NAME_INDEX])) {
					// Case where there is only the same person left, let them
					// fall to the next category
					if (list1.size() == 1 && list2.size() == 1)
						return matchups;
					else
						rand = ThreadLocalRandom.current().nextInt(0, list1.size());
				}

				matchups.add(new Pair<String[], String[]>(list1.get(rand), list2.get(0)));

				list1.remove(rand);
				list2.remove(0);
			}

		return matchups;
	}

	// Load the responses from the file
	// OLD: Name = 1, ID# = 2, Draw = 3, Receive = 4, References = 5, Backup? = 6
	// Userpage = 8 OLD
	private static ArrayList<String[]> load() {
		ArrayList<String[]> responses = new ArrayList<String[]>();

		BufferedReader in;

		String line = "";
		try {
			in = new BufferedReader(new FileReader(FILE_NAME));

			while ((line = in.readLine()) != null) {
				responses.add(line.split("\t"));
			}
			in.close();
		} catch (Exception e) {
			System.out.println("ERROR LOADING FILE");
		}
		return responses;
	}

	// Take the given matchups and printing to a file
	private static void write(ArrayList<Pair<String[], String[]>> matchups) {
		BufferedWriter out;

		try {
			// Write matchups file
			out = new BufferedWriter(new FileWriter("./matchups_NAMES_ONLY.txt"));
			for (Pair<String[], String[]> pair : matchups) {
				out.write("Artist: " + pair.fst()[NAME_INDEX] + " > Recipient: " + pair.snd()[NAME_INDEX] + "\n");
			}
			out.close();

			// Write preference matchups file
			out = new BufferedWriter(new FileWriter("./matchups_PREF_ONLY.txt"));
			for (Pair<String[], String[]> pair : matchups) {
				out.write("Artist: " + pair.fst()[DRAW_INDEX] + " > Recipient: " + pair.snd()[RECEIVE_INDEX] + "\n");
			}
			out.close();

			// Write matchups with ID numbers
			out = new BufferedWriter(new FileWriter("./matchups_NAMES_ID.txt"));
			for (Pair<String[], String[]> pair : matchups) {
				out.write("Artist: " + pair.fst()[NAME_INDEX] + " -" + pair.fst()[ID_INDEX] + "-  > Recipient: " + pair.snd()[NAME_INDEX] + " -"
						+ pair.snd()[ID_INDEX] + "-\n");
			}
			out.close();

			// Write matchups for the Python Script auto message
			out = new BufferedWriter(new FileWriter("./matchups.tsv"));
			for (Pair<String[], String[]> pair : matchups) {
				out.write(pair.fst()[NAME_INDEX] + "\t" + ("flightrising.com/main.php?p=lair&tab=userpage&id=" + pair.snd()[ID_INDEX]) + "\t" + pair.snd()[NAME_INDEX] + "\t" + pair.snd()[RECEIVE_INDEX] + "\t"
						+ pair.snd()[REF_INDEX] + "\n");
			}
			out.close();

		} catch (Exception e) {
			System.out.println("ERROR WRITING FILE");
		}
	}
	
	/**
	 * Checks for any exceptions made during matches
	 * 
	 * @return True if this match is an exception that should not be made, false if it's fine
	 */
	private static boolean badMatch(String person1, String person2) {
		if (person1.equals("Lizzi") || person1.equals("Hexlash") || person1.equals("FightingPolygon") && person2.equals("Lizzi") || person2.equals("Hexlash") || person2.equals("FightingPolygon")) {
				return true;
		}
//		else if () {
//			
//				return true;
//		}
			
		return false;
	}

	/**
	 * Holds two objects in a tuple. For holding matchups.
	 *
	 * @param <X>
	 * @param <Y>
	 */
	public static class Pair<X, Y> {
		public final X x;
		public final Y y;

		public Pair(X x, Y y) {
			this.x = x;
			this.y = y;
		}

		public X fst() {
			return this.x;
		}

		public Y snd() {
			return this.y;
		}
	}
}
