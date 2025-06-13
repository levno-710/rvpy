# RISC-V VM in Python

A minimal RISC-V virtual machine implemented in Python for the Bachelor's Seminar “Moderne Hardware” at Heinrich-Heine-Universität Düsseldorf.

See the accompanying paper for design details: [./paper](paper)

## Usage
```
usage: main.py [-h] [-x] [-m MEM_SIZE] [-d] program

positional arguments:
  program             Path to the RISC-V program to execute

options:
  -h, --help          show this help message and exit
  -x, --hex           Interpret the program as a hex file instead of a binary file
  -m MEM_SIZE, --mem-size MEM_SIZE
                      Size of the memory in bytes (default: 1 GiB)
  -d, --disassemble   Print executed instructions in disassembled form
```

Example:

```bash
python src/main.py -x test/fib/fib.txt
```