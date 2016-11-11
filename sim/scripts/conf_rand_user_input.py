import random
import os

#lists used for rangom generation
zero_100_l = [i for i in range(0, 100)]
three_33_l = [i for i in range(3, 33)]
zero_5bits_l = [i for i in range(0, 2**5)]
zero_15bits_l = [i for i in range(0, 2**15)]
zero_16bits_l = [i for i in range(0, 2**16)]
prob_opcode_l = ["prob_opcode_add", "prob_opcode_addi", "prob_opcode_addiu", "prob_opcode_addu", \
"prob_opcode_sub", "prob_opcode_subu", "prob_opcode_and", "prob_opcode_andi", "prob_opcode_nor", \
"prob_opcode_or", "prob_opcode_ori", "prob_opcode_xor", "prob_opcode_xori", "prob_opcode_sll", \
"prob_opcode_srl", "prob_opcode_sra", "prob_opcode_sllv", "prob_opcode_srlv", "prob_opcode_srav", \
"prob_opcode_slt", "prob_opcode_slti", "prob_opcode_sltiu", "prob_opcode_sltu", "prob_opcode_beq", \
"prob_opcode_bne", "prob_opcode_blt", "prob_opcode_bgt", "prob_opcode_ble", "prob_opcode_bge", \
"prob_opcode_j", "prob_opcode_jal", "prob_opcode_jr", "prob_opcode_jalr", "prob_opcode_move", \
"prob_opcode_lb", "prob_opcode_lbu", "prob_opcode_lh", "prob_opcode_lhu", "prob_opcode_lui", "prob_opcode_lw", \
"prob_opcode_li", "prob_opcode_la", "prob_opcode_sb", "prob_opcode_sh", "prob_opcode_sw"] 

def conf_user_test(seed):
   # configure input_test
   random.seed(seed)
   input_test = "random_user_test.py"
   ret_input_test = "random_user_test"
   f_in = open(input_test, "w")
   f_in.write("import weights")
   f_in.write("\n")
   for item in prob_opcode_l:
      in_string = "weights.test_weights_d[\"prob_opcode_add\"].set(" + str(random.choice(zero_100_l)) + ")"
      f_in.write(in_string)
      f_in.write("\n")
   in_string = "weights.test_weights_d[\"numb_of_regs_to_use_max_value\"] = " + str(random.choice(three_33_l)) 
   f_in.write(in_string)
   f_in.write("\n")
   in_string = "weights.test_weights_d[\"imm_value_5_max_value\"] = " + str(random.choice(zero_5bits_l))
   f_in.write(in_string)
   f_in.write("\n")
   in_string = "weights.test_weights_d[\"imm_value_15_max_value\"] = " + str(random.choice(zero_15bits_l)) 
   f_in.write(in_string)
   f_in.write("\n")
   in_string = "weights.test_weights_d[\"imm_value_16_max_value\"] = " + str(random.choice(zero_16bits_l)) 
   f_in.write(in_string)
   f_in.write("\n")
   f_in.close()
   
   return ret_input_test 
