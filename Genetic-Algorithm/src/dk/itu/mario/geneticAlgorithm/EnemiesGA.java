
package dk.itu.mario.geneticAlgorithm;

import java.util.Arrays;
import java.util.Random;

public class EnemiesGA extends GeneticAlgorithm {
    
	private int tournamentSize;
	private int chromossomeSize;
    private float desiredSparseness;
        
    private float maxFitness;
        
	public EnemiesGA(int populationSize, int chromossomeSize, float mutationProbability, float crossOverProbability, int eliteSize, int tournamentSize, float desiredSparseness, int stopCriteria) {
		
		super(populationSize, mutationProbability, crossOverProbability, eliteSize, stopCriteria);
		
		this.tournamentSize = tournamentSize;
		this.chromossomeSize = chromossomeSize;
		this.desiredSparseness = desiredSparseness;
                
		calcMaxFitness();
             
	}

	protected void calcMaxFitness()
    {
        int[] maxSparsenessChromossome = new int[this.chromossomeSize/EnemiesIndividual.ENEMIES_BLOCKS_SIZE];
        
    	maxSparsenessChromossome[0] = 1;
    	maxSparsenessChromossome[this.chromossomeSize/EnemiesIndividual.ENEMIES_BLOCKS_SIZE - 1] = 1;    
        
        EnemiesIndividual ind = new EnemiesIndividual(chromossomeSize/EnemiesIndividual.ENEMIES_BLOCKS_SIZE, maxSparsenessChromossome);
        maxFitness = ind.Sparseness(maxSparsenessChromossome) * maxSparsenessChromossome.length;
                     
        System.out.println("maxFitness: " + maxFitness);
    }

	@Override
	protected void selectPopulation() {
		
		Individual selectedPopulation[] = Tournament(population, tournamentSize);
		
		for(int i = 0; i < selectedPopulation.length; i++)
		{
			matingPool[i] =  selectedPopulation[i];
		}
	}

	@Override
	protected void initPopulation() {
		
		for(int i = 0; i < population.length; i++) {
			
			population[i] = new EnemiesIndividual(chromossomeSize, desiredSparseness, maxFitness);
		}
		
		for(int i = 0; i < matingPool.length; i++) {
			
			matingPool[i] = new EnemiesIndividual(chromossomeSize, desiredSparseness, maxFitness);
		}
		
	}

	@Override
	protected void groupPopulation() {
		// TODO Auto-generated method stub
		
	}

	@Override
	protected void crossOver() {
		
		Random rand = new Random();
		
		//A 1-point crossover
		for(int i = 0; i < matingPool.length/2; i += 2)
		{
			if(rand.nextFloat() < crossOverProbability)
			{
				EnemiesIndividual son1 = new EnemiesIndividual(chromossomeSize, desiredSparseness, maxFitness);
				EnemiesIndividual son2 = new EnemiesIndividual(chromossomeSize, desiredSparseness, maxFitness);
	                        
				onePointCrossover(matingPool[i], matingPool[i + 1], son1, son2);
				
				matingPool[i] = son1;
				matingPool[i + 1] = son2;
			}
		}
		
	}

	@Override
	protected void mutation() {
		// TODO Auto-generated method stub
		
	}
    
}
