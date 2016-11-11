import random

class cell:
   # weight can be le then max or ge then min
   # so max and min are feasible value for weight
   def __init__(self, v_min, v_max, v_weight = 0) :
      self.value_min = v_min
      self.value_max = v_max
      self.weight    = v_weight
   def set (self, v_weight) :
      self.weight    = v_weight

test_weights_d = {}

test_weights_d["prob_opcode_add"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_addi"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_addiu"]   = cell(0, 100, 10)
test_weights_d["prob_opcode_addu"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_sub"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_subu"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_and"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_andi"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_nor"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_or"]      = cell(0, 100, 10)
test_weights_d["prob_opcode_ori"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_xor"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_xori"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_sll"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_srl"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_sra"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_sllv"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_srlv"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_srav"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_slt"]     = cell(0, 100, 10)
test_weights_d["prob_opcode_slti"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_sltiu"]   = cell(0, 100, 10)
test_weights_d["prob_opcode_sltu"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_beq"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_bne"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_blt"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_bgt"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_ble"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_bge"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_j"]       = cell(0,   0,  0)
test_weights_d["prob_opcode_jal"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_jr"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_jalr"]    = cell(0,   0,  0)
test_weights_d["prob_opcode_move"]    = cell(0, 100, 10)
test_weights_d["prob_opcode_lb"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_lbu"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_lh"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_lhu"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_lui"]     = cell(0,   0,  0)
test_weights_d["prob_opcode_lw"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_li"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_la"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_sb"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_sh"]      = cell(0,   0,  0)
test_weights_d["prob_opcode_sw"]      = cell(0,   0,  0)

# must be greater than three
test_weights_d["numb_of_regs_to_use_max_value"] = 32
test_weights_d["numb_of_regs_to_use"] = random.choice([i for i in range (3, test_weights_d["numb_of_regs_to_use_max_value"]+1)])

# imm_value_5
test_weights_d["imm_value_5_max_value"] = 2**5+1
# imm_value_15
test_weights_d["imm_value_15_max_value"] = 2**15+1
# imm_value_16
test_weights_d["imm_value_16_max_value"] = 2**16+1

# between 1 and 100
max_num_of_labels = 1

# list from which chose an instruction
def set_list() :
   global weighted_opcodes_l 
   weighted_opcodes_l = (test_weights_d["prob_opcode_add"].weight    * ["add"]   +  
                         test_weights_d["prob_opcode_addi"].weight   * ["addi"]  +
                         test_weights_d["prob_opcode_addiu"].weight  * ["addiu"] +
                         test_weights_d["prob_opcode_addu"].weight   * ["addu"]  +
                         test_weights_d["prob_opcode_sub"].weight    * ["sub"]   +
                         test_weights_d["prob_opcode_subu"].weight   * ["subu"]  +
                         test_weights_d["prob_opcode_and"].weight    * ["and"]   +
                         test_weights_d["prob_opcode_andi"].weight   * ["andi"]  +
                         test_weights_d["prob_opcode_nor"].weight    * ["nor"]   +
                         test_weights_d["prob_opcode_or"].weight     * ["or"]    +
                         test_weights_d["prob_opcode_ori"].weight    * ["ori"]   +
                         test_weights_d["prob_opcode_xor"].weight    * ["xor"]   +
                         test_weights_d["prob_opcode_xori"].weight   * ["xori"]  +
                         test_weights_d["prob_opcode_sll"].weight    * ["sll"]   +
                         test_weights_d["prob_opcode_srl"].weight    * ["srl"]   +
                         test_weights_d["prob_opcode_sra"].weight    * ["sra"]   +
                         test_weights_d["prob_opcode_sllv"].weight   * ["sllv"]  +
                         test_weights_d["prob_opcode_srlv"].weight   * ["srlv"]  +
                         test_weights_d["prob_opcode_srav"].weight   * ["srav"]  +
                         test_weights_d["prob_opcode_slt"].weight    * ["slt"]   +
                         test_weights_d["prob_opcode_slti"].weight   * ["slti"]  +
                         test_weights_d["prob_opcode_sltiu"].weight  * ["sltiu"] +
                         test_weights_d["prob_opcode_sltu"].weight   * ["sltu"]  +
                         test_weights_d["prob_opcode_beq"].weight    * ["beq"]   +
                         test_weights_d["prob_opcode_bne"].weight    * ["bne"]   +
                         test_weights_d["prob_opcode_blt"].weight    * ["blt"]   +
                         test_weights_d["prob_opcode_bgt"].weight    * ["bgt"]   +
                         test_weights_d["prob_opcode_ble"].weight    * ["ble"]   +
                         test_weights_d["prob_opcode_bge"].weight    * ["bge"]   +
                         test_weights_d["prob_opcode_j"].weight      * ["j"]     +
                         test_weights_d["prob_opcode_jal"].weight    * ["jal"]   +
                         test_weights_d["prob_opcode_jr"].weight     * ["jr"]    +
                         test_weights_d["prob_opcode_jalr"].weight   * ["jalr"]  +
                         test_weights_d["prob_opcode_move"].weight   * ["move"]  +
                         test_weights_d["prob_opcode_lb"].weight     * ["lb"]    +
                         test_weights_d["prob_opcode_lbu"].weight    * ["lbu"]   +
                         test_weights_d["prob_opcode_lh"].weight     * ["lh"]    +
                         test_weights_d["prob_opcode_lhu"].weight    * ["lhu"]   +
                         test_weights_d["prob_opcode_lui"].weight    * ["lui"]   +
                         test_weights_d["prob_opcode_lw"].weight     * ["lw"]    +
                         test_weights_d["prob_opcode_li"].weight     * ["li"]    +
                         test_weights_d["prob_opcode_la"].weight     * ["la"]    +
                         test_weights_d["prob_opcode_sb"].weight     * ["sb"]    +
                         test_weights_d["prob_opcode_sh"].weight     * ["sh"]    +
                         test_weights_d["prob_opcode_sw"].weight     * ["sw"])
   test_weights_d["imm_value_5_l"] = [i for i in range (0, test_weights_d["imm_value_5_max_value"])]
   test_weights_d["imm_value_15_l"] = [i for i in range (0, test_weights_d["imm_value_15_max_value"])]
   test_weights_d["imm_value_16_l"] = [i for i in range (0, test_weights_d["imm_value_16_max_value"])]
   test_weights_d["numb_of_regs_to_use"] = random.choice([i for i in range (3, test_weights_d["numb_of_regs_to_use_max_value"]+1)])
