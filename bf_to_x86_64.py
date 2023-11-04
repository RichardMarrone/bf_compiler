from bf_lexer import BFLexer
from bf_parser import BFParser

lexer = BFLexer('./test_programs/hello_world.bf')
lexer.scan()

parser = BFParser(lexer.tokens)
blocks = parser.parse()


def infinite_number_stream():
    num = 0
    while True:
        yield num
        num += 1

stream = infinite_number_stream()

def generate_loop_code(block):
    body = ''
    loop_number = next(stream)
    for sub_block in block.body:
        body += gen_code(sub_block)

    current = f"""
    _loop_start_{loop_number}:
    mov al, [r10]
    test al, al
    jz _loop_done_{loop_number}
        {body}
    mov al, [r10]
    test al, al
    jnz _loop_start_{loop_number}
    _loop_done_{loop_number}:
    """
    
    return current

def gen_code(block):
    buffer = ''
    type = block.type
    match type:
        case '+':
            buffer += f'add       [r10], byte {block.value} \n'
        case '-':
            buffer += f'sub       [r10], byte {block.value}\n'
        case '>':
            buffer += f'add       r10, {block.value}\n'
        case '<':
            buffer += f'sub       r10, {block.value}\n'
        case 'print':
            buffer += "call      _stdout\n"
        case 'read':
            buffer += "call      _stdin\n"
        case 'loop':
            buffer += generate_loop_code(block)
        case 'EOF':
            buffer += ''

    return buffer

code = []
for block in blocks:
    code.append(gen_code(block))

code = ''.join(code)

with open('./output/output.s', 'w') as fp:
    # generate python from the code blocks. 
    fp.write(f"""    ; r10 holds ptr to current position in array    
    section   .bss
    array:    resb      30000 ; 30k byte array
    buffer:   resb      2     ; 1 byte IO buffer
                      
    global    _start

    section   .text
    _start:
          mov       r10, array
          {code}
          mov       rax, 60                 ; system call for exit
          xor       rdi, rdi                ; exit code 0
          syscall                           ; invoke operating system to exit
        
    _stdout:  
            mov       rax, 1                  ; system call for write
            mov       rdi, 1                  ; file handle 1 is stdout
            mov       rsi, r10             ; address of string to output
            mov       rdx, 1                 ; number of bytes
            syscall                           ; invoke operating system to do the write
            ret

    _stdin:   
            mov       rax, 0                  ; syscall for read
            mov       rdi, 0                  ; fd of 0 for read
            mov       rsi, buffer             ; address of buffer. we use 2 bytes due to new line
            mov       rdx, 2                 ; number of bytes
            syscall
            mov r13b, [rsi]
            mov [r10], r13b
            ret
    """)