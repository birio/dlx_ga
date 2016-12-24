# DEFINES
# attr_instr  : gene - an instruction - string
# individual  : a generate asm test - list
# population  : list of asm tests

# always use lists; converto to file only when eval is called;
# inside eval the is run and the output file is done

import random
import weights
import re
import os
import generator

import pdb

from deap import base
from deap import creator
from deap import tools

def MutFlipList (ind, indpb, n): 
  for i in range(0, n):
    # if tools.mutFlipBit(ind, indpb):
    if random.random() < indpb:
      ind[i] = generator.gen_line()
  return ind,
#  return [tools.mutFlipBit(ind[b], indpb) for b in range(0, n)]

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

number_of_lines = 100

# Attribute generator 
#                      define 'attr_instr' to be an attribute ('gene')
#                      which corresponds to the wight of the selected item
toolbox.register("attr_instr", generator.gen_line)

# Structure initializers
#                         define 'individual' to be an individual
#                         consisting of a generated asm file base on
#                         'attr_instr' of all items
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_instr, number_of_lines)

# define the population to be a list of individuals
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# the goal ('fitness') function to be maximized
def evalOneMax(individual):


    # transform the list to file .asm
    file_name = "generated_test.asm"
    test_file = open(file_name, 'w+')
    # for each element of the individual list
    for i in range (0, len(individual)):
       line = "".join(individual[i])
       test_file.write("\t")
       test_file.write(line)
       test_file.write("\n")
    for i in range(0, 10):
       test_file.write("NOP")
       test_file.write("\n")
    test_file.close()

    # compile the test corresponding to the individual
    os.system("java -jar ../../compiler/Mars4_4.jar a dump .text HexText ../../sim/tests/generated_test.hex " + str(file_name))

    # run the test
    os.system("vsim  -c -do \"run -all; exit\" work.udlx_tb")

    # the test output is print in regs_out: parse it and compute the fitness value
    # the fitness value is the same of the content of all registers, which is printed in regs_out
    # REF register[i]: xx
    # pdb.set_trace()
    acc = 0
    read_regs = open("regs_out", 'r') 
    lines = read_regs.readlines()
    for i in range(0, len(lines)):
       acc += int(lines[i])

    return acc,

#----------
# Operator registration
#----------
# register the goal / fitness function
toolbox.register("evaluate", evalOneMax)

# register the crossover operator
toolbox.register("mate", tools.cxTwoPoint)

# register a mutation operator with a probability to
# flip each attribute/gene of 0.05
toolbox.register("mutate", MutFlipList, indpb=0.05, n=number_of_lines)

# operator for selecting individuals for breeding the next
# generation: each individual of the current generation
# is replaced by the 'fittest' (best) of three individuals
# drawn randomly from the current generation.
toolbox.register("select", tools.selTournament, tournsize=3)

#----------


def main():

    print "build the DUT"
    build_str = "export TIMESCALE='1ns/10ps' ; vlog -timescale $TIMESCALE -f ../srclist/udlx_test.srclist ;"
    os.system(build_str)
    weights.set_list()

    # TODO fixed seed?
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=300)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    #
    # NGEN  is the number of generations for which the
    #       evolution runs
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40
   
    rep_seqs   = open("rep_seqs", "w")
    stats_file = open("stats_file", "w") 
    print("Start of evolution")
    stats_file.write("Start of evolution\n")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    stats_file.write("  Evaluated %i individuals\n" % len(pop))
    
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        stats_file.write("-- Generation %i --\n" % g)

        # select an arbitrary portion of the population
        # TODO for perf reasons, do select twice is not a good choice
        temp_offspring = toolbox.select(pop, len(pop)/3)
        temp_offspring = list(map(toolbox.clone, temp_offspring))

        # TODO fixed size
        # search for a pattern
        # pdb.set_trace()
        # ignore nop
        # for the moment, fixed size

        cnct_ind = [temp_offspring[i][0] for i in range(0, len(temp_offspring))]
        size = 2
        all_seqs=[]
        rep_seqs=[]
        for i in range(0, len(cnct_ind)-size+1):
           if len([ j for j in cnct_ind[i:i+size] if "nop" not in j]) == 0:
              if cnct_ind[i:i+size] in all_seqs:
                 rep_seqs.append(cnct_ind[i:i+size])
              else:
                 all_seqs.append(cnct_ind[i:i+size])

        # add the pattern in the generator weight dictionary
        # do not add twice the same sequence
        if len(rep_seqs) != 0:
           print ("identified a repeated sequence\n")
           rep_seqs.write("identified a repeated sequence\n")
           for i in range(0, len(rep_seqs)):
              seq_str = "multi_"
              seq_str = "".join(i for i in rep_seqs[0]).replace(" ", "_").replace("$", "").replace(",", "")
              test_weights_d[seq_str] = cell(0, 100, 10) # the generator will handle it
              rep_seqs.write(seq_str)
              rep_seqs.write("\n")

        
        weights.set_list()

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        stats_file.write("  Evaluated %i individuals\n" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
       
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        stats_file.write("  Min %s\n" % min(fits))
        print("  Max %s" % max(fits))
        stats_file.write("  Max %s\n" % max(fits))
        print("  Avg %s" % mean)
        stats_file.write("  Avg %s\n" % mean)
        print("  Std %s" % std)
        stats_file.write("  Std %s\n" % std)
    
    print("-- End of (successful) evolution --")
    stats_file.write("-- End of (successful) evolution --\n")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    stats_file.write("Best individual is %s, %s\n" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()