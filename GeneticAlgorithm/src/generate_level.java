import dk.itu.mario.MarioInterface.GamePlay;
import dk.itu.mario.level.Level;
import dk.itu.mario.level.generator.GALevelGenerator;
import dk.itu.mario.engine.util.PRNG;

public class generate_level {
    public static String generate(long seed, int steps, int levelWidth, int levelHeight, int populationSize, float mutationRate, float crossoverRate, int elitismCount, int tournamentSize) {
        GALevelGenerator clg = new GALevelGenerator();
        GamePlay gp = new GamePlay();
        
        PRNG.setSeed(seed);
        
        int stopCriteria = 50;
        Level level = (Level)clg.generateLevel(gp, levelWidth, levelHeight, populationSize, mutationRate, crossoverRate, elitismCount, tournamentSize, stopCriteria, steps);
        return level.FromBytesToTiles();
    }
}
