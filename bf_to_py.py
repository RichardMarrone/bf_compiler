from bf_lexer import BFLexer
from bf_parser import BFParser

lexer = BFLexer('./test_programs/hello_world.bf')
lexer.scan()

parser = BFParser(lexer.tokens)
blocks = parser.parse()

def generate_loop_code(block, depth=0):
    indents = ' ' * depth * 4
    # TODO safety
    current = 'while memory[ptr] > 0:\n'
    for sub_block in block.body:
        current += gen_code(sub_block, depth + 1)
    return current

def gen_code(block, depth=0):
    indents = ' ' * depth * 4
    buffer = ''
    type = block.type
    match type:
        case '+':
            # TODO overflow
            buffer += (indents + F'memory[ptr] += {block.value}\n')
        case '-':
            # TODO underflow
            buffer += (indents + f'memory[ptr] -= {block.value}\n')
        case '>':
            # TODO limit mem
            buffer += (indents + f'ptr += {block.value}\n')
        case '<':
            # TODO limit mem
            buffer += (indents + f'ptr -= {block.value}\n')
        case 'print':
            buffer += (indents + "print(chr(memory[ptr]), end='')\n")
        case 'read':
            # TODO safety
            buffer += (indents + "memory[ptr] = ord(input('> '))\n")
        case 'loop':
            buffer += (indents + generate_loop_code(block, depth))
        case 'EOF':
            buffer += (indents + 'exit(0)')

    return buffer



with open('./output/output.py', 'w') as fp:
    # generate python from the code blocks. 
    fp.write('ptr = 0\n')
    fp.write('memory = [0 for _ in range(30_000)]\n')
    for block in blocks:
        fp.write(gen_code(block))
        