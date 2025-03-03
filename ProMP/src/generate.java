import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import com.google.gson.Gson;

import engine.core.MarioLevelModel;
import engine.core.MarioTimer;
import levelGenerators.benWeber.LevelGenerator;

public class generate {
    private static final String HELP_MESSAGE = "Usage: java generate <seed> <number of levels to generate>.\n";

    public static void main(String[] args) {
        if(args.length < 2){
            System.err.println("ERROR: Invalid number of arguments.\n" + HELP_MESSAGE);
            System.exit(1);
        }

        Random main_random = new Random();
        main_random.setSeed(Long.parseLong(args[0]));

        int levelWidth = 140;
        int levelHeight = 14;
        
        // It uses benWeber's level generator because it is the one imported before
        LevelGenerator generator = new LevelGenerator();

        List<Long> seeds = new ArrayList<>();
        List<Long> times = new ArrayList<>();

        // Create the levels folder
        String levelsFolder = "levels_ProMP";
        createFolder(levelsFolder);

        int generations = Integer.parseInt(args[1]);
        for(int i=0; i<generations; i++){
            long seed = main_random.nextLong();

            long startTime = System.nanoTime();

            String level = generator.getGeneratedLevel(new MarioLevelModel(levelWidth, levelHeight), new MarioTimer(5 * 60 * 60 * 1000), seed);
            
            String[] lines = level.split("\\r?\\n");
            List<String> vglcLines = convertLevelToVGLC(lines, main_random);
            List<String> adjustedLevel = adjustPipesAndBullets(vglcLines);
            level = String.join("\n", adjustedLevel);

            long endTime = System.nanoTime();

            saveLevelStringToFile(level, levelsFolder + File.separator + "level" + i + ".txt");
            
            seeds.add(seed);
            times.add(endTime - startTime);
        }

        // Save seeds and times
        saveSeedsAndTimes(seeds, times, levelsFolder);

        System.out.println("Levels generated successfully");
    }

    private static void createFolder(String folderName) {
        File folder = new File(folderName);
        try {
            folder.mkdir();
        } catch (Exception e) {
            System.err.println("ERROR creating folder: " + folderName + ".\n" + e);
            System.exit(1);
        }
    }

    private static void saveSeedsAndTimes(List<Long> seeds, List<Long> times, String output_folder_path) {
        Gson gson = new Gson();
        String seedsJson = gson.toJson(seeds);
        String timesJson = gson.toJson(times);

        try {
            FileWriter seedsFile = new FileWriter(output_folder_path + File.separator + "seeds.json");
            seedsFile.write(seedsJson);
            seedsFile.close();
        } catch (Exception e) {
            System.err.println("ERROR: Could not write to file seeds.json\n" + e);
            System.exit(1);
        }

        try {
            FileWriter timesFile = new FileWriter(output_folder_path + File.separator + "times.json");
            timesFile.write(timesJson);
            timesFile.close();
        } catch (Exception e) {
            System.err.println("ERROR: Could not write to file times.json\n" + e);
            System.exit(1);
        }
    }

    public static void saveLevelStringToFile(String level, String fileName) {
        try {
            java.io.PrintWriter out = new java.io.PrintWriter(fileName);
            String[] lines = level.split("\\r?\\n");
            for (String line : lines) {
                out.println(line);
            }
            out.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    private static List<String> convertLevelToVGLC(String[] levelLines, Random random) {
        List<String> vglcLines = new ArrayList<>();
        for (String line : levelLines) {
            String vglcLine = "";
            for (char ch : line.toCharArray()) {
                vglcLine += convertCharToVGLC(ch, random);
            }
            vglcLines.add(vglcLine);
        }
        return vglcLines;
    }

    private static char convertCharToVGLC(char ch, Random random) {
        switch (ch) {
            case 'M':
            case 'F':
                throw new IllegalArgumentException("ERROR. Level contains initial or final positions.");
            case '#':
                return 'X';
            case 'C':
            case 'L':
            case 'U':
            case '2':
            case '1':
            case 'D':
            case '%':
                return 'S';
            case '@':
            case '!':
                return random.nextBoolean() ? '?' : 'Q';
            case 't':
            case 'T':
                return 't';
            case '*':
                return '*';
            case '|':
                return '-';
            case 'g':
            case 'G':
            case 'r':
            case 'R':
            case 'k':
            case 'K':
            case 'y':
            case 'Y':
                return 'E';
            default:
                return ch;
        }
    }

    private static List<String> adjustPipesAndBullets(List<String> levelLines) {
        List<String> newLevel = new ArrayList<>();
        for (int i = 0; i < levelLines.size(); i++) {
            String newLine = "";
            int j = 0;

            while (j < levelLines.get(i).length()) {
                char ch = levelLines.get(i).charAt(j);

                if (ch == 't') {
                    if (i != 0 && levelLines.get(i - 1).charAt(j) == 't') {
                        newLine += '[';
                        if (j != levelLines.get(i).length() - 1 && levelLines.get(i).charAt(j + 1) == 't') {
                            newLine += ']';
                            j++;
                        }
                    } else {
                        newLine += '<';
                        if (j != levelLines.get(i).length() - 1 && levelLines.get(i).charAt(j + 1) == 't') {
                            newLine += '>';
                            j++;
                        }
                    }
                } else if (ch == '*') {
                    if (i != 0 && levelLines.get(i - 1).charAt(j) == '*') {
                        newLine += 'b';
                    } else {
                        newLine += 'B';
                    }
                } else {
                    newLine += ch;
                }

                j++;
            }

            newLevel.add(newLine);
        }
        return newLevel;
    }
}