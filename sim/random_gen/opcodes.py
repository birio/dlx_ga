
# instr r0, r1, r2 
r_types_l = [

"add", "addu", "sub", "subu",
"and", "nor",  "or",  "xor",
"sllv", "srlv", "srav",
"slt", "sltu",

]

# instr r0
r_j_types_l = [

"jr",  "jalr"

]

# instr r0, r1, imm
i_types_l = [

"addi", "addiu",
"andi", "ori",   "xori",
"slti", "sltiu",

]

# instr r0, r1, label
b_types_l = [

"beq",  "bne",   "blt",  "bgt", "ble", "bge"

]

# move r0, r1
move_types_l = [

"move"

]

# instr r0, imm16
load_types_l = [

"lb",   "lbu",   "lh",   "lhu", "lw", "la",
"sb",   "sh",    "sw"

]

# instr r0, r1, imm5
s_i_types_l = [
 
"sll", "srl",  "sra"

]

# instr r0, imm16
l_i_types_l = [

"lui" ,  "li"

]

# instr label
j_types_l = [

"j", "jal"

]

