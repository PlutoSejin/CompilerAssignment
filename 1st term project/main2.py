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
    LETTER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q,' 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
              'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    SYMBOL = ['+', '-', '*', '/', '<', '>', '"', '!'] + ASSIGN + BRACE + PAREN + SEMICOLON + COMMA
    ZERO = ['0']
    NON_ZERO = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    DIGIT = ZERO + NON_ZERO
    STRING = LETTER + DIGIT + SYMBOL + WHITESPACE

    def __init__(self, file):
        self.input_file = file

    def check_id(self, word, letter):
        tmp_word = ""
        symbol = self.LETTER + self.DIGIT
        current_state = 0
        final = [1, 2, 3]
        transition_table = [[1, -1], [2, 3], [2, 3], [2, 3]]

        if letter == "":
            letter = self.input_file.read(1)
        # Read string
        while letter in symbol:
            word = word + letter
            letter = self.input_file.read(1)

        # Analyze
        for c in word:
            if c in self.LETTER:
                current_state = transition_table[current_state][0]
            elif c in self.DIGIT:
                current_state = transition_table[current_state][1]
            else:
                return tmp_word, False, letter
            tmp_word = tmp_word + c

            if current_state == -1:  # 존재하지 않는 경로
                return tmp_word, False, letter

        # 주어진 string 모두 확인한 후
        if current_state in final:  # final state에 존재하는가
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    def check_int(self, word, letter):
        tmp_word = ""
        current_state = 0
        transition_table = [[1, 2, 3], [-1, -1, 3], [-1, -1, -1], [-1, 4, 5], [-1, 4, 5], [-1, 4, 5]]
        final_state = [2, 3, 4, 5]
        symbol = ['-'] + self.DIGIT

        # Read string
        if letter == "":
            letter = self.input_file.read(1)
        while letter in symbol:
            if word[-1] in self.DIGIT and letter == '-':
                break
            word = word + letter
            letter = self.input_file.read(1)

        for c in word:
            if c == '-':
                current_state = transition_table[current_state][0]
            elif c in self.ZERO:
                current_state = transition_table[current_state][1]
            elif c in self.NON_ZERO:
                current_state = transition_table[current_state][2]
            else:
                return tmp_word, True, letter
            tmp_word = tmp_word + c

            if current_state == -1:  # 존재하지 않는 경로
                return tmp_word, False, letter

            # 주어진 string 모두 확인한 후
        if current_state in final_state:  # final state에 존재하는가
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    def check_string(self, letter):
        tmp_word, total_word = "", ""
        symbol = self.LETTER + [" ", '"'] + self.DIGIT
        current_state = 0
        final_state = [2]
        transition_table = [[1, -1, -1, -1], [2, 3, 4, 5], [-1, -1, -1, -1], [2, 3, 4, 5], [2, 3, 4, 5], [2, 3, 4, 5]]
        if letter == "":
            letter = self.input_file.read(1)
        while letter in symbol:
            total_word = total_word + letter
            letter = self.input_file.read(1)

        # Analyze
        for c in total_word:
            if c == '"':
                current_state = transition_table[current_state][0]
            elif c in self.LETTER:
                current_state = transition_table[current_state][1]
            elif c in self.DIGIT:
                current_state = transition_table[current_state][2]
            elif c == ' ':
                current_state = transition_table[current_state][3]
            else:
                return tmp_word, False, letter
            tmp_word = tmp_word + c

            if current_state == -1:
                return tmp_word, False, letter

        if current_state in final_state:
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    def run(self):
        result_table = list()
        line_number = 1
        word = ""
        letter = ""
        while True:
            #print(result_table)
            if letter == '':
                letter = self.input_file.read(1)  # 1글자 읽어옴
            if letter == "" and word == "": # 반복문 탈출
                break

            if letter not in self.STRING and word == "":  # ??
                try:
                    f = open(file_name[:-2] + '_error.out', 'w')
                    f.write("1Line" + str(line_number) + ": Wrong input format" + letter)
                    f.close()
                    print("1Line" + str(line_number) + ": Wrong input format" + letter)
                    exit()
                except:
                    print("Failed to write file")
                    exit()
            if letter == "\n":  # 엔터 입력
                line_number += 1
                letter = ""
                continue
            elif letter in self.WHITESPACE:  # whitespace
                letter = ""
                continue

            word += letter
            letter = ""

            if word in self.LETTER:
                if letter == "":
                    letter = self.input_file.read(1)

                while letter in self.LETTER:
                    word += letter
                    letter = self.input_file.read(1)

                if letter in self.DIGIT:
                    continue

                if word in self.VARIABLE:
                    result_table.append(['variable type', word])
                    word = ""
                    continue

                elif word in self.KEYWORD:
                    result_table.append([word, word])
                    word = ""
                    continue

            if word in self.ASSIGN:
                if letter == "":
                    letter = self.input_file.read(1)

                if word + letter in self.COMPARISON:  # =>, ==
                    result_table.append(['comparison', word+letter])
                    word, letter = "", ""
                else:  # =
                    result_table.append(['assign', word])
                    word = ""
                continue

            if word in ['-']:
                if (len(result_table) != 0) and (
                        ('num' in result_table[-1]) or ('id' in result_table[-1]) or (')' in result_table[-1])):
                    result_table.append(['addsub', word])
                    # letter = ""
                    word = ""
                    continue

            if word in self.MERGE + ['!']:
                if word in ['<', '>']:  # <, >가 포함된 문자열
                    if letter == "":
                        letter = self.input_file.read(1)
                    if word+letter in self.COMPARISON:
                        result_table.append(['comparison', word + letter])
                        word = ""
                        continue
                    elif word in self.COMPARISON:
                        result_table.append(['comparison', word])
                        word = ""
                        continue
                elif word == "!":
                    if letter == "":
                        letter = self.input_file.read(1)
                    if letter == "=":
                        result_table.append(['comparison', word + letter])
                        word = ""
                        continue
                    else:
                        try:
                            f = open(file_name[:-2] + '_error.out', 'w')
                            f.write("Line " + str(line_number) + ": Wrong input format")
                            f.close()
                            print("Line " + str(line_number) + ": Wrong input format")
                            exit()
                        except:
                            print("Fail to write file")
                            exit()

                if word in self.SEMICOLON:  # 세미콜론
                    result_table.append(['semicolon', word])
                elif word in self.BRACE:  # 중괄호
                    if word == '{':
                        result_table.append(['lbrace', word])
                    else:
                        result_table.append(['rbrace', word])
                elif word in self.PAREN:  # 소괄호
                    if word == '(':
                        result_table.append(['lparen', word])
                    elif word == ')':
                        result_table.append(['rparen', word])
                elif word in self.COMMA:  # 콤마
                    result_table.append(['comma', word])
                elif word in self.OPERATOR:
                    result_table.append(['operator', word])
                word = ""
                continue

            if word[0] in self.DIGIT + ['-']:
                word, is_int, letter = self.check_int(word, letter)

                if is_int:  # int임
                    result_table.append(['num', word])
                    word = ""
                    continue
                else:
                    if word == '-':
                        word = word + letter
                        letter = ""
                        continue

            if word[0] in self.LETTER:
                word, is_id, letter = self.check_id(word, letter)
                if is_id:  # identifier
                    result_table.append(['id', word])
                    word = ""
                    continue
                else:
                    try:
                        f = open(file_name[:-2] + '_error.out', 'w')
                        f.write("Line " + str(line_number) + ": Wrong input format")
                        f.close()
                        print("Line " + str(line_number) + ": Wrong input format")
                        exit()
                    except:
                        print("Fail to write file")
                        exit()
            if word[0] == '"':  # 따옴표 만남
                word, is_string, letter = self.check_string(word)
                if is_string:  # string이 맞음
                    result_table.append(['literal', word])
                    word = ""
                    continue
                else:  # error 처리
                    try:
                        f = open(file_name[:-2] + "_error.out", 'w')
                        f.writelines("Line" + str(line_number) + ": Wrong input stream")
                        f.close()
                        print("Line" + str(line_number) + ": Wrong input stream")
                        exit()
                    except:
                        print("Fail to write file")
                        exit()

        return result_table


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    '''if len(sys.argv) != 2:
        print("Input error")
        exit()'''

        # Open file for reading
    try:
        file_name = sys.argv[1]
        # file_name = "test.c"
        f = open(file_name)
        # Run lexical Analyzer
        la = LexicalAnalyzer(f)
        symbol_table = la.run()

        # Close the file
        f.close()
    except Exception as e:
        print("Fail to read file")
        print(e)
        exit()

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