# assembler and vcpu for the bored architecture

I was bored, so I made some stuff, and called the architecture bored.

I made this project to try to instrument a custom architecture, as well as an
assembler, assemlby language, and virtual cpu that are all designed to support
and run the bored architecture. If you find this useful, cool.

Progress will be ongoing, and might be slow.

The bored_assembler.py file will read the code.bd file, and assemble it into the code file.


Every instruction is 32 bytes long. This doesn't really matter for now, but will
eventually facilitate more instructions. Probably.
