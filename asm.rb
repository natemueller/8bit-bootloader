#!/usr/bin/env ruby

OPCODES = {
  'NOOP' => 0,
  'LDA' => 1,
  'ADD' => 2,
  'SUB' => 3,
  'STA' => 4,
  'LDI' => 5,
  'JMP' => 6,
  'JC' => 7,
  'JZ' => 8,

  'OUT' => 14,
  'HLT' => 15,
}

File.open(ARGV[0].sub(/\.8sm$/, '.out'), 'wb') do |fh|
  File.readlines(ARGV[0]).each_with_index do |line, i|
    opcode, arg = line.chomp.split(/ +/)

    if !OPCODES.key?(opcode)
      puts "Unknown opcode: #{opcode}"
      exit(-1)
    end

    fh.write([OPCODES[opcode].to_s(16) + (arg.to_i || 0).to_s(16)].pack('H*'))
  end
end
