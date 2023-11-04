An interpreter, transpiler, and compiler for the BrainF*** programming language

## Running
This repo offers 3 ways to run a BF program:
- ```interpreter.py``` is a python interpreter.
  - Run this ```python3 interpreter.py``` to directly interpret your input BF file
- ```bf_to_py.py``` transpiles a source BF file to python.
  - Run ```python3 bf_to_py.py``` to generate ```output.py``` in ```/output```. Then run ```python3 output.py``` to run your program
- ```bf_to_x86_64.py``` compiles a source BF file to x86_64 assembly.
  - Run ```python3 bf_to_x86_64.py``` to generate ```output.s``` in ```/output```. Then ```cd``` into ```/output``` and run ```nasm -f elf64 output.s && ld output.o && ./a.out``` to assemble, link, and execute your program. Note this will only work on linux as it relies on linux syscalls.


### x86_64 syscalls 
https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md#x86_64-64_bit

### Handy NASM guide
https://cs.lmu.edu/~ray/notes/nasmtutorial/

### BrainF*** sample scripts
[https://esolangs.org/wiki/brainf***](https://esolangs.org/wiki/Brainfuck)

### Lexer inspiration
https://github.com/slu4coder/Minimal-UART-CPU-System/blob/main/Min%20Language/min.py

### Python interpreter inspiration
[https://github.com/joshhoughton...pyf***.py](https://github.com/joshhoughton/PyFuck/blob/master/pyfuck.py)