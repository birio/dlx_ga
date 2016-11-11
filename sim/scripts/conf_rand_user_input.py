import random
import os

#lists used for rangom generation
zero_100_l = [i for i in range(0, 100)]
three_33_l = [i for i in range(3, 33)]
zero_5bits_l = [i for i in range(0, 2**5)]
zero_15bits_l = [i for i in range(0, 2**15)]
zero_16bits_l = [i for i in range(0, 2**16)]
prob_opcode_l = ["prob_opcode_add", "prob_opcode_addi", \
"prob_opcode_sub", "prob_opcode_subi", "prob_opcode_and", "prob_opcode_andi", \
"prob_opcode_or", "prob_opcode_ori"] 

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
