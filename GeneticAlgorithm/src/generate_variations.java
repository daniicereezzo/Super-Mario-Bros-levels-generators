import java.util.Random;
import java.io.File;
import java.io.FileWriter;
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.List;
import java.util.ArrayList;
import com.google.gson.Gson;

import dk.itu.mario.engine.util.PRNG;

public class generate_variations {
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

        // Default parameters
        int defaultGenerations = Integer.parseInt(args[1]);
        String defaultOutputfolder = "levels_default";
        int defaultPopulationSize = levelWidth * 40;    // Each one of the four populations would have levelWidth * 10 = 1400 individuals
        float defaultMutationRate = 0.3f;
        float defaultCrossoverRate = 0.9f;
        int defaultElitismCount = 1;
        int defaultTournamentSize = 2;
        int defaultSteps = levelWidth * 8;
        
        int generations = 10;
        int[] steps = {500, 2000};
        int[] populations = {40, 400};  // Each one of the four populations would have 10 or 100 individuals
        int[] tournamentSizes = {5, 7};
        float[] crossoverRates = {0.5f, 0.7f};
        float[] mutationRates = {0.05f, 0.1f};
        int[] elitismCounts = {14, 70}; // 1% and 5% of the size of each population

        Dictionary<String, List<Long>> seeds = new Hashtable<>();
        Dictionary<String, List<Integer>> times = new Hashtable<>();

        seeds.put("default", new ArrayList<Long>());
        times.put("default", new ArrayList<Integer>());

        for(int step : steps){
            seeds.put("iterations_" + step, new ArrayList<Long>());
            times.put("iterations_" + step, new ArrayList<Integer>());
        }

        for(int population : populations){
            seeds.put("pop_size_" + population, new ArrayList<Long>());
            times.put("pop_size_" + population, new ArrayList<Integer>());
        }

        for(int tournamentSize : tournamentSizes){
            seeds.put("tournament_size_" + tournamentSize, new ArrayList<Long>());
            times.put("tournament_size_" + tournamentSize, new ArrayList<Integer>());
        }

        for(float crossoverRate : crossoverRates){
            seeds.put("cross_rate_" + crossoverRate, new ArrayList<Long>());
            times.put("cross_rate_" + crossoverRate, new ArrayList<Integer>());
        }

        for(float mutationRate : mutationRates){
            seeds.put("mut_rate_" + mutationRate, new ArrayList<Long>());
            times.put("mut_rate_" + mutationRate, new ArrayList<Integer>());
        }

        for(int elitismCount : elitismCounts){
            seeds.put("elitism_" + elitismCount, new ArrayList<Long>());
            times.put("elitism_" + elitismCount, new ArrayList<Integer>());
        }
        
        // Create parent folder
        createFolder("levels");

        // Execute the Mario GA for the default parameters

        // Create the default levels folder
        String levelsFolder = "levels" +  File.separator + defaultOutputfolder;
        createFolder(levelsFolder);
        
        // Generate the levels

        System.out.println("Generating default levels...");

        for(int i = 0; i < defaultGenerations; i++){
            String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
            System.out.println("Generating " + outputLevelPath + "...");

            long seed = main_random.nextLong();

            long startTime = System.nanoTime();
            String levelString = generate_level.generate(seed, defaultSteps, levelWidth, levelHeight, defaultPopulationSize, defaultMutationRate, defaultCrossoverRate, defaultElitismCount, defaultTournamentSize);
            long endTime = System.nanoTime();

            seeds.get("default").add(seed);
            times.get("default").add((int) ((endTime - startTime)));

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
        saveSeedsAndTimes(seeds, times);

        // Execute the Mario GA for the rest of the parameters
        for(int step : steps){
            // Create the levels folder
            levelsFolder = "levels" +  File.separator + "levels_steps_" + step;
            createFolder(levelsFolder);

            System.out.println("Generating levels for steps = " + step);

            // Generate the levels
            for(int i = 0; i < generations; i++){
                String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
                System.out.println("Generating " + outputLevelPath + "...");

                long seed = main_random.nextLong();

                long startTime = System.nanoTime();
                String levelString = generate_level.generate(seed, step, levelWidth, levelHeight, defaultPopulationSize, defaultMutationRate, defaultCrossoverRate, defaultElitismCount, defaultTournamentSize);
                long endTime = System.nanoTime();

                seeds.get("iterations_" + step).add(seed);
                times.get("iterations_" + step).add((int) ((endTime - startTime)));

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
            saveSeedsAndTimes(seeds, times);
        }

        for(int population : populations){
            // Create the levels folder
            levelsFolder = "levels" +  File.separator + "levels_pop_size_" + population;
            createFolder(levelsFolder);

            System.out.println("Generating levels for population_size = " + population);

            // Generate the levels
            for(int i = 0; i < generations; i++){
                String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
                System.out.println("Generating " + outputLevelPath + "...");

                long seed = main_random.nextLong();

                long startTime = System.nanoTime();
                String levelString = generate_level.generate(seed, defaultSteps, levelWidth, levelHeight, population, defaultMutationRate, defaultCrossoverRate, defaultElitismCount, defaultTournamentSize);
                long endTime = System.nanoTime();

                seeds.get("pop_size_" + population).add(seed);
                times.get("pop_size_" + population).add((int) ((endTime - startTime)));

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
            saveSeedsAndTimes(seeds, times);
        }

        for(int tournamentSize : tournamentSizes){
            // Create the levels folder
            levelsFolder = "levels" +  File.separator + "levels_tournament_size_" + tournamentSize;
            createFolder(levelsFolder);

            System.out.println("Generating levels for tournament_size = " + tournamentSize);

            // Generate the levels
            for(int i = 0; i < generations; i++){
                String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
                System.out.println("Generating " + outputLevelPath + "...");

                long seed = main_random.nextLong();

                long startTime = System.nanoTime();
                String levelString = generate_level.generate(seed, defaultSteps, levelWidth, levelHeight, defaultPopulationSize, defaultMutationRate, defaultCrossoverRate, defaultElitismCount, tournamentSize);
                long endTime = System.nanoTime();

                seeds.get("tournament_size_" + tournamentSize).add(seed);
                times.get("tournament_size_" + tournamentSize).add((int) ((endTime - startTime)));

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
            saveSeedsAndTimes(seeds, times);
        }

        for(float crossoverRate : crossoverRates){
            // Create the levels folder
            levelsFolder = "levels" +  File.separator + "levels_cross_rate_" + crossoverRate;
            createFolder(levelsFolder);

            System.out.println("Generating levels for crossover_rate = " + crossoverRate);

            // Generate the levels
            for(int i = 0; i < generations; i++){
                String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
                System.out.println("Generating " + outputLevelPath + "...");

                long seed = main_random.nextLong();

                long startTime = System.nanoTime();
                String levelString = generate_level.generate(seed, defaultSteps, levelWidth, levelHeight, defaultPopulationSize, defaultMutationRate, crossoverRate, defaultElitismCount, defaultTournamentSize);
                long endTime = System.nanoTime();

                seeds.get("cross_rate_" + crossoverRate).add(seed);
                times.get("cross_rate_" + crossoverRate).add((int) ((endTime - startTime)));

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
            saveSeedsAndTimes(seeds, times);
        }

        for(float mutationRate : mutationRates){
            // Create the levels folder
            levelsFolder = "levels" +  File.separator + "levels_mut_rate_" + mutationRate;
            createFolder(levelsFolder);

            System.out.println("Generating levels for mutation_rate = " + mutationRate);

            // Generate the levels
            for(int i = 0; i < generations; i++){
                String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
                System.out.println("Generating " + outputLevelPath + "...");

                long seed = main_random.nextLong();

                long startTime = System.nanoTime();
                String levelString = generate_level.generate(seed, defaultSteps, levelWidth, levelHeight, defaultPopulationSize, mutationRate, defaultCrossoverRate, defaultElitismCount, defaultTournamentSize);
                long endTime = System.nanoTime();

                seeds.get("mut_rate_" + mutationRate).add(seed);
                times.get("mut_rate_" + mutationRate).add((int) ((endTime - startTime)));

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
            saveSeedsAndTimes(seeds, times);
        }

        for(int elitismCount : elitismCounts){
            // Create the levels folder
            levelsFolder = "levels" +  File.separator + "levels_elitism_" + elitismCount;
            createFolder(levelsFolder);

            System.out.println("Generating levels for elitism_count = " + elitismCount);

            // Generate the levels
            for(int i = 0; i < generations; i++){
                String outputLevelPath = levelsFolder + File.separator + "level" + i + ".txt";
                System.out.println("Generating " + outputLevelPath + "...");

                long seed = main_random.nextLong();

                long startTime = System.nanoTime();
                String levelString = generate_level.generate(seed, defaultSteps, levelWidth, levelHeight, defaultPopulationSize, defaultMutationRate, defaultCrossoverRate, elitismCount, defaultTournamentSize);
                long endTime = System.nanoTime();

                seeds.get("elitism_" + elitismCount).add(seed);
                times.get("elitism_" + elitismCount).add((int) ((endTime - startTime)));

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
            saveSeedsAndTimes(seeds, times);
        }

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

    private static void saveSeedsAndTimes(Dictionary<String, List<Long>> seeds, Dictionary<String, List<Integer>> times) {
        Gson gson = new Gson();
        String seedsJson = gson.toJson(seeds);
        String timesJson = gson.toJson(times);

        try {
            FileWriter seedsFile = new FileWriter("seeds.json");
            seedsFile.write(seedsJson);
            seedsFile.close();
        } catch (Exception e) {
            System.err.println("ERROR: Could not write to file seeds.json\n" + e);
            System.exit(1);
        }

        try {
            FileWriter timesFile = new FileWriter("times.json");
            timesFile.write(timesJson);
            timesFile.close();
        } catch (Exception e) {
            System.err.println("ERROR: Could not write to file times.json\n" + e);
            System.exit(1);
        }
    }
}
