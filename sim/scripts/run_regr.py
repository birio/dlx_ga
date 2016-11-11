#!/usr/bin/python

import os
import sys
import random

# import function for generating random user test
import conf_rand_user_input

# ./run_regr.py NUM_OF_TESTS_IN_THE_REGRESSION
# assume that sim/tb/defines.sv and rtl/common/rom.v already are set for generated_test.hex
# - gen the seed
# - build only once
# - generate the test
# - run the test

# user_test (one for each regression)
# generated_asm (NUM_OF_TESTS_IN_THE_REGRESSION)
# regs value (NUM_OF_TESTS_IN_THE_REGRESSION)

#number of tests in the regression is passed as argument
numb_of_tests = int(sys.argv[1])

#build the rtl
build_str = "export TIMESCALE='1ns/10ps' ; vlog -timescale $TIMESCALE -f ../srclist/udlx_test.srclist ;"
os.system(build_str)

seed = random.choice([j for j in range(0, 2**16)])
input_test = conf_rand_user_input.conf_user_test(seed)

for i in range(0, numb_of_tests):
   # move input_test to the generator.py directory
   os.system("mv " + str(input_test) + ".py ../random_gen/" + str(input_test) + ".py")
   # keep track of generated assembly test
   output_test = "gen_test_" + str(i) + ".asm"
   os.system("./../random_gen/generator.py " + str(seed) + " -t " + str(input_test) + " -o " + str(output_test))
   os.system("java -jar ../../compiler/Mars4_4.jar a dump .text HexText ../../sim/tests/generated_test.hex " + str(output_test))
   os.system("vsim  -c -do \"run -all; exit\" work.udlx_tb")
   # the tb generate the file regs_out: rename it with the test number
   os.system("mv regs_out regs_out_" + str(i))
