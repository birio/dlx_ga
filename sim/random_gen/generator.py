#!/usr/bin/python

import sys
import random
import importlib

# generator includes
import opcodes
import weights

# ./generator.py SEED
seed = sys.argv[1]
random.seed(seed)

# if argv[2] is present, import the python file associated
if len(sys.argv) == 3:
   var = sys.argv[2]
   importlib.import_module(var, package=None)

# fixed value
number_of_lines = 10

# available registers to use in the test
trues_l  = [True]  * weights.test_weights_d["numb_of_regs_to_use"]
falses_l = [False] * (32 - weights.test_weights_d["numb_of_regs_to_use"])
prob_use_reg_l = trues_l + falses_l
random.shuffle(prob_use_reg_l)
available_regs_l = [ i for i in range(0, 32) if prob_use_reg_l[i] == True ]

# labels used in the test
num_of_labels = random.choice([i for i in range(0, weights.max_num_of_labels)])
labels_lines_l = random.sample([i for i in range(0, number_of_lines)], num_of_labels)
labels_lines_l.sort()
printed_label = 0

print "available_regs_l"
print available_regs_l 

print "number_of_lines = " + str(number_of_lines)

weights.set_list()
print weights.weighted_opcodes_l 

test_file = open('generated_test.asm', 'w+')

for i in range (0, number_of_lines):
   # chose an instr from the weighted list
   asm_line = random.sample(weights.weighted_opcodes_l, 1)
 
   if str(asm_line[0]) in opcodes.r_types_l:
      r0 = random.choice(available_regs_l)
      r1 = random.choice(available_regs_l)
      r2 = random.choice(available_regs_l)
      line = str(asm_line[0]) + "\t $" + str(r0) + ",\t $" + str(r1) + ",\t $" + str(r2)

   elif str(asm_line[0]) in opcodes.i_types_l:
      r0 = random.choice(available_regs_l)
      r1 = random.choice(available_regs_l)
      if (asm_line[0] == "slti") or (asm_line[0] == "sltiu"):
         imm = random.choice(weights.test_weights_d["imm_value_15_l"])
      else:
         imm = random.choice(weights.test_weights_d["imm_value_16_l"])
      line = str(asm_line[0]) + "\t $" + str(r0) + ",\t $" + str(r1) + ",\t " + str(imm)

   elif str(asm_line[0]) in opcodes.s_i_types_l:
      r0 = random.choice(available_regs_l)
      r1 = random.choice(available_regs_l)
      imm = random.choice(weights.test_weights_d["imm_value_5_l"])
      line = str(asm_line[0]) + "\t $" + str(r0) + ",\t $" + str(r1) + ",\t " + str(imm)

   elif str(asm_line[0]) in opcodes.load_types_l:
      r0 = random.choice(available_regs_l)
      r1 = random.choice(available_regs_l)
      imm = random.choice(weights.test_weights_d["imm_value_16_l"])
      line = str(asm_line[0]) + "\t $" + str(r0) + ",\t " + str(imm) + "($" + str(r1) + ")"

   elif str(asm_line[0]) in opcodes.b_types_l:
      r0 = random.choice(available_regs_l)
      r1 = random.choice(available_regs_l)
      b_label = "label_" + str(random.choice([j for j in range (0, num_of_labels)]))
      line = str(asm_line[0]) + "\t $" + str(r0) + ",\t $" + str(r1) + ",\t " + str(b_label)

   elif str(asm_line[0]) in opcodes.l_i_types_l:
      r0 = random.choice(available_regs_l)
      if (asm_line[0] == "lui"):
         imm = random.choice(weights.test_weights_d["imm_value_16_l"])
      else: # "li"
         imm = int(random.random()*2**32) 
      line = str(asm_line[0]) + "\t $" + str(r0) + ",\t " + str(imm)

   elif str(asm_line[0]) in opcodes.move_types_l:
      r0 = random.choice(available_regs_l)
      r1 = random.choice(available_regs_l)
      line = str(asm_line[0]) + "\t $" + str(r0) + "\t $" + str(r1)

   elif str(asm_line[0]) in opcodes.j_types_l:
      j_label = "label_" + str(random.choice([j for j in range (0, num_of_labels)]))
      line = str(asm_line[0]) + "\t " + str(j_label)

   elif str(asm_line[0]) in opcodes.r_j_types_l:
      r0 = random.choice(available_regs_l)
      line = str(asm_line[0]) + "\t $" + str(r0)

   else:
      line = str(asm_line[0])

   if i in labels_lines_l:
      label_str = "label_" + str(printed_label) + ":" 
      test_file.write(label_str)
      test_file.write("\n")
      printed_label += 1

   test_file.write("\t")
   test_file.write(line)
   test_file.write("\n")

for i in range(0, 10):
   test_file.write("NOP")
   test_file.write("\n")

# for i in range(number_of_lines, 2**32):
#    label_str = "j label_" + str(random.choice([ i for i in range(0, num_of_labels)]))
#    test_file.write(label_str)
#    test_file.write("\n")

test_file.close()
