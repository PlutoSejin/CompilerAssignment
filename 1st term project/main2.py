import sys


class LexicalAnalyzer(object):
    # 토큰 설정
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

    # Letter 설정
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

    # id check하기
    def check_id(self, word, letter):
        tmp_word = ""
        symbol = self.LETTER + self.DIGIT  # id DFA가 인식 가능한 symbol
        current_state = 0  # 현재 state
        final = [1, 2, 3]  # final state table
        transition_table = [[1, -1], [2, 3], [2, 3], [2, 3]]  # id DFA state table

        if letter == "":  # letter가 비어 있는 경우 1byte 읽기
            letter = self.input_file.read(1)

        while letter in symbol:  # letter가 symbol에 있을 때까지 입력 받기
            word = word + letter
            letter = self.input_file.read(1)

        # word 분석
        for c in word:  # 각 글자에 맞춰 state 이동
            if c in self.LETTER:
                current_state = transition_table[current_state][0]
            elif c in self.DIGIT:
                current_state = transition_table[current_state][1]
            else:
                return tmp_word, False, letter
            tmp_word = tmp_word + c

            if current_state == -1:  # 존재하지 않는 경로
                return tmp_word, False, letter

        # 주어진 word 모두 확인한 후
        if current_state in final:  # final state에 존재하는지 확인
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    # int check하기
    def check_int(self, word, letter):
        print("word letter"+str(word)+" "+str(letter))
        tmp_word = ""
        symbol = ['-'] + self.DIGIT  # int DFA에서 인식 가능한 symbol 정의
        current_state = 0  # 현재 state
        final_state = [2, 3, 4, 5]  # final state table
        transition_table = [[1, 2, 3], [-1, -1, 3], [-1, -1, -1], [-1, 4, 5], [-1, 4, 5],
                            [-1, 4, 5]]  # int DFA state table

        if letter == "":  # letter가 비어있으면 1byte 읽기
            letter = self.input_file.read(1)

        while letter in symbol:  # 인자로 들어온 word 뒤에 추가할 글자가 없을 때까지 읽기
            if word[-1] in self.DIGIT and letter == '-':  # 마지막 글자가 DIGIT이고 새로 받은 단어가 -인 경우
                break
            word = word + letter
            letter = self.input_file.read(1)

<<<<<<< HEAD
        print("letter: "+str(letter))

        # Analyze하기
        for c in word:
            if c == '-':  #c가 '-'이면 j를 0으로 설정
=======
        # word 분석
        for c in word:  # 글자에 맞춰 state 이동
            if c == '-':
>>>>>>> 409b01a0a89ebbfb48fc3713dac76cab4088b23b
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

        if current_state in final_state:  # 최종 state가 final state인지 확인
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    # string check
    def check_string(self, letter):
        tmp_word, total_word = "", ""
        symbol = self.LETTER + [" ", '"'] + self.DIGIT  # string DFA가 인식할 수 있는 symbol
        current_state = 0  # 현재 state
        final_state = [2]  # final state table
        transition_table = [[1, -1, -1, -1], [2, 3, 4, 5], [-1, -1, -1, -1], [2, 3, 4, 5], [2, 3, 4, 5],
                            [2, 3, 4, 5]]  # string DFA state table

        if letter == "":  # letter가 비어 있으면 1byte 추가로 읽기
            letter = self.input_file.read(1)

        while letter in symbol:  # letter가 symbol에 존재하지 않을 때까지 글자 읽기
            total_word = total_word + letter
            letter = self.input_file.read(1)

        # Analyze하기
        for c in total_word:  # 글자에 맞춰 state 이동
            if c == '"':
                current_state = transition_table[current_state][0]
<<<<<<< HEAD
            elif c in self.LETTER: #c가 LETTER이면 j를 1로 설정
                tmp_word = tmp_word + c
                current_state = transition_table[current_state][1]
            elif c in self.DIGIT: #c가 DIGIT이면 j를 2로 설정
                tmp_word = tmp_word + c
                current_state = transition_table[current_state][2]
            elif c == ' ': #c가 ' '이면 j를 3으로 설정
                tmp_word = tmp_word + c
=======
            elif c in self.LETTER:
                current_state = transition_table[current_state][1]
            elif c in self.DIGIT:
                current_state = transition_table[current_state][2]
            elif c == ' ':
>>>>>>> 409b01a0a89ebbfb48fc3713dac76cab4088b23b
                current_state = transition_table[current_state][3]
            else:
                return tmp_word, False, letter


            if current_state == -1:  # 존재하지 않는 경로
                return tmp_word, False, letter

        if current_state in final_state:  # 최종 state가 final state인지 확인
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    def run(self):
        result_table = list()  # lexeme와 token을 넣을 result_table 생성
        line_number = 1  # 현재 읽고 있는 파일의 줄
        word = ""  # 현재 읽고 있는 단어
        letter = ""  # 현재 읽어온 1byte 글자

        while True:

            if letter == '':  # letter에 아무 것도 없는 경우
                letter = self.input_file.read(1)  # 파일에서 1글자 읽기
            if letter == "" and word == "":  # 만약 letter와 word 모두 없을때 즉 파일을 다 읽었을때 반복문 탈출
                break

            if letter not in self.STRING and word == "":  # 위에서 선언한 STRING에 없을 경우
                try:  # 오류 파일 생성 후 오류 메세지 출력
                    f = open(file_name[:-2] + '_error.out', 'w')
                    f.write("Line" + str(line_number) + ": Wrong input format" + letter)
                    f.close()
                    print("Line" + str(line_number) + ": Wrong input format" + letter)
                    exit()
                except:  # 파일이 안적힐 경우
                    print("Failed to write file")
                    exit()

            if letter == "\n":  # 엔터 인식
                line_number += 1
                letter = ""  # letter 초기화
                continue
            elif letter in self.WHITESPACE:  # whitespace 인식
                letter = ""  # letter 초기화
                continue

            word += letter  # 엔터와 whitespace가 아닌 경우, word 뒤에 letter를 추가
            letter = ""

            if word in self.LETTER:  # word가 LETTER에 있다면
                if letter == "":  # letter가 비어 있는 경우
                    letter = self.input_file.read(1)  # 한 글자 읽어 오기

                while letter in self.LETTER:  # letter가 LETTER에 존재하지 않을 때까지 word에 letter 추가
                    word += letter
                    letter = self.input_file.read(1)

                if letter in self.DIGIT:  # letter가 숫자일 경우 (id)
                    continue

                if word in self.VARIABLE:  # word가 variable(int,char)일 경우
                    result_table.append(['variable type', word])  # result_table 에 삽입
                    word = ""  # word 초기화
                    continue

                elif word in self.KEYWORD:  # word가 keyword(if, else, while, return)일 경우
                    result_table.append([word, word])  # result_table 에 삽입
                    word = ""  # word 초기화
                    continue

            if word in self.ASSIGN:  # word에 =가 포함된 경우
                if letter == "":  # letter 비어 있는 경우
                    letter = self.input_file.read(1)  # 한 글자 읽어 오기

                if word + letter in self.COMPARISON:  # word+letter 가 =>,==일 경우
                    result_table.append(['comparison', word + letter])  # result_table 에 삽입
                    word, letter = "", ""  # word, letter 초기화
                else:  # =일 경우
                    result_table.append(['assign', word])  # result_table 에 삽입
                    word = ""  # word 초기화
                continue

<<<<<<< HEAD
            if word in ['-']: #word가 '-'일 경우
                #print(word)
=======
            if word in ['-']:  # word에 '-'가 포함된 경우
>>>>>>> 409b01a0a89ebbfb48fc3713dac76cab4088b23b
                if (len(result_table) != 0) and (
                        ('num' in result_table[-1]) or ('id' in result_table[-1]) or (
                        ')' in result_table[-1])):  # 앞에 num,id,)가 있다면 -는 부호가 아닌 연산자
                    result_table.append(['operator', word])  # result_table 에 삽입
                    word = ""  # word 초기화
                    continue

                letter2 = self.input_file.read(1)
                if letter2 in self.ZERO:
                    result_table.append(['operator', word])  # result_talbe에 삽입
                    # letter = ""
                    word = ""  # word 초기화
                    word += letter2
                    print("- word check: " + word)
                    continue
                word+=letter2

            if word in self.MERGE + ['!']:
                if word in ['<', '>']:  # word에 < 또는 >가 포함된 경우
                    if letter == "":  # letter 가 비어 있는 경우
                        letter = self.input_file.read(1)  # 한 글자 읽어 오기

                    if word + letter in self.COMPARISON:  # word가 <=, >=일 경우
                        result_table.append(['comparison', word + letter])  # result_table에 삽입
                        word = ""  # word 초기화
                        continue
                    elif word in self.COMPARISON:  # word가 <,>일 경우
                        result_table.append(['comparison', word])  # result_table에 삽입
                        word = ""  # word 초기화
                        continue
                elif word == "!":  # word가 !일 경우
                    if letter == "":  # letter 비어 있는 경우
                        letter = self.input_file.read(1)  # 한 글자 읽어 오기
                    if letter == "=":  # word + letter가 !=일 경우
                        result_table.append(['comparison', word + letter])  # result_table에 삽입
                        word = ""  # word 초기화
                        continue
                    else:
                        try:  # 오류파일 생성 후 오류 메세지 출력
                            f = open(file_name[:-2] + '_error.out', 'w')
                            f.write("Line " + str(line_number) + ": Wrong input format")
                            f.close()
                            print("Line " + str(line_number) + ": Wrong input format")
                            exit()
                        except Exception as err:  # 파일이 안적힐 경우
                            print("Fail to write file")
                            print(f"error : {err}")
                            exit()

                if word in self.SEMICOLON:  # word 세미콜론 분기
                    result_table.append(['semicolon', word])
                elif word in self.BRACE:  # word 중괄호 분기
                    if word == '{':
                        result_table.append(['lbrace', word])
                    else:
                        result_table.append(['rbrace', word])
                elif word in self.PAREN:  # word 소괄호 분기
                    if word == '(':
                        result_table.append(['lparen', word])
                    elif word == ')':
                        result_table.append(['rparen', word])
                elif word in self.COMMA:  # word 콤마 분기
                    result_table.append(['comma', word])
                elif word in self.OPERATOR:  # word 연산자 분기
                    result_table.append(['operator', word])
                word = ""  # word 초기화
                continue

            if word[0] in self.DIGIT + ['-']:  # int 인식
                word, is_int, letter = self.check_int(word, letter)  # 단어, int 여부, 읽던 글자 받아 오기

                if is_int:  # int인 경우
                    result_table.append(['num', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # int가 아닌 경우
                    if word == '-':  # word가 -인 경우
                        word = word + letter
                        letter = ""  # letter 초기화
                        continue

            if word[0] in self.LETTER:  # id 인식
                word, is_id, letter = self.check_id(word, letter)  # 단어, id 여부, 읽던 글자 받아오기
                if is_id:  # id 인 경우
                    result_table.append(['id', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # id가 아닌 경우
                    try:  # 오류 파일 생성 후 오류 메세지 출력
                        f = open(file_name[:-2] + '_error.out', 'w')
                        f.write("Line " + str(line_number) + ": Wrong input format")
                        f.close()
                        print("Line " + str(line_number) + ": Wrong input format")
                        exit()
                    except Exception as err:  # 파일 쓰기 오류
                        print("Fail to write file")
                        print(f"error : {err}")
                        exit()

            if word[0] == '"':  # string literal 인식
                word, is_string, letter = self.check_string(word)  # 단어, literal 여부, 읽던 글자 받아오기
                if is_string:  # string literal인 경우
                    result_table.append(['literal', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # error 처리
                    try:  # 오류 파일 생성 후 오류 메세지 출력
                        f = open(file_name[:-2] + "_error.out", 'w')
                        f.writelines("Line" + str(line_number) + ": Wrong input stream")
                        f.close()
                        print("Line" + str(line_number) + ": Wrong input stream")
                        exit()
                    except Exception as err:  # 파일 쓰기 오류
                        print("Fail to write file")
                        print(f"error : {err}")
                        exit()

        return result_table  # result_table 반환


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # 파일 읽기
    try:
        file_name = sys.argv[1]
        input_file = open(file_name)  # 파일 열기
        lexical_analyzer = LexicalAnalyzer(input_file)  # file_stream 설정
        analyzer_table = lexical_analyzer.run()  # 파일 분석
        # Close the file
        input_file.close()  # 파일 닫기

        for i in analyzer_table:  # analyzer_table 출력
            print(i[0], i[1])

        output_file = open(file_name[:-2] + '.out', 'w')
        # 결과 파일로 저장
        for i in analyzer_table:
            token = i[0]
            lexeme = i[1]
            output_file.writelines(token + ' ' + lexeme + '\n')
        output_file.close()  # 파일 닫기
    except Exception as err:  # error handle
        print(f"error : {err}")
        exit()