package postGen;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Locale;

/**
 * Generates formatted submissions for Lizzi's FLight Rising Art Trade Event!
 * 
 */
public class FR_Post_Gen {
	// Name of the file containing submissions to generate template from
	private static final String FILE_NAME = "./SUBMISSIONS - Responses.tsv";

	public static void main(String[] args) {
		ArrayList<String> responses = new ArrayList<String>();
		ArrayList<String[]> responsesDone = new ArrayList<String[]>();

		ArrayList<String[]> drag = new ArrayList<String[]>();
		ArrayList<String[]> gij = new ArrayList<String[]>();

		// Loading responses from the file
		responses = load();

		// Removing the top text
		responses.remove(0);

		// Sort the strings
		java.util.Collections.sort(responses, Collator.getInstance(Locale.US));

		// Reform string array format
		responsesDone = split(responses);

		for (String[] response : responsesDone) {
			if (response[5].equals("Dragon"))
				drag.add(response);
			else
				gij.add(response);
		}

		// Write responses into a text file with the formatted art tempalte
		write(drag, gij);
	}

	// Load the responses from the file
	// Artist = 0, Recipient = 1, Full Art Link = 2, Preview Link = 3, Type = 5
	private static ArrayList<String> load() {
		ArrayList<String> responses = new ArrayList<String>();

		BufferedReader in;

		String line = "";
		try {
			in = new BufferedReader(new FileReader(FILE_NAME));

			while ((line = in.readLine()) != null) {
				// Break string into array, remove first element and reform string
				String[] temp = line.split("\t");
				temp = Arrays.copyOfRange(temp, 1, temp.length);
				// Swap recipient and artist
				String temp1 = temp[0];
				temp[0] = temp[1];
				temp[1] = temp1;
				responses.add(String.join("\t", temp));
			}
			in.close();
		} catch (Exception e) {
			System.out.println("ERROR LOADING FILE");
			e.printStackTrace();
		}
		return responses;
	}

	// Write to a file with the formatted art template
	private static void write(ArrayList<String[]> dragon, ArrayList<String[]> gijinka) {
		BufferedWriter out;

		try {
			out = new BufferedWriter(new FileWriter("./art_template_DRAG.txt"));
			out.write("[center][size=6][b]Dragon Art[/b][/size]\n(Click the previews to see the full image!)\nArtwork is organized alphabetically by [b][u]recipient![/b][/u]\n\n");
			for (int i = 0; i < dragon.size(); i++) {
				out.write((i % 2 < 1 ? "[columns]\n" : "") + "[url=" + dragon.get(i)[2] + "][img]" + dragon.get(i)[3]
						+ "[/img][/url]\n");
				out.write("[center][i]For[/i] @" + dragon.get(i)[0] + "\n[i]Drawn by[/i] @" + dragon.get(i)[1]
						+ " [/center]" + (i % 2 < 1 ? "\n[nextcol]\n" : ""));
				if (i % 2 > 0 || i == dragon.size() - 1)
					out.write("\n[/columns]\n\n\n");
			}
			out.close();

			out = new BufferedWriter(new FileWriter("./art_template_GIJ.txt"));
			out.write("[center][size=6][b]Gijinka Art[/b][/size]\n(Click the previews to see the full image!)\nArtwork is organized alphabetically by [b][u]recipient![/b][/u]\n\n");
			for (int i = 0; i < gijinka.size(); i++) {
				out.write((i % 2 < 1 ? "[columns]\n" : "") + "[url=" + gijinka.get(i)[2] + "][img]" + gijinka.get(i)[3]
						+ "[/img][/url]\n");
				out.write("[center][i]For[/i] @" + gijinka.get(i)[0] + "\n[i]Drawn by[/i] @" + gijinka.get(i)[1]
						+ " [/center]" + (i % 2 < 1 ? "\n[nextcol]\n" : ""));
				if (i % 2 > 0 || i == gijinka.size() - 1)
					out.write("\n[/columns]\n\n\n");
			}
			out.close();
		} catch (Exception e) {
			System.out.println("ERROR WRITING FILE");
			e.printStackTrace();
		}
	}

	// Converts the array of strings into a single string that
	// can be sorted and then put back into the original format.
	private static ArrayList<String[]> split(ArrayList<String> strings) {
		ArrayList<String[]> responses = new ArrayList<String[]>();

		// Split all strings by the regex
		for (int i = 0; i < strings.size(); i++)
			responses.add(strings.get(i).split("\t"));

		return responses;
	}
}