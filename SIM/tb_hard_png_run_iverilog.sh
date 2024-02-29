rm -f sim.out dump.vcd
iverilog -g2001 -o sim.out tb_hard_png.v ../RTL/hard_png.v ../RTL/huffman_builder.v ../RTL/huffman_decoder.v
vvp -n sim.out
rm -f sim.out