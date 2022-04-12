# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys


class LexicalAnalyzer(object):
    # Token Definition
    VARIABLE = ['int', 'INT', 'char', 'CHAR']
    KEYWORD = ['if', 'IF', 'else', 'ELSE', 'while', 'WHILE', 'return', 'RETURN']
    OPERATOR = ['-', '+', '*', '/']
    COMPARISON = ['<', '>', '==', '!=', '<=', '>=']
    WHITESPACE = ['\t', '\n', ' ']
    BRACE = ['{', '}']
    PAREN = ['(', ')']
    ASSIGN = ['=']
    SEMICOLON = [';']
    COMMA = [',']
    MERGE = BRACE + PAREN + SEMICOLON + COMMA + OPERATOR[1:] + COMPARISON

    # Letter Definition
    LETTER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q,' 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p','q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    SYMBOL = ['+', '-', '*', '/', '<', '>', '"', '!'] + ASSIGN + BRACE + PAREN + SEMICOLON + COMMA
    ZERO = ['0']
    NON_ZERO = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    DIGIT = ZERO + NON_ZERO
    STRING = LETTER + DIGIT + SYMBOL + WHITESPACE

    def __init__(self, file):
        self.input_file = file

    def check_id(self, id, char):
        """print("ididididiid: "+id)
        T = ["T0", "T1", "T2", "T3"]
        wdT = T[0]  # working directory T

        buf_id = id
        result = ""
        read_all = True

        #
        if len(id) == 1:
            head = id


        z = len(id)
        while z>0:
            z = z-1
            print("length of id: " + str(len(id))+" "+id)
            print("length of buf_id: "+str(len(buf_id))+" "+buf_id)
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
                        print("id T[2]->T[3] head : "+head)# 1 byte input

                else:
                    return result, False, head

            elif wdT == T[1]:
                if head in self.LETTER:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[1]->T[2] head : "+head)

                elif head in self.DIGIT:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[1]->T[3] head : " + head)

                else:
                    return result, True, head

            elif wdT == T[2]:
                if head in self.LETTER:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[2]->T[2] head : " + head)

                elif head in self.DIGIT:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[2]->T[3] head : " + head)

                else:
                    return result, True, head

            elif wdT == T[3]:
                if head in self.LETTER:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[3]->T[2] head : " + head)

                elif head in self.DIGIT:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[3]->T[3] head : " + head)

                else:
                    return result, True, head

            if head not in (self.LETTER + self.DIGIT):
                break

        if wdT == T[1] or wdT == T[2] or wdT == T[3]:
            return result, True, head
        else:
            return result, False, head"""
        sub_string = ""
        symbol = self.LETTER + self.ZERO + self.NON_ZERO + ['_']
        i = 0
        j = 0
        final = [1, 2, 3, 4, 5, 6]
        transition_table = [[1, -1, -1, 2], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6], [3, 4, 5, 6]]

        if char == "":
            char = self.input_file.read(1)

        # Read string
        while char in symbol:
            id = id + char
            char = self.input_file.read(1)

        # Analyze
        for c in id:
            if c in self.LETTER:
                j = 0
            elif c in self.ZERO:
                j = 1
            elif c in self.NON_ZERO:
                j = 2
            elif c in ['_']:
                j = 3
            else:
                return sub_string, False, char

            tmp_i = i
            i = transition_table[i][j]
            sub_string = sub_string + c

            if i == -1:
                return sub_string, False, char

        if i in final:
            return sub_string, True, char
        else:
            return sub_string, False, char

    def check_int(self, integer):
        T = ["T0", "T1", "T2", "T3", "T4", "T5"]
        wdT = T[0]  # working directory T

        buf_integer = integer
        result = ""
        read_all = True

        if len(integer) == 1:
            head = integer

        while True:
            print("integer of length: " + str(len(integer)) + " " + integer)
            print("buf_integer of length " + str(len(buf_integer)) + " " + buf_integer)
            if len(integer) > 1:
                if len(buf_integer) != 0:
                    head = buf_integer[0]
                    buf_integer = buf_integer[1:]
                    read_all = False
                if len(buf_integer) == 0:
                    read_all = True

            print("head: "+head)

            if wdT == T[0]:
                #print("check T[0]: " + head+ integer)
                if head == "-":
                    print("ASDFASFASDFASFASFDAS")
                    wdT = T[1]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[0]->T[1] head : " + head)

                elif head in self.ZERO:
                    wdT = T[2]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[0]->T[2] head : " + head)

                elif head in self.NON_ZERO:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[0]->T[3] head : " + head)

                else:
                    return result, False, head

            elif wdT == T[1]:
                if head in self.NON_ZERO:
                    wdT = T[3]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[1]->T[3] head : " + head)

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
                        print("id T[3]->T[4] head : " + head)

                elif head in self.NON_ZERO:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[3]->T[5] head : " + head)

                else:
                    return result, True, head

            elif wdT == T[4]:
                if head in self.ZERO:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[4]->T[4] head : " + head)

                elif head in self.NON_ZERO:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[4]->T[5] head : " + head)

                else:
                    return result, True, head

            elif wdT == T[5]:
                if head in self.ZERO:
                    wdT = T[4]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[5]->T[4] head : " + head)

                elif head in self.NON_ZERO:
                    wdT = T[5]
                    result = result + head
                    if read_all:
                        head = self.input_file.read(1)
                        print("id T[5]->T[5] head : " + head)

                else:
                    return result, True, head

            if head not in self.DIGIT:
                break

        if head == ".":
            return result, False, head
        if wdT == T[2] or wdT == T[3] or wdT == T[4] or wdT == T[5]:
            return result, True, head
        else:
            return result, False, head

    def check_string(self, string):
        T = ["T0", "T1", "T2", "T3", "T4", "T5"]
        wdT = T[0]  # working directory T

        buf_string = string
        result = ""
        read_all = True

        if len(string) == 1:
            head = string

        while True:
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

                else:
                    return result, False, head

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

                else:
                    return result, False, head

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

                else:
                    return result, False, head

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

                else:
                    return result, False, head

            if head not in (self.DIGIT + self.LETTER + [' ', '"']):
                break

        if wdT == T[2]:
            return result, True, head
        else:
            return result, False, head

    def run(self):
        check = True
        line_num = 1
        result = ""
        symbol_table = []

        while True:
            if check:
                one = self.input_file.read(1)
                print("check one: "+one)
                check = True

            if (one == "") and (result == ""):
                break

            print("check result & one: "+result+ " "+one)
            if (one not in self.STRING) and (result == ""):
                #print("check three: " + one)
                error_noti = "1Line" + str(line_num) + ": Wrong input format" + one
                try:
                    f = open(file_name[:-2]+'_error.out','w')
                except:
                    print("Failed to write file")
                    exit()

                for i in error_noti :
                    f.writelines(i)

                f.close()
                print(error_noti)
                exit()

            if one == '\n':
                line_num = line_num + 1
                one = ""
                check = True
                continue

            if one in self.WHITESPACE:
                one = ""
                check = True
                continue

            result = result + one
            one = ""
            check = True

            if result in self.LETTER:
                if one == "":
                    one = self.input_file.read(1)
                    check = False

                while(one in self.LETTER):
                    result = result + one
                    one = self.input_file.read(1)

                if one in self.DIGIT:
                    check = False
                    continue

                if result in self.VARIABLE:
                    symbol_table.append(['variable type', result])
                    result = ""
                    continue

                elif result in self.KEYWORD:
                    symbol_table.append([result, result])
                    result = ""
                    continue

            if result in self.ASSIGN:
                if one == "":
                    one = self.input_file.read(1)
                    check = False

                if result + one in self.COMPARISON:
                    symbol_table.append(['comp', result+one])
                    result = ""
                    one = ""
                    check = True
                    continue

                else:
                    symbol_table.append(['assign', result])
                    result = ""
                    continue

            if result in ['-']:
                if (len(symbol_table) != 0) and (('num' in symbol_table[-1]) or ('id' in symbol_table[-1]) or (')' in symbol_table[-1])):
                    symbol_table.append(['addsub', result])
                    result = ""
                    continue

            if result in self.MERGE + ['!']:
                if result in ['<','>']:
                    if one == "":
                        one = self.input_file.read(1)
                        check = True

                    if result + one in self.COMPARISON:
                        symbol_table.append(['comp2', result + one])
                        result = ""
                        check = True
                        continue

                if result == "!":
                    if one == "":
                        one = self.input_file.read(1)
                        check = True

                    if one == "=":
                        symbol_table.append(['comp3', result + one])
                        result = ""
                        check = True
                        continue

                    else:
                        error_noti = "2Line" + str(line_num) + ":Wrong input format"
                        try:
                            f= open(file_name[:-2]+'_error.out','w')
                        except :
                            print("Fail to write file")
                            exit()

                        for i in error_noti:
                            f.writelines(i)
                        f.close()
                        print(error_noti)
                        exit()

                if result in self.BRACE:
                    if result == '{':
                        symbol_table.append(['lbrace', result])
                    elif result == '}':
                        symbol_table.append(['rbrace', result])
                elif result in self.PAREN:
                    if result == '(':
                        print("left paren find! "+str(line_num))
                        symbol_table.append(['lparen', result])
                    elif result == ')':
                        symbol_table.append(['rparen', result])
                elif result in self.SEMICOLON:
                    symbol_table.append(['semi', result])
                elif result in self.COMMA:
                    symbol_table.append(['comma', result])
                elif result in self.OPERATOR:
                    if result == '+':
                        symbol_table.append(['add', result])
                    elif result == '-':
                        symbol_table.append(['sub', result])
                    elif result == '*':
                        symbol_table.append(['multi', result])
                    elif result == '/':
                        symbol_table.append(['div', result])
                elif result in self.COMPARISON:
                    symbol_table.append(['comp4', result])
                result = ""
                continue

            #print("digit check:" + result)
            if result[0] in self.DIGIT + ['-']:
                result, fact, one = self.check_int(result)

                if fact:
                    if one ==".":
                        result = result + one
                        one = ""
                        check = True
                    else:
                        symbol_table.append(['num', result])
                        result = ""

                    if result == "":
                        if one != "":
                            check = False
                            continue
                        else:
                            check = True
                            continue

                else:
                    if one == ".":
                        result = result + one
                        one = ""
                        check = True

                    if result =='-':
                        result = result + one
                        one = ""
                        check = True

                    if result == "":
                        if one != "":
                            check = False
                        else:
                            check = True

            #print("result: "+result)
            if result[0] in self.LETTER:
                result, fact, one = self.check_id(result, one)
                if fact:
                    symbol_table.append(['id', result])
                    result = ""
                    if one != "":
                        check = False
                        continue
                    else:
                        check = True
                        continue

                else:
                    error_noti = "3Line" + str(line_num) + ": Wrong input format"
                    # Open file for writing Error
                    try:
                        f = open(file_name[:-2]+'_error.out', 'w')
                    except:
                        print("Fail to write file")
                        exit()

                    for i in error_noti:
                        f.writelines(i)
                    f.close()
                    print(error_noti)
                    exit()

            if result[0] == '"':
                #print("string result check: "+result)
                result, fact, one = self.check_string(result)
                if fact:
                    symbol_table.append(['literal', result])
                    result = ""
                    if one != "":
                        check = False
                        continue
                    else:
                        check = True
                        continue

                else:
                    error_noti = "4Line" + str(line_num) + ": Wrong input format"
                    # Open file for writing Error
                    try:
                        f = open(file_name[:-2]+'_error.out', 'w')
                    except:
                        print("Fail to write file")
                        exit()

                    for i in error_noti:
                        f.writelines(i)
                    f.close()
                    print(error_noti)
                    exit()

        return symbol_table


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