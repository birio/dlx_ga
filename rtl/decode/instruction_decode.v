// +----------------------------------------------------------------------------
// GNU General Public License
// -----------------------------------------------------------------------------
// This file is part of uDLX (micro-DeLuX) soft IP-core.
//
// uDLX is free soft IP-core: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// uDLX soft core is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with uDLX. If not, see <http://www.gnu.org/licenses/>.
// +----------------------------------------------------------------------------
// PROJECT: uDLX core Processor
// ------------------------------------------------------------------------------
// FILE NAME   : instruction_decode.v
// -----------------------------------------------------------------------------
// KEYWORDS    : dlx, decoder, instruction
// -----------------------------------------------------------------------------
// PURPOSE     : Top level module of Instruction Decode stage
// -----------------------------------------------------------------------------
module instruction_decode
#(
   parameter PC_WIDTH = 20,
   parameter DATA_WIDTH = 32,
   parameter INSTRUCTION_WIDTH = 32,
   parameter REG_ADDR_WIDTH = 5,
   parameter OPCODE_WIDTH = 6,
   parameter FUNCTION_WIDTH = 6,
   parameter IMEDIATE_WIDTH = 16,
   parameter PC_OFFSET_WIDTH = 26
)
(
   input clk,
   input rst_n,
   input [INSTRUCTION_WIDTH-1:0] instruction_in,
   input [PC_WIDTH-1:0] new_pc_in,
   input wb_write_enable,
   input [DATA_WIDTH-1:0] wb_write_data,
   input [REG_ADDR_WIDTH-1:0] wb_reg_wr_addr,
   input select_new_pc_in,

   //  output alu_src_out,
   output [REG_ADDR_WIDTH-1:0] reg_rd_addr1_out,
   output [REG_ADDR_WIDTH-1:0] reg_rd_addr2_out,
   output [INSTRUCTION_WIDTH-1:0] instruction_out,
   output [OPCODE_WIDTH-1:0] opcode_out,
   output [FUNCTION_WIDTH-1:0] inst_function_out, //added, will exist when the function is zero
   output mem_data_rd_en_out,
   output mem_data_wr_en_out,
   output write_back_mux_sel_out,
   output reg_wr_en_out,
   output [REG_ADDR_WIDTH-1:0] reg_wr_addr_out,
   output [DATA_WIDTH-1:0] constant_out,
   output imm_inst_out,
   output [DATA_WIDTH-1:0] data_alu_a_out,
   output [DATA_WIDTH-1:0] data_alu_b_out,
   output [PC_WIDTH-1:0] new_pc_out,
   output [PC_OFFSET_WIDTH-1:0] pc_offset_out,
   output branch_inst_out,
   output jump_inst_out,
   output jump_use_r_out,

   output rd_inst_ena,
   output stall_out,
   output general_flush

);

// -----------------------------------------------------------------------------
// Internal
// -----------------------------------------------------------------------------

// Wires

wire [DATA_WIDTH-1:0] data_alu_a;
wire [DATA_WIDTH-1:0] data_alu_b;
wire [OPCODE_WIDTH-1:0] opcode;
wire [FUNCTION_WIDTH-1:0] inst_function;
wire [REG_ADDR_WIDTH-1:0] reg_rd_addr1;
wire [REG_ADDR_WIDTH-1:0] reg_rd_addr2;
wire reg_rd_en1;
wire reg_rd_en2;
wire [REG_ADDR_WIDTH-1:0] reg_wr_addr;
wire reg_wr_en;
wire [IMEDIATE_WIDTH-1:0] immediate;
wire imm_inst;
wire [DATA_WIDTH-1:0] constant;
wire [PC_OFFSET_WIDTH-1:0] pc_offset;
wire mem_data_wr_en;
wire write_back_mux_sel;
wire branch_inst;
wire jump_inst;
wire jump_use_r;

wire decode_flush;

// Ranges dependem das instruções a serem definidas

// -----------------------------------------------------------------------------
// Instruction decoder unit
// -----------------------------------------------------------------------------
instruction_decoder
#(
   .INSTRUCTION_WIDTH(INSTRUCTION_WIDTH),
   .OPCODE_WIDTH(OPCODE_WIDTH),
   .FUNCTION_WIDTH(FUNCTION_WIDTH),
   .REG_ADDR_WIDTH(REG_ADDR_WIDTH),
   .IMEDIATE_WIDTH(IMEDIATE_WIDTH),
   .PC_OFFSET_WIDTH(PC_OFFSET_WIDTH)
)
instruction_decoder_u0
(
   .instruction_in(instruction_in),
   .opcode(opcode),
   .inst_function(inst_function),
   .reg_rd_addr1_out(reg_rd_addr1),
   .reg_rd_addr2_out(reg_rd_addr2),
   .reg_rd_en1_out(reg_rd_en1),
   .reg_rd_en2_out(reg_rd_en2),
   .reg_wr_addr_out(reg_wr_addr),
   .reg_wr_en_out(reg_wr_en),
   .immediate_out(immediate),
   .imm_inst_out(imm_inst),
   .pc_offset(pc_offset),
   .mem_data_wr_en_out(mem_data_wr_en),
   .mem_data_rd_en_out(mem_data_rd_en),
   .write_back_mux_sel_out(write_back_mux_sel),
   .branch_inst_out(branch_inst),
   .jump_inst_out(jump_inst),
   .jump_use_r_out(jump_use_r)
);

// -----------------------------------------------------------------------------
// Register File
// -----------------------------------------------------------------------------
register_bank
#(
   .DATA_WIDTH(DATA_WIDTH),
   .ADDRESS_WIDTH(REG_ADDR_WIDTH)
)
register_bank_u0
(
   .clk(clk),
   .rst_n(rst_n),
   .rd_reg1_addr(reg_rd_addr1),
   .rd_reg2_addr(reg_rd_addr2),
   .write_address(wb_reg_wr_addr),
   .write_enable(wb_write_enable),
   .write_data(wb_write_data),
   .rd_reg1_data_out(data_alu_a),
   .rd_reg2_data_out(data_alu_b)
);


// -----------------------------------------------------------------------------
// General core control Signals
// -----------------------------------------------------------------------------
control
control_u0
(
   .id_ex_mem_data_rd_en(mem_data_rd_en_out),
   .id_ex_reg_wr_addr(reg_wr_addr_out),
   .if_id_rd_reg_a_en(reg_rd_en1),
   .if_id_rd_reg_b_en(reg_rd_en2),
   .if_id_rd_reg_a_addr(reg_rd_addr1),
   .if_id_rd_reg_b_addr(reg_rd_addr2),
   .select_new_pc(select_new_pc_in),

   .inst_rd_en(rd_inst_ena),
   .stall(stall_out),
   .general_flush(general_flush),
   .decode_flush(decode_flush)
);


// -----------------------------------------------------------------------------
// Immediate value signal extend
// -----------------------------------------------------------------------------
signal_extend
#(
    .OUT_DATA_WIDTH(32),
    .IN_DATA_WIDTH(16)
)
signal_extend_u0
(
    .signal_in(immediate),
    .signal_out(constant)
);

// -----------------------------------------------------------------------------
// Pipeline registers ID/EX
// -----------------------------------------------------------------------------
inst_decode_pipe
#(
   .INSTRUCTION_WIDTH(INSTRUCTION_WIDTH),
   .PC_WIDTH(PC_WIDTH),
   .DATA_WIDTH(DATA_WIDTH),
   .OPCODE_WIDTH(OPCODE_WIDTH),
   .FUNCTION_WIDTH(FUNCTION_WIDTH),
   .REG_ADDR_WIDTH(REG_ADDR_WIDTH),
   .IMEDIATE_WIDTH(IMEDIATE_WIDTH),
   .PC_OFFSET_WIDTH(PC_OFFSET_WIDTH)
)
inst_decode_pipe_u0
(
   .clk(clk),
   .rst_n(rst_n),

   .flush(decode_flush),

   .data_alu_a_in(data_alu_a),
   .data_alu_b_in(data_alu_b),
   .new_pc_in(new_pc_in),
   .instruction_in(instruction_in),
   .opcode_in(opcode),
   .inst_function_in(inst_function),
   .reg_rd_addr1_in(reg_rd_addr1),
   .reg_rd_addr2_in(reg_rd_addr2),
   .reg_wr_addr_in(reg_wr_addr),
   .reg_wr_en_in(reg_wr_en),
   .constant_in(constant),
   .imm_inst_in(imm_inst),
   .pc_offset_in(pc_offset),
   .mem_data_wr_en_in(mem_data_wr_en),
   .mem_data_rd_en_in(mem_data_rd_en),
   .write_back_mux_sel_in(write_back_mux_sel),
   .branch_inst_in(branch_inst),
   .jump_inst_in(jump_inst),
   .jump_use_r_in(jump_use_r),


   .data_alu_a_out(data_alu_a_out),
   .data_alu_b_out(data_alu_b_out),
   .new_pc_out(new_pc_out),
   .instruction_out(instruction_out),
   .opcode_out(opcode_out),
   .inst_function_out(inst_function_out),
   .reg_rd_addr1_out(reg_rd_addr1_out),
   .reg_rd_addr2_out(reg_rd_addr2_out),
   .reg_wr_addr_out(reg_wr_addr_out),
   .reg_wr_en_out(reg_wr_en_out),
   .constant_out(constant_out),
   .imm_inst_out(imm_inst_out),
   .pc_offset_out(pc_offset_out),
   .mem_data_wr_en_out(mem_data_wr_en_out),
   .mem_data_rd_en_out(mem_data_rd_en_out),
   .write_back_mux_sel_out(write_back_mux_sel_out),
   .branch_inst_out(branch_inst_out),
   .jump_inst_out(jump_inst_out),
   .jump_use_r_out(jump_use_r_out)
 );


endmodule