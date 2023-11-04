'''
BF spec has 8 symbols
> = Increment ptr
< = Decrement ptr
+ = Increment byte at ptr
- = Decrement byte at ptr
. = Print byte at ptr
, = Read byte, save to ptr
[ = loop_start
] = loop_end
'''
class BFLexer:

    SYMBOLS = ['>', '<', '+', '-', '.', ',', '[', ']']
    
    def __init__(self, input_file):
        self.ptr = 0
        self.input_file = input_file
        self.source = None
        self.tokens = []

    # gets current character while ignoring all other symbols
    # for now if we see any character outside of SYMBOLS, we treat it
    # and the rest of that line as a comment
    def look(self):
        if self.source[self.ptr] not in self.SYMBOLS:
            while self.source[self.ptr] not in self.SYMBOLS and self.source[self.ptr] != '\0':
                self.ptr += 1
        return self.source[self.ptr]

    # returns current character and advances
    def take(self):
        current = self.look()
        self.ptr += 1
        return current

    def scan(self):
        try:
            fp = open(self.input_file, 'r')
            self.source = fp.read() + '\0' 
            fp.close()
        except:
            raise Exception(f'Failed to read {self.input_file}')
        
        current = None
        while (current != '\0'):
            current = self.take()
            self.tokens.append(current)