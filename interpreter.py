from bf_lexer import BFLexer

lexer = BFLexer('./test_programs/hello_world.bf')
lexer.scan()

# Match Brackets
loop_start_to_end = {}
loop_end_to_start = {}
stack = []
for index, token in enumerate(lexer.tokens):
    if token == '[':
        stack.append(index)
    elif token == ']':
        if len(stack) == 0:
            raise Exception(f"Invalid program. ']' at index {index} is missing opening '['")
        opening = stack.pop()
        loop_end_to_start[index] = opening
        loop_start_to_end[opening] = index

if len(stack) > 0:
    raise Exception(f"Invalid program. Missing closing for {stack.pop()}.\nThis error will only report the location of the most recent open '['")

memory = [0 for _ in range(3_000_000)]
pointer = 0
ip = 0

while ip < len(lexer.tokens):
    token = lexer.tokens[ip]
    match token:
        case '>':
            if pointer < 30_000:
                pointer += 1
            ip += 1
        case '<':
            if pointer > 0:
                pointer -= 1
            ip += 1
        case '+':
            memory[pointer] += 1
            if memory[pointer] == 256:
                memory[pointer] = 0
            ip += 1
        case '-':
            memory[pointer] -= 1
            if memory[pointer] < 0:
                memory[pointer] = 255
            ip += 1
        case '.':
            print(chr(memory[pointer]), end='')
            ip += 1
        case ',':
            data = ord(input('>'))
            if (data < 0 or data > 255):
                print('Error: please enter one byte of data')
            else:
                memory[pointer] = data
            ip += 1
        case '[':
            if memory[pointer] == 0:
                ip = loop_start_to_end[ip]
            ip += 1
        case ']':
            if memory[pointer] != 0:
                ip = loop_end_to_start[ip]
            ip += 1
        case '\0':
            break