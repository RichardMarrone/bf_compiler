class ParseNode:

    def __init__(self, type, value=None, body=None):
        self.type = type
        self.value = value # to be used for optimizations
        self.body = body # for loops

    def __str__(self):
        return f"NODE_{self.type}"
    
    def __repr__(self):
        return f"NODE_{self.type}"

class BFParser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.ip = 0

    
    def parse(self):
        code_blocks = []

        while self.ip < len(self.tokens):
            code_blocks.append(self.command())
            self.ip += 1

        return code_blocks

    def peek_next(self):
        if self.ip < len(self.tokens) - 1:
            return self.tokens[self.ip + 1]
        return None

    def combine_duplicates(self, symbol):
        count = 1
        while self.peek_next() == symbol:
            count += 1
            self.ip += 1
 
        return ParseNode(symbol, count)

    def command(self):        
        token = self.tokens[self.ip]
        match token:
            case '>':
                return self.combine_duplicates('>')
            case '<':
                return self.combine_duplicates('<')
            case '+':
                return self.combine_duplicates('+')
            case '-':
                return self.combine_duplicates('-')
            case '.':
                return ParseNode('print')
            case ',':
                return ParseNode('read')
            case '[':
                return self.loop()
            case '\0':
                return ParseNode('EOF')
            case _:
                raise Exception(f'Parser Error: encountered unexpected token {token}')
    
    def loop(self):
        # ip points to opening [, step "inside"
        loop_body = []
        self.ip += 1
        while self.ip < len(self.tokens) and self.tokens[self.ip] != ']':
            loop_body.append(self.command())
            self.ip += 1
        
        if self.tokens[self.ip] == ']':
            return ParseNode('loop', body=loop_body)
        else:
            raise Exception(f'Parser error: encountered EOF while inside of a loop')