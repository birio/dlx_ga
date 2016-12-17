#!/usr/bin/python

import sys
import random
import importlib

# generator includes
import opcodes
import weights

def gen_line():
 
   #random.seed(seed)
   # chose an instr from the weighted list
   asm_line = random.sample(weights.weighted_opcodes_l, 1)
   
   
   # available registers to use in the test
   trues_l  = [True]  * weights.test_weights_d["numb_of_regs_to_use"]
   falses_l = [False] * (32 - weights.test_weights_d["numb_of_regs_to_use"])
   prob_use_reg_l = trues_l + falses_l
   random.shuffle(prob_use_reg_l)
   available_regs_l = [ i for i in range(0, 32) if prob_use_reg_l[i] == True ]
   # print "available_regs_l"
   # print available_regs_l 
   
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
   
   # if i in labels_lines_l:
   #    label_str = "label_" + str(printed_label) + ":" 
   #    test_file.write(label_str)
   #    test_file.write("\n")
   #    printed_label += 1

   return line,

def main():
   # ./generator.py SEED [-t <user_test> -o <generated_asm.asm>]
   seed = sys.argv[1]
   random.seed(seed)
   
   # if -t is present, the next arg is the user_test
   if ("-t" in sys.argv):
      user_test = sys.argv[sys.argv.index("-t")+1]
      # check if by errors the user test ends by ".py", delete it
      if user_test.endswith(".py"):
         user_test = user_test[user_test:-3]
      importlib.import_module(user_test, package=None)
      
   # if -o is present, the next arg is the name of output asm file
   if ("-o" in sys.argv):
      file_name = sys.argv[sys.argv.index("-o")+1]
   else:
      file_name = "generated_test.asm"
      
   
   # fixed value
   number_of_lines = 100
   
   # labels used in the test
   num_of_labels = random.choice([i for i in range(0, weights.max_num_of_labels)])
   labels_lines_l = random.sample([i for i in range(0, number_of_lines)], num_of_labels)
   labels_lines_l.sort()
   printed_label = 0
   
   print "number_of_lines = " + str(number_of_lines)
   
   # methods the set the opcodes and imm list based on user_test weights
   weights.set_list()
   # print weights.weighted_opcodes_l 
   
   test_file = open(file_name, 'w+')
   
   # init all registers
   for i in range (0, 32):
      asm_line = "\t addi $" + str(i) + ", $0, 0\n"
      test_file.write(asm_line)
   
   for i in range (0, number_of_lines):
      line = gen_line()
      test_file.write("\t")
      test_file.write(line[0])
      test_file.write("\n")
   for i in range(0, 10):
      test_file.write("NOP")
      test_file.write("\n")
   
   # for i in range(number_of_lines, 2**32):
   #    label_str = "j label_" + str(random.choice([ i for i in range(0, num_of_labels)]))
   #    test_file.write(label_str)
   #    test_file.write("\n")
   
   test_file.close()

if __name__ == "__main__":
    main()
