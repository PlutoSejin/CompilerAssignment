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
        symbol = self.LETTER + self.DIGIT  # id이기 때문에 LETTER과 DIGIT만 있어야하기 때문에 symbol에 넣기
        current_state = 0  # 현재 table 위치 표시
        final = [1, 2, 3]  # table 1,2,3에서 나가는건 가능하므로 final에 위치
        transition_table = [[1, -1], [2, 3], [2, 3], [2, 3]]  # id의 DFA의 인자들에서 갈 수 있는 table 위치

        if letter == "":  # letter가 아무것도 없으면 한 단어 읽어오기
            letter = self.input_file.read(1)

        while letter in symbol:  # 인자로 들어온 word 뒤에 추가할 인자가 있는지 확인, 만약 있다면 while로 계속 추가하기
            word = word + letter
            letter = self.input_file.read(1)

        # Analyze하기
        for c in word:
            if c in self.LETTER:  # c가 LETTER이면 j를 0으로 설정
                current_state = transition_table[current_state][0]
            elif c in self.DIGIT:  # c가 DIGIT이면 j를 1로 설정
                current_state = transition_table[current_state][1]
            else:  # c가 DIGIT, LETTER 모두 아니면
                return tmp_word, False, letter
            tmp_word = tmp_word + c

            if current_state == -1:  # 존재하지 않는 경로
                return tmp_word, False, letter

        # 주어진 word 모두 확인한 후
        if current_state in final:  # final state에 존재하는가
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    # int check하기
    def check_int(self, word, letter):
        tmp_word = ""
        symbol = ['-'] + self.DIGIT  # int이기 때문에 '-'와 DIGIT만 있어야하기 때문에 symbol에 넣기
        current_state = 0  # 현재 table 위치 표시
        final_state = [2, 3, 4, 5]  # table 2,3,4,5에서 나가는건 가능하므로 final에 위치
        transition_table = [[1, 2, 3], [-1, -1, 3], [-1, -1, -1], [-1, 4, 5], [-1, 4, 5],
                            [-1, 4, 5]]  # int의 DFA의 인자들에서 갈 수 있는 table 위치

        if letter == "":  # letter가 아무것도 없으면 단어 추가하기
            letter = self.input_file.read(1)

        while letter in symbol:  # 인자로 들어온 word 뒤에 추가할 인자가 있는지 확인, 만약 있다면 while로 계속 추가하기
            if word[-1] in self.DIGIT and letter == '-':  # 만약 앞에 있는 숫자가 있고 새로 받은 단어가 -면 break
                break
            word = word + letter
            letter = self.input_file.read(1)

        # Analyze하기
        for c in word:
            if c == '-':  # c가 '-'이면 j를 0으로 설정
                current_state = transition_table[current_state][0]
            elif c in self.ZERO:  # c가 0이면 j를 1로 설정
                current_state = transition_table[current_state][1]
            elif c in self.NON_ZERO:  # c가 NON_ZERO이면 j를 2로 설정
                current_state = transition_table[current_state][2]
            else:  # c가 '-',0,NON_ZERO가 아니면
                return tmp_word, True, letter
            tmp_word = tmp_word + c

            if current_state == -1:  # 존재하지 않는 경로
                return tmp_word, False, letter

        # 주어진 word 모두 확인한 후
        if current_state in final_state:  # final state에 존재하는가
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    # string check하기
    def check_string(self, letter):
        tmp_word, total_word = "", ""
        symbol = self.LETTER + [" ", '"'] + self.DIGIT  # string이기 때문에 ' ', '"'와 DIGIT와 LETTER만 있어야하기 때문에 symbol에 넣기
        current_state = 0  # 현재 table 위치 표시
        final_state = [2]  # table 2에서 나가는건 가능하므로 final에 위치
        transition_table = [[1, -1, -1, -1], [2, 3, 4, 5], [-1, -1, -1, -1], [2, 3, 4, 5], [2, 3, 4, 5],
                            [2, 3, 4, 5]]  # string의 DFA의 인자들에서 갈 수 있는 table 위치

        if letter == "":  # letter가 아무것도 없으면 단어 추가하기
            letter = self.input_file.read(1)

        while letter in symbol:  # 인자로 들어온 word 뒤에 추가할 인자가 있는지 확인, 만약 있다면 while로 계속 추가하기
            total_word = total_word + letter
            letter = self.input_file.read(1)

        # Analyze하기
        for c in total_word:
            if c == '"':  # c가 '"'이면 j를 0으로 설정
                current_state = transition_table[current_state][0]
            elif c in self.LETTER:  # c가 LETTER이면 j를 1로 설정
                tmp_word = tmp_word + c
                current_state = transition_table[current_state][1]
            elif c in self.DIGIT:  # c가 DIGIT이면 j를 2로 설정
                tmp_word = tmp_word + c
                current_state = transition_table[current_state][2]
            elif c == ' ':  # c가 ' '이면 j를 3으로 설정
                tmp_word = tmp_word + c
                current_state = transition_table[current_state][3]
            else:  # c가 '"',' ',LETTER,DIGIT이 아니면
                return tmp_word, False, letter

            if current_state == -1:  # 존재하지 않는 경로
                return tmp_word, False, letter

        # 주어진 word 모두 확인한 후
        if current_state in final_state:  # final state에 존재하는가
            return tmp_word, True, letter
        else:
            return tmp_word, False, letter

    def run(self):
        result_table = list()  # lexeme와 token을 넣을 result_table 생성
        line_number = 1  # 현재 읽고 있는 파일의 줄
        word = ""  # 현재 읽고 있는 단어
        letter = ""  # 한 단어씩 읽을 때 임시 저장

        while True:
            # 만약 letter에 아무것도 없을때
            if letter == '':
                letter = self.input_file.read(1)  # 1글자 읽어옴
            if letter == "" and word == "":  # 만약 letter와 word 모두 없을때 즉 파일을 다 읽었을때 반복문 탈출
                break

            if letter not in self.STRING and word == "":  # 위에서 선언한 STRING에 없을 경우
                LexicalAnalyzer.make_error(line_number, "Unsupported characters exist")

            if letter == "\n":  # 엔터 인식
                line_number += 1  # 다음 줄로 넘어가기
                letter = ""  # letter 초기화
                continue
            elif letter in self.WHITESPACE:  # whitespace 인식
                letter = ""  # letter 초기화
                continue

            word += letter  # 엔터와 whitespace가 아닐경우, word 뒤에 letter를 추가
            letter = ""

            if word in self.LETTER:  # word가 LETTER에 있다면
                if letter == "":  # letter 없을 경우
                    letter = self.input_file.read(1)  # 한 글자 읽어오기

                while letter in self.LETTER:  # letter가 LETTER에 있을 경우
                    word += letter  # word 뒤에 letter 추가
                    letter = self.input_file.read(1)  # 한 글자 읽어오기

                if letter in self.DIGIT:  # letter가 숫자일 경우
                    continue  # id이기 때문에 위로 이동

                if word in self.VARIABLE:  # word가 variable(int,char)일 경우
                    result_table.append(['VTYPE', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue

                elif word in self.KEYWORD:  # word가 keyword(if, else, while, return)일 경우
                    result_table.append([word.upper(), word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue

            if word in self.ASSIGN:  # word가 =일 경우
                print(letter, word)
                if letter == "":  # letter 없을 경우
                    letter = self.input_file.read(1)  # 한 글자 읽어오기

                if word + letter in self.COMPARISON:  # word+letter가 =>,==일 경우
                    result_table.append(['COMPARISON', word + letter])  # result_table에 삽입
                    word, letter = "", ""  # word, letter 초기화
                else:  # =일 경우
                    result_table.append(['ASSIGN', word])  # result_table에 삽입
                    word, letter = "",""  # word 초기화
                continue

            if word in ['-']:  # word가 '-'일 경우
                if (len(result_table) != 0) and (
                        ('INTEGER' in result_table[-1]) or ('ID' in result_table[-1]) or (
                        ')' in result_table[-1])):  # 앞에 num,id,)가 있다면 -부호가 아닌 연산자 -임.
                    result_table.append(['OP', word])  # result_table에 삽입
                    # letter = ""
                    word = ""  # word 초기화
                    continue

                letter2 = self.input_file.read(1)  # 파일 한글자 더 읽기
                if letter2 in self.ZERO:  # -뒤에 있는 숫자가 0일 경우
                    result_table.append(['OP', word])  # result_table에 삽입
                    result_table.append(['INTEGER', '0'])  # result_table에 num, 0 삽입
                    word = ""  # word 초기화
                    continue
                elif letter2 in self.LETTER:  # 뒤에 있는 글자가 알파벳일 경우
                    LexicalAnalyzer.make_error(line_number, "Unacceptable format")  # 에러
                word += letter2  # 먼저 읽었던 단어 추가

            if word in self.MERGE + ['!']:
                if word in ['<', '>']:  # word가 <, >일 경우
                    if letter == "":  # letter 없을 경우
                        letter = self.input_file.read(1)  # 한 글자 읽어오기

                    if word + letter in self.COMPARISON:  # word가 <=일 경우
                        result_table.append(['COMPARISON', word + letter])  # result_table에 삽입
                        word, letter = "",""  # word 초기화
                        continue
                    elif word in self.COMPARISON:  # word가 <,>일 경우
                        result_table.append(['COMPARISON', word])  # result_table에 삽입
                        word = ""  # word 초기화
                        continue
                elif word == "!":  # word가 !일 경우
                    if letter == "":  # letter 없을 경우
                        letter = self.input_file.read(1)  # 한 글자 읽어오기
                    if letter == "=":  # letter가 =일 경우, 즉 word+letter가 !=일 경우
                        result_table.append(['COMPARISON', word + letter])  # result_table에 삽입
                        word, letter = "",""  # word  초기화
                        continue
                    else:
                        LexicalAnalyzer.make_error(line_number, "Invalid COMPARISON combination")  # 에러

                if word in self.SEMICOLON:  # word가 세미콜론일 경우
                    result_table.append(['SEMI', word])
                elif word in self.BRACE:  # word가 중괄호일 경우
                    if word == '{':
                        result_table.append(['LBRACE', word])
                    else:
                        result_table.append(['RBRACE', word])
                elif word in self.PAREN:  # word가 소괄호일 경우
                    if word == '(':
                        result_table.append(['LPAREN', word])
                    elif word == ')':
                        result_table.append(['RPAREN', word])
                elif word in self.COMMA:  # word가 콤마일 경우
                    result_table.append(['COMMA', word])
                elif word in self.OPERATOR:  # word가 연산자일 경우
                    result_table.append(['OP', word])
                word = ""  # word 초기화
                continue

            if word[0] in self.DIGIT + ['-']:  # int일때
                word, is_int, letter = self.check_int(word, letter)  # check_int에서 인자 3개 받아오기

                if is_int:  # int이면
                    result_table.append(['INTEGER', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # is_int가 False이면
                    if word == '-':  # word가 -이면
                        word = word + letter  # word뒤에 letter 합친 후
                        letter = ""  # letter 초기화
                        continue

            if word[0] in self.LETTER:  # id이면
                word, is_id, letter = self.check_id(word, letter)  # check_id에서 인자 3개 받아오기
                if is_id:  # id이면
                    result_table.append(['ID', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # False이면
                    LexicalAnalyzer.make_error(line_number, "Invalid format for ID")  # 에러

            if word[0] == '"':  # string일때
                word, is_string, letter = self.check_string(word)  # check_string에서 인자 3개 받아오기
                if is_string:  # string이면
                    result_table.append(['STRING', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # error 처리
                    LexicalAnalyzer.make_error(line_number, "Invalid format for STRING")  # 에러

        return result_table  # result_table 반환

    @staticmethod
    def make_error(line_number, error_string):  # 에러 함수
        try:  # 오류파일 생성 후 오류 메세지 적고 출력
            f = open(file_name[:-2] + "_error.out", 'w')  # 에러 파일 만들기
            f.writelines(f"Line {str(line_number)} : {error_string}")  # 에러 내용 적기
            f.close()
            print(f"Line {str(line_number)} : {error_string}")
            exit()
        except IOError as e:  # 파일이 안적힐 경우
            print("Fail to write file " + e.filename)
            exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 파일 읽기
    try:
        file_name = sys.argv[1]
        read_f = open(file_name)  # 파일 열기
        lexical_analyzer = LexicalAnalyzer(read_f)  # class 불러오기
        analyzer_table = lexical_analyzer.run()  # LexicalAnalyzer에서 run() 실행후 result_table을 symbol_table에 넣기
        read_f.close()  # 파일 닫기

        write_f = open(file_name[:-2] + '.out', 'w')
        # out 파일에 결과 적기
        for i in analyzer_table:
            token = i[0]
            lexeme = i[1]
            write_f.writelines(str(token) + ' ' + str(lexeme) + '\n')
            print(i[0], i[1])
        write_f.close()  # 파일 닫기
    except IOError as e:  # IO Error 처리
        print("Fail to read/write file " + e.filename)
        exit()
