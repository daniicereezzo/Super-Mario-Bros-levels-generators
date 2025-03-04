package dk.itu.mario.engine.util;

import java.util.Random;

public class PRNG {
    public static Random random;

    public static void setSeed(long seed) {
        random = new Random(seed);
    }
}
