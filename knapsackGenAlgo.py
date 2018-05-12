"""
* Genetic Algorithm applied to the Knapsack Problem (an NP complete problem)
* Version: Python 3.5
*
* Description: A problem in combinatorial optimization: Given a set of items,
* each with a weight and a value, determine which items to include
* in a collection so that the total weight is less than or equal to a given
* limit and the total value is as large as possible.
*
* Known issues: Genetic algorithms are known to get stuck at local maxima, and
* thus can produce incomplete and suboptimal results. This has been mitigated by
* implementing an early termination condition using a max fitness score
* heuristic.
"""

import random

"""
* Box class: the items with various weights and values which are contained in 
*            chromosomes.

"""

class Box:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value
"""
* Population: a set of permutated of chromosomes, initialized to a pre-set size.
"""
class Population:
    def __init__(self, pop_size):
        self.population = []
        self.size = pop_size

    def generate_population(self, box_list):
        for i in range(0, self.size):
            chrom = Chromosome(box_list)
            print("Fitness: ", str(chrom.fitness), "\n")
            self.population.append(chrom)

    """
    * get_fittest: sorts the population according to best fit score (descending)
    """
    def get_fittest(self):
        self.population = sorted(self.population,
                                 key=lambda x: x.fitness, reverse = True)

    """
    * cull: operation which halves the generated population, removing the weakest 
    *       candidates as measured by the fitness score. 
    """
    def cull(self):
        self.get_fittest()
        length = int((len(self.population)/2))
        self.population = self.population[:length]
        self.size = length

    """
    * print_pop: a function that prints the population for verification. 
    """
    def print_pop(self):
        for i in self.population:
            print("Total weight: ", i.total_weight)
            for j in i.boxes:
                print(j.name, j.weight, j.value)
            print("Fitness: ", i.fitness, "\n")

"""
* Chromosome: a group of boxes who's attributes include a total weight, total
*             value, and fitness score. 
"""
class Chromosome:
    def __init__(self, boxes):
        self.boxes = self.gen_chromosome(boxes)
        self.total_weight = self.sum_weight()
        self.total_value = self.sum_value()
        self.fitness = self.calc_fitness()

    """
    * sum_weight: a helper function that sums the weights of all the boxes in 
    *             the chromosome. 
    """
    def sum_weight(self):
        sum = 0
        for i in self.boxes:
            sum += i.weight

        return sum

    """
    * sum_value: a helper function that sums the values of all the boxes in 
    *            the chromosome. 
    """
    def sum_value(self):
        sum = 0
        for i in self.boxes:
            sum += i.value

        return sum

    """
    * gen_chromosome: generates a chromosome, which is a random permutation of 
    *                 boxes
    """

    def gen_chromosome(self, box_list):
        chrom = []
        if len(box_list) == 0:
            return chrom

        random.shuffle(box_list)
        weight = 0
        for i in range(0,3):
            chrom.append(box_list[i])
            print(box_list[i].name, box_list[i].weight, box_list[i].value)
            weight += box_list[i].weight
        print("Weight: ", weight)
        return chrom

    """
    * calc_fitness: determines the fitness score by applying rewards for 
    *                higher values and maximum weight and penalties for being
    *                overweight
    """

    def calc_fitness(self):
        fit_score = 0
        ideal_weight_bonus = 2

        weight = 0
        for i in self.boxes:
            fit_score += i.value
            weight += i.weight
        if weight > 120:
            fit_score -= int((weight - 120)/2)
        elif weight == 120: fit_score += ideal_weight_bonus


        return fit_score

"""
* crossover: an essential algorithm for providing genetic variability. The 
*            function accepts two chromosomes and mates them, producing a hybrid
*            of their box attributes. 
"""
def crossover(x, y):
    temp = []
    if dupe_check(x,y):
        return x

    baby = Chromosome(temp)
    temp1 = sorted(x.boxes, key=lambda x: x.name)
    temp2 = sorted(y.boxes, key=lambda x: x.name)

    for i in range(0,len(temp1)):
        which = random.randint(0,1)
        if which == 0:
            if temp1[i] in baby.boxes:
                baby.boxes.append(temp2[i])
            else:
                baby.boxes.append(temp1[i])
        else:
            if temp2[i] in baby.boxes:
                baby.boxes.append(temp1[i])
            else:
                baby.boxes.append(temp2[i])

    return baby

"""
* crossover: a less essential algorithm for providing genetic variability. The 
*            function accepts a single chromosome after it has been crossed-over
*            and mutates its boxes (provided that the mutation probability is
*            satisfied. 
"""
def mutate(baby, probability, boxes):
    temp_list = boxes[:]
    for i in baby.boxes:
        if i in temp_list:
            temp_list.remove(i)

    for j in range(0,len(baby.boxes)):
        if mutant_prob(probability):
            baby.boxes[j] = random.choice(temp_list)
            temp_list.remove(baby.boxes[j])

    return baby

"""
* mutant_prob : a helper function which returns a bool value, depending upon
*               whether or not a mutation has occured. The function accepts a 
*               probability that the mutation will occur. 
"""
def mutant_prob(probability):
    probability *= 10
    temp = random.randint(0,10)

    if temp <= probability:
        return True
    return False

"""
* dupe_check: a helper function for the mutation function which makes sure that
*             no chromosome has more than one of the same object (ie no dupes).
"""
def dupe_check(x,y):
    temp1 = sorted(x.boxes, key=lambda x: x.name)
    temp2 = sorted(y.boxes, key=lambda x: x.name)

    if temp1 == temp2:
        return True
    return False

"""
* genetic_algo: the genetic algorithm generates a population of chromosomes, 
*               uses crossover and mutation functions to generate a new 
*               generation, and returns an optimal solution chromosome. 
"""
def genetic_algo(population, boxes):
    nextgen = Population(population.size)
    MUTANT_PROB = .30
    MAX_SCORE = 22
    best = None

    for i in range(0,5):
        for j in range(0,nextgen.size):
            # x and y are chomosomes
            x = random.choice(population.population)
            y = random.choice(population.population)

            if x == y:
                while x == y:
                    y = random.choice(population.population)

            child = crossover(x,y)
            child = mutate(child, MUTANT_PROB, boxes)

            child.fitness = child.calc_fitness()
            child.total_weight = child.sum_weight()
            child.total_value = child.sum_value()
            nextgen.population.append(child)

        fittest = return_fittest(nextgen)
        if fittest.fitness == MAX_SCORE:
            best = return_fittest(nextgen)
            print("OPTIMAL RESULT FOUND IN", i+1, "CYCLES.")
            return best

        population.population = nextgen.population[:]
        population.cull()
        print("NEW GENERATION\n-----------------")
        population.print_pop()
        nextgen.population.clear()

    return best

"""
* return_fittest: a wrapper function that returns the most fit chromosome of a
*                 population generation.
"""
def return_fittest(population):
    population.get_fittest()
    return population.population[0]

##### Driver #####

boxes = []

a = Box('a',20, 6)
boxes.append(a)
b = Box('b',30, 5)
boxes.append(b)
c = Box('c',60, 8)
boxes.append(c)
d = Box('d',90, 7)
boxes.append(d)
e = Box('e',50, 6)
boxes.append(e)
f = Box('f',70, 9)
boxes.append(f)
g = Box('g',30, 4)
boxes.append(g)

print("Below are the boxes which will be used: ")
for i in boxes:
    print(i.name, i.weight,i.value)
print("---------------------------\n")
POP_SIZE = 35

population = Population(POP_SIZE)
population.generate_population(boxes)


population.print_pop()

best = genetic_algo(population,boxes)
print("WINNER: value:", best.total_value, "fitness score:",  best.fitness,
      "weight:", best.total_weight)
for x in best.boxes:
    print(x.name, x.weight, x.value)







