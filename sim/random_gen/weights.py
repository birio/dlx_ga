# import opcodes

prob_opcode_add     = 10
prob_opcode_addi    = 10
prob_opcode_addiu   = 10
prob_opcode_addu    = 10
prob_opcode_sub     = 10
prob_opcode_subu    = 10
prob_opcode_and     = 10
prob_opcode_andi    = 10
prob_opcode_nor     = 10
prob_opcode_or      = 10
prob_opcode_ori     = 10
prob_opcode_xor     = 10
prob_opcode_xori    = 10
prob_opcode_sll     = 10
prob_opcode_srl     = 10
prob_opcode_sra     = 10
prob_opcode_sllv    = 10
prob_opcode_srlv    = 10
prob_opcode_srav    = 10
prob_opcode_slt     = 10
prob_opcode_slti    = 10
prob_opcode_sltiu   = 10
prob_opcode_sltu    = 10
prob_opcode_beq     =  0
prob_opcode_bne     =  0
prob_opcode_blt     =  0
prob_opcode_bgt     =  0
prob_opcode_ble     =  0
prob_opcode_bge     =  0
prob_opcode_j       =  0
prob_opcode_jal     =  0
prob_opcode_jr      =  0
prob_opcode_jalr    =  0
prob_opcode_move    = 10
prob_opcode_lb      =  0
prob_opcode_lbu     =  0
prob_opcode_lh      =  0
prob_opcode_lhu     =  0
prob_opcode_lui     =  0
prob_opcode_lw      =  0
prob_opcode_li      =  0
prob_opcode_la      =  0
prob_opcode_sb      =  0
prob_opcode_sh      =  0
prob_opcode_sw      =  0

# must be greater than three
numb_of_regs_to_use = 10

# imm_value_5
imm_value_5_l = [ i for i in range (0, 2**5) ]

# imm_value_16
imm_value_16_l = [ i for i in range (0, 2**16) ]
# imm_value_15
imm_value_15_l = [ i for i in range (0, 2**15) ]

# between 1 and 100
max_num_of_labels = 1

weighted_opcodes_l = (prob_opcode_add    * ["add"] +  
                      prob_opcode_addi   * ["addi"] +
                      prob_opcode_addiu  * ["addiu"] +
                      prob_opcode_addu   * ["addu"] +
                      prob_opcode_sub    * ["sub"] +
                      prob_opcode_subu   * ["subu"] +
                      prob_opcode_and    * ["and"] +
                      prob_opcode_andi   * ["andi"] +
                      prob_opcode_nor    * ["nor"] +
                      prob_opcode_or     * ["or"] +
                      prob_opcode_ori    * ["ori"] +
                      prob_opcode_xor    * ["xor"] +
                      prob_opcode_xori   * ["xori"] +
                      prob_opcode_sll    * ["sll"] +
                      prob_opcode_srl    * ["srl"] +
                      prob_opcode_sra    * ["sra"] +
                      prob_opcode_sllv   * ["sllv"] +
                      prob_opcode_srlv   * ["srlv"] +
                      prob_opcode_srav   * ["srav"] +
                      prob_opcode_slt    * ["slt"] +
                      prob_opcode_slti   * ["slti"] +
                      prob_opcode_sltiu  * ["sltiu"] +
                      prob_opcode_sltu   * ["sltu"] +
                      prob_opcode_beq    * ["beq"] +
                      prob_opcode_bne    * ["bne"] +
                      prob_opcode_blt    * ["blt"] +
                      prob_opcode_bgt    * ["bgt"] +
                      prob_opcode_ble    * ["ble"] +
                      prob_opcode_bge    * ["bge"] +
                      prob_opcode_j      * ["j"] +
                      prob_opcode_jal    * ["jal"] +
                      prob_opcode_jr     * ["jr"] +
                      prob_opcode_jalr   * ["jalr"] +
                      prob_opcode_move   * ["move"] +
                      prob_opcode_lb     * ["lb"] +
                      prob_opcode_lbu    * ["lbu"] +
                      prob_opcode_lh     * ["lh"] +
                      prob_opcode_lhu    * ["lhu"] +
                      prob_opcode_lui    * ["lui"] +
                      prob_opcode_lw     * ["lw"] +
                      prob_opcode_li     * ["li"] +
                      prob_opcode_la     * ["la"] +
                      prob_opcode_sb     * ["sb"] +
                      prob_opcode_sh     * ["sh"] +
                      prob_opcode_sw     * ["sw"])
