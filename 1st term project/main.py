# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
class LexicalAnalyzer(object):

    #Token Definition
    VARIALBE = ['int', 'INT', 'char', 'CHAR']
    KEYWORD = ['if', 'IF', 'else', 'ELSE', 'while', 'WHILE', 'return', 'RETURN']
    OPERATOR = ['-', '+', '*', '/']
    COMPARSION = ['<', '>', '==', '!=', '<=', '>=']
    WHITESPACE = ['\t', '\n', ' ']
    BRACE = ['{', '}']
    PAREN = ['(', ')']
    ASSIGN = ['=']
    SEMICOLON = [';']
    COMMA = [',']

    #Letter Definition
    LETTER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q,' 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
              'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    SYMBOL = ['+', '-', '*', '/', '<', '>', '"', '!'] + ASSIGN+BRACE+PAREN+SEMICOLON+COMMA
    ZERO = ['0']
    NON_ZERO = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    DIGIT = ZERO + NON_ZERO
    STRING = LETTER + DIGIT + SYMBOL + WHITESPACE

    input_file = None

    def __init__(self, file):
        self.input_file = file

    def check_id(self, id):
        T = ["T0", "T1", "T2", "T3"]
        wdT = T[0]  # working directory T

        buf_id = id
        result = ""
        read_all = True

        if len(id)==1:
            head = id

        while(True):
            if len(id) > 1:
                if len(buf_id) != 0:
                    head = buf_id[0]
                    buf_id = buf_id[1:]
                    read_all = False
                if len(buf_id) == 0:
                    read_all = True

            if wdT == T[0]:
                if head in self.LETTER:
                    wdT = T[1]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                else:
                    return result, False, head

            elif wdT == T[1]:
                if head in self.LETTER:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.DIGIT:
                    wdT = T[3]
                    result = result + head
                    if read_all :
                        head = self.input_file.read(1)

            elif wdT == T[2]:
                if head in self.LETTER:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.DIGIT:
                    wdT = T[3]
                    result = result + head
                    if read_all :
                        head = self.input_file.read(1)

            elif wdT == T[3]:
                if head in self.LETTER:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.DIGIT:
                    wdT = T[3]
                    result = result + head
                    if read_all :
                        head = self.input_file.read(1)

            if head not in (self.LETTER + self.DIGIT):
                break

        if wdT == T[1] or wdT == T[2] or wdT == T[3]:
            return result, True, head
        else:
            return result, False, head

    def check_int(self, integer):
        T= ["T0", "T1", "T2", "T3", "T4", "T5"]
        wdT = T[0] #working directory T

        buf_integer = integer
        result = ""
        read_all= True

        if len(integer) == 1:
            head = integer

        while(True):
            if len(integer) > 1:
                if len(buf_integer) != 0:
                    head = buf_integer[0]
                    buf_integer = buf_integer[1:]
                    read_all = False
                if len(buf_integer) == 0:
                    read_all = True

            if wdT == T[0]:
                if head == "-":
                    wdT = T[1]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.ZERO:
                    wdT = T[2]
                    result = result + head
                    if read_all :
                        head = self.input_file.read(1)

                elif input in self.NON_ZERO:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                else:
                    return result, False, head

            elif wdT == T[1]:
                if head in self.NON_ZERO:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                else:
                    return result, False, head

            elif wdT == T[2]:
                return result, True, head

            elif wdT == T[3]:
                if head in self.ZERO:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.NON_ZERO:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                else :
                    return result, False, head

            elif wdT == T[4]:
                if head in self.ZERO:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.NON_ZERO:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                else:
                    return result, False, head

            elif wdT == T[5]:
                if head in self.ZERO:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.NON_ZERO:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                else:
                    return result, False, head

            if head not in self.DIGIT:
                break

        if head == ".":
            return result, False, head
        if wdT == T[2] or wdT == T[3] or wdT == T[4] or wdT == T[5]:
            return result, True, head
        else:
            return result, False, head


    def check_string(self, string):
        T= ["T0", "T1", "T2", "T3", "T4", "T5"]
        wdT = T[0] #working directory T

        buf_string = string
        result = ""
        read_all = True

        if len(string) == 1:
            input = string

        while (True):
            if len(string) > 1:
                if len(buf_string) != 0:
                    head = buf_string[0]
                    buf_string = buf_string[1:]
                    read_all = False
                if len(buf_string) == 0:
                    read_all = True

            if wdT == T[0]:
                if head in ['"']:
                    wdT = T[1]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                else:
                    return result, False, head

            elif wdT == T[1]:
                if head in ['"']:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.LETTER:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.DIGIT:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in [' ']:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

            elif wdT == T[2]:
                return result, True, head

            elif wdT == T[3]:
                if head in ['"']:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.LETTER:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.DIGIT:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in [' ']:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

            elif wdT == T[4]:
                if head in ['"']:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.LETTER:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.DIGIT:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in [' ']:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

            elif wdT == T[5]:
                if head in ['"']:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.LETTER:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in self.DIGIT:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

                elif head in [' ']:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)

            if head not in (self.DIGIT+self.LETTER+[' ','"']):
                break

        if wdT == T[2]:
            return result, True, head
        else:
            return result, False, head


    def run(self):



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Input error")
        exit()

        # Open file for reading
    try:
        file_name = sys.argv[1]
        f = open(file_name)
    except:
        print("Fail to read file")
        exit()

        # Run lexical Analyzer
    la = LexicalAnalyzer(f)
    symbol_table = la.run()

    # Close the file
    f.close()

    # Visualize the result
    for i in symbol_table:
        print(i[0], i[1])

    # Open file for writing result
    try:
        f = open(file_name[:-2] + '.out', 'w')
    except:
        print("Fail to write file")
        exit()

    for i in symbol_table:
        token = i[0]
        lexeme = i[1]
        f.writelines(token + ' ' + lexeme + '\n')
    f.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
