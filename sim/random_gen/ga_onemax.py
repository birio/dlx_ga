#!/usr/bin/python

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
import argparse

import pdb

from deap import base
from deap import creator
from deap import tools

def MutFlipList (ind, indpb, n):
  for i in range(0, n):
    if random.random() < indpb:
      lines = generator.gen_line()
      ind[i] = lines
  return ind,

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

number_of_lines = 100
test_value = "FORWARDS"

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
       for j in range (0, len(individual[i])):
         line = "".join(individual[i][j])
         test_file.write("\t")
         test_file.write(line)
         test_file.write("\n")
    for i in range(0, 10):
       test_file.write("NOP")
       test_file.write("\n")
    test_file.close()

    # rm previous .hex
    os.system("rm ../tests/generated_test.hex")
    file_name = "generated_test.asm"
    # compile the test corresponding to the individual
    os.system("java -jar ../../compiler/Mars4_4.jar a dump .text HexText ../../sim/tests/generated_test.hex " + str(file_name))
    ret_value = os.system("ls ../tests/generated_test.hex")

    if ret_value != 0:
       raise ValueError("compiler returns an error");

    # run the test
    # REVISIT ensure that a fail will block the regression
    # REVISIT print test number
    print ("run the test")
    os.system("vsim -c -do \"run -all; exit\" work.udlx_tb > temp_vsim.log")

    # the test output is print in regs_out: parse it and compute the fitness value
    # the fitness value is the same of the content of all registers, which is printed in regs_out
    # REF register[i]: xx
    acc = 0
    if test_value == "REGS_OUT":
       read_regs = open("regs_out", 'r')
       lines = read_regs.readlines()
       for i in range(0, len(lines)):
          acc += int(lines[i])
    else:
       forw = open("forw", 'r')
       lines = forw.readlines()
       acc += float(lines[0])

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

    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="set parameters for rapid regression")
    parser.add_argument('--test', help='chose between REGS_OUT and FORWARDS')
    args = parser.parse_args()

    # main parameters of the algorithm
    n_gen = 40
    n_pop = 300
    patt_prct = .05

    if args.quick:
       print "quick regression selected"
       n_gen = 4
       n_pop = 10
       patt_prct = .3
       weights.test_weights_d["prob_opcode_addi"]    = weights.cell(0, 100, 0)
       weights.test_weights_d["prob_opcode_subu"]    = weights.cell(0, 100, 0)
       weights.test_weights_d["prob_opcode_and"]     = weights.cell(0, 100, 0)
       weights.test_weights_d["prob_opcode_andi"]    = weights.cell(0, 100, 0)
       weights.test_weights_d["prob_opcode_or"]      = weights.cell(0, 100, 0)
       weights.test_weights_d["prob_opcode_ori"]     = weights.cell(0, 100, 0)
       weights.test_weights_d["numb_of_regs_to_use_max_value"] = 3
       weights.test_weights_d["numb_of_regs_to_use"] = random.choice([i for i in range (3, weights.test_weights_d["numb_of_regs_to_use_max_value"]+1)])

    global test_value
    if args.test: 
       print "test is set to ", args.test
       if args.test not in ["FORWARDS", "REGS_OUT"]:
         print "test is invalid: test is assigned to FORWARDS"
       else:
         test_value = args.test
    else:
       print "test is not set: default is FORWARDS"

    # rm previous .hex if present from other tests eventually
    os.system("rm ../tests/generated_test.hex")

    print "build the DUT"
    build_str = "export TIMESCALE='1ns/10ps' ; vlog -timescale $TIMESCALE -f ../srclist/udlx_test.srclist  +define+" + str(test_value) + ";"
    os.system(build_str)
    weights.set_list()

    # create an initial population of n_pop individuals
    pop = toolbox.population(n=n_pop)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    #
    # NGEN  is the number of generations for which the
    #       evolution runs
    CXPB, MUTPB, NGEN = 0.5, 0.2, n_gen
    PATT_PRCT = patt_prct

    fp_rep_seqs = open("rep_seqs", "w")
    stats_file = open("stats_file", "w") 
    print("Start of evolution")
    stats_file.write("Start of evolution\n")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    stats_file.write("  Evaluated %i individuals\n" % len(pop))
    
    dict_seqs=[]
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        stats_file.write("-- Generation %i --\n" % g)

        # select an arbitrary portion of the population
        temp_offspring = tools.selBest(pop, int(len(pop)*PATT_PRCT))
        temp_offspring = list(map(toolbox.clone, temp_offspring))
        min_temp_valid = (min([pop[i].fitness.values[0] for i in range(0, len(pop))])) >= 50 # means greater than the 50 prct of the possible maximum value

        # REVISIT fixed size
        # search for a pattern

        size = 4
        all_seqs=[]
        rep_seqs=[]
        if min_temp_valid and len(dict_seqs) < 1000:
           for j in range(0, len(temp_offspring)):
              cnct_ind = temp_offspring[j][:]
              for i in range(0, len(cnct_ind)-size+1):
                 if (cnct_ind[i:i+size] in all_seqs) and not (cnct_ind[i:i+size] in dict_seqs):
                    rep_seqs.append([k[0] for k in cnct_ind[i:i+size]])
                    dict_seqs.append([k[0] for k in cnct_ind[i:i+size]])
                 else:
                    all_seqs.append(cnct_ind[i:i+size])

        # add the pattern in the generator weight dictionary
        # do not add twice the same sequence
        if len(rep_seqs) != 0:
           print ("identified a repeated sequence\n")
           fp_rep_seqs.write("identified a repeated sequence\n")
           # for i in range(0, len(rep_seqs)):
           for i in rep_seqs:
              seq_str = "multi__" + "".join(str(j + "__") for j in i)
           weights.test_weights_d[seq_str] = weights.cell(0, 100, 10) # the generator will handle it
           fp_rep_seqs.write(seq_str)
           fp_rep_seqs.write("\n")

        
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


# REVISIT smarter  ^C effect
# REVISIT files with smarter path definition
# TODO print seed generated at the begginning of the regr, and then pass it as an argument
# TODO post mortem debug

# TODO review mutation probability
# TODO use prct value for fitness in order to add other statistics easly
