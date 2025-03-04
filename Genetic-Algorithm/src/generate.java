import java.util.Random;
import java.io.File;
import java.io.FileWriter;
import java.util.List;
import java.util.ArrayList;
import com.google.gson.Gson;

public class generate {
    private static final String HELP_MESSAGE = "Usage: java generate <seed> <number of levels to generate>.\n";
    public static void main(String args[]) {
        if(args.length < 2){
            System.err.println("ERROR: Invalid number of arguments.\n" + HELP_MESSAGE);
            System.exit(1);
        }

        Random main_random = new Random();
        main_random.setSeed(Long.parseLong(args[0]));

        int levelWidth = 140;
        int levelHeight = 14;

        List<Long> seeds = new ArrayList<>();
        List<Long> times = new ArrayList<>();
        
        // Create parent folder
        String levelsFolder = "levels_GeneticAlgorithm";
        createFolder(levelsFolder);
        
        // Default parameters
        int populationSize = levelWidth * 40;    // Each one of the four populations would have levelWidth * 10 = 1400 individuals
        float mutationRate = 0.3f;
        float crossoverRate = 0.9f;
        int elitismCount = 1;
        int tournamentSize = 2;
        int steps = levelWidth * 8;

        // Generate the levels
        int generations = Integer.parseInt(args[1]);
        for(int i = 0; i < generations; i++){
            String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
            System.out.println("Generating " + outputLevelPath + "...");

            long seed = main_random.nextLong();

            long startTime = System.nanoTime();

            String levelString = generate_level.generate(seed, steps, levelWidth, levelHeight, populationSize, mutationRate, crossoverRate, elitismCount, tournamentSize);
            
            long endTime = System.nanoTime();

            seeds.add(seed);
            times.add(endTime - startTime);

            try{
                FileWriter fw = new FileWriter(outputLevelPath);
                fw.write(levelString);
                fw.close();
            }
            catch(Exception e){
                System.err.println("ERROR: Could not write to file " + outputLevelPath + ".txt\n" + e);
                System.exit(1);
            }
    
            System.out.println("Level generated");
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
}
