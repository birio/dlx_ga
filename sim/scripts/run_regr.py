#!/usr/bin/python

import os
import sys
import random

# ./run_regr.py NUM_OF_TESTS_IN_THE_REGRESSION
# assume that sim/tb/defines.sv and rtl/common/rom.v already are set for generated_test.hex
# - gen the seed
# - build only once
# - generate the test
# - run the test
# - generated asm are not saved

numb_of_tests = int(sys.argv[1])

build_str = "export TIMESCALE='1ns/10ps' ; vlog -timescale $TIMESCALE -f ../srclist/udlx_test.srclist ;"
os.system(build_str)

for i in range(0, numb_of_tests):
   seed = random.choice([j for j in range(0, 2**16)])
   input_test = "user_test" # + str(i)
   output_test = "gen_test_" + str(i) + ".asm"
   os.system("./../random_gen/generator.py " + str(seed) + " -t " + str(input_test) + " -o " + str(output_test))
   os.system("java -jar ../../compiler/Mars4_4.jar a dump .text HexText ../../sim/tests/generated_test.hex generated_test.asm")
   os.system("vsim  -c -do \"run -all; exit\" work.udlx_tb")
