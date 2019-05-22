import numpy as np
import random
import matplotlib.pyplot as plt

class board_info():
    def __init__(self):
        self.board = None 
        self.fitness = None

    def setBoard(self, val):
        self.board = val
    
    def setFitness(self, val):
        self.fitness = val

    #returns a randomized chess board with 8 queens, one in each column
    def randomBoard(self):
        initBoard = np.random.randint(8, size=8) 
        initBoard
        return initBoard
    
    #get the chessboard current fitness
    def getFitness(self):
        clashes = 0
        diag_clashes = 0
        #horizontal clashes
        row_clashes = abs(len(self.board)) - len(np.unique(self.board))
        #diagonal clashes
        for i in range(len(self.board)):
            for j in range(i, len(self.board)):
                if i != j:
                    dx = abs(i-j)
                    dy = abs(self.board[i] - self.board[j])
                    if(dx == dy):
                        diag_clashes += 1

        clashes += row_clashes + diag_clashes
        return 28-clashes
    
    #random mutation
    def mutate(self, muta):
        if random.randint(0, 99) <= muta:
            index = random.randint(0,7)
            number = random.randint(0,7)
            self.board[index] = number
        
        self.setFitness(self.getFitness())

class queen_pop():
    def __init__(self):
        self.population = [] 
        self.fitness_sum = 0
        self.fitness_avg = 0

    #create a population of len, and set each board's fitness
    def populate(self, len):
        for i in range(len):
            temp_board = board_info()
            temp_board.setBoard(temp_board.randomBoard())
            temp_board.setFitness(temp_board.getFitness())
            self.population.append(temp_board)

    #get the fitness sum for the whole population in current generation
    def getFitnessSum(self):
        return sum(chromosome.fitness for chromosome in self.population)
    
    #find the average fitness for a population in current generation
    def getFitnessAvg(self):
        return self.fitness_sum/len(self.population)

    def printAllInfo(self):
        for each in self.population:
            print(each.board, end='')
            print('Fitness: %2d' %(each.fitness))

    

    #find the probability distribution based on fitness for individual boards of a population
    def dist_prob(self):
        temp_dist = []
        for chromosome in self.population:
            temp_dist.append(chromosome.fitness/self.fitness_sum)
        return temp_dist

    #cross over two genes at random location depending on distribution probability. 
    def crossOver(self, len):
        #get distribution probablity for each board
        fitness_dist = self.dist_prob()
        #create a mapping of the length of population
        pop_map = np.arange(len)
        #find two parent mappings depending on distribution
        cross_parents = np.random.choice(pop_map, 2, p=fitness_dist)
        #create two new childs to hold crossover
        child_one = board_info()
        child_two = board_info()
        
        #copy parent board into child
        child_one.setBoard(self.population[cross_parents[0]].board.copy())
        child_two.setBoard(self.population[cross_parents[1]].board.copy())

        #randomly select a place to splice, and swap the values
        c = np.random.randint(8)
        child_one.board[c:], child_two.board[c:] = child_two.board[c:], child_one.board[c:].copy()
        child_one.setFitness(child_one.getFitness())
        child_two.setFitness(child_two.getFitness())
        return (child_one, child_two)

    #check if goal state is reached -- no queens attacking one another and display it
    def finish(self):
        goal = False
        #print('Average Fitness: %.2f' %(self.fitness_avg))
        for each in self.population:
            if each.fitness == 28:
                print(each.board, end='')
                print('fitness value: %2d' %(each.fitness))
                goal = True
        return goal
    
    #genetic algorithm wrapper
    def genetic_algo(self, popSize, mutaProp):
        plot_data = []
        iteration = 3000 
        self.populate(popSize)
        self.fitness_sum = self.getFitnessSum()
        self.fitness_avg = self.getFitnessAvg()
        for count in range(iteration):
            plot_data.append(self.fitness_avg)
            #print('ITERATION: %4d' %(count))
            if self.finish() == True:
                print('SOLUTION FOUND at ITERATION: %4d' %(count))
                break
            i = 0
            new_pop = []
            while i < popSize/2:
                child1, child2 = self.crossOver(popSize)
                child1.mutate(mutaProp)
                child2.mutate(mutaProp)
                new_pop.append(child1)
                new_pop.append(child2)
                i += 1

            self.population = new_pop
            self.fitness_sum = self.getFitnessSum()
            self.fitness_avg= self.getFitnessAvg()
        return plot_data


def main():

    queens1 = queen_pop()
    queens2 = queen_pop()
    queens3 = queen_pop()
    #queens4 = queen_pop()
    #queens5 = queen_pop()
    #queens6 = queen_pop()

    popSize1 = 100
    #popSize2 = 300
    #popSize3 = 500
    mutaprop1 = 5
    #mutaprop2 = 7
    #mutaprop3 = 10
    #mutaprop4 = 3

    plot_data1 = queens1.genetic_algo(popSize1,mutaprop1)
    #plot_data2 = queens2.genetic_algo(popSize2, mutaprop1)
    #plot_data3 = queens3.genetic_algo(popSize3, mutaprop1)

    #plot_data4 = queens4.genetic_algo(popSize1, mutaprop4)
    #plot_data5 = queens5.genetic_algo(popSize1, mutaprop2)
    #plot_data6 = queens6.genetic_algo(popSize1, mutaprop3)


    #plt.title("Fitness Average at each Iteration to solve 8-Queens")
    #plt.xlabel("Iterations")
    #plt.ylabel("Fitness Average")
    #plt.plot(plot_data1, label='population size = 100, gene mutation prob = 5%')
    #plt.plot(plot_data2, label='population size = 300, gene mutation prob = 5%')
    #plt.plot(plot_data3, label='population size = 500, gene mutation prob = 5%')
    #plt.legend(loc='upper left')
    #plt.savefig('foo.png')

    #plt.title("Fitness Average at each Iteration to solve 8-Queens")
    #plt.xlabel("Iterations")
    #plt.ylabel("Fitness Average")
    #plt.plot(plot_data4, label='population size = 100, gene mutation prob = 3%')
    #plt.plot(plot_data5, label='population size = 100, gene mutation prob = 7%')
    #plt.plot(plot_data6, label='population size = 100, gene mutation prob = 10%')
    #plt.legend(loc='upper left')
    #plt.savefig('mutaprob.png')
    return 0


if __name__ == '__main__':
    main()