import sys
import os


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
    LETTER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
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
                    result_table.append(['vtype', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue

                elif word in self.KEYWORD:  # word가 keyword(if, else, while, return)일 경우
                    result_table.append([word.lower(), word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue

            if word in self.ASSIGN:  # word가 =일 경우
                if letter == "":  # letter 없을 경우
                    letter = self.input_file.read(1)  # 한 글자 읽어오기

                if word + letter in self.COMPARISON:  # word+letter가 =>,==일 경우
                    result_table.append(['comp', word + letter])  # result_table에 삽입
                    word, letter = "", ""  # word, letter 초기화
                else:  # =일 경우
                    result_table.append(['assign', word])  # result_table에 삽입
                    word= "" # word 초기화
                continue

            if word in ['-']:  # word가 '-'일 경우
                if (len(result_table) != 0) and (
                        ('num' in result_table[-1]) or ('id' in result_table[-1]) or (
                        ')' in result_table[-1])):  # 앞에 num,id,)가 있다면 -부호가 아닌 연산자 -임.
                    result_table.append(['addsub', word])  # result_table에 삽입
                    # letter = ""
                    word = ""  # word 초기화
                    continue

                letter2 = self.input_file.read(1)  # 파일 한글자 더 읽기
                if letter2 in self.ZERO:  # -뒤에 있는 숫자가 0일 경우
                    result_table.append(['addsub', word])  # result_table에 삽입
                    result_table.append(['num', '0'])  # result_table에 num, 0 삽입
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
                        result_table.append(['comp', word + letter])  # result_table에 삽입
                        word, letter = "", ""  # word 초기화
                        continue
                    elif word in self.COMPARISON:  # word가 <,>일 경우
                        result_table.append(['comp', word])  # result_table에 삽입
                        word = ""  # word 초기화
                        continue
                elif word == "!":  # word가 !일 경우
                    if letter == "":  # letter 없을 경우
                        letter = self.input_file.read(1)  # 한 글자 읽어오기
                    if letter == "=":  # letter가 =일 경우, 즉 word+letter가 !=일 경우
                        result_table.append(['comp', word + letter])  # result_table에 삽입
                        word, letter = "", ""  # word  초기화
                        continue
                    else:
                        LexicalAnalyzer.make_error(line_number, "Invalid comparison combination")  # 에러

                if word in self.SEMICOLON:  # word가 세미콜론일 경우
                    result_table.append(['semi', word])
                elif word in self.BRACE:  # word가 중괄호일 경우
                    if word == '{':
                        result_table.append(['lbrace', word])
                    else:
                        result_table.append(['rbrace', word])
                elif word in self.PAREN:  # word가 소괄호일 경우
                    if word == '(':
                        result_table.append(['lparen', word])
                    elif word == ')':
                        result_table.append(['rparen', word])
                elif word in self.COMMA:  # word가 콤마일 경우
                    result_table.append(['comma', word])
                elif word in self.OPERATOR:  # word가 연산자일 경우
                    if word == '+' or word == '-':
                        result_table.append(['addsub', word])
                    else:
                        result_table.append(['multdiv', word])
                word = ""  # word 초기화
                continue

            if word[0] in self.DIGIT + ['-']:  # int일때
                word, is_int, letter = self.check_int(word, letter)  # check_int에서 인자 3개 받아오기

                if is_int:  # int이면
                    result_table.append(['num', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # is_int가 False이면
                    if word == '-':  # word가 -이면
                        word = word + letter  # word뒤에 letter 합친 후
                        letter = ""  # letter 초기화
                        continue
                    else:
                        LexicalAnalyzer.make_error(line_number, "Invalid format for num")

            if word[0] in self.LETTER:  # id이면
                word, is_id, letter = self.check_id(word, letter)  # check_id에서 인자 3개 받아오기
                if is_id:  # id이면
                    result_table.append(['id', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # False이면
                    LexicalAnalyzer.make_error(line_number, "Invalid format for id")  # 에러

            if word[0] == '"':  # string일때
                word, is_string, letter = self.check_string(word)  # check_string에서 인자 3개 받아오기
                if is_string:  # string이면
                    result_table.append(['literal', word])  # result_table에 삽입
                    word = ""  # word 초기화
                    continue
                else:  # error 처리
                    LexicalAnalyzer.make_error(line_number, "Invalid format for literal")  # 에러

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


class SyntaxAnalyzer:
    # end mark
    END_MARK = '$'

    # rules
    RULES = {'0': 'S → CODE',
             '1': 'CODE → VDECL CODE',
             '2': 'CODE → FDECL CODE',
             '3': 'CODE → epsilon',
             '4': 'VDECL → vtype id semi',
             '5': 'FDECL → vtype id lparen ARG rparen lbrace BLOCK RETURN rbrace',
             '6': 'ARG → vtype id MOREARGS',
             '7': 'ARG → epsilon',
             '8': 'MOREARGS → comma vtype id MOREARGS',
             '9': 'MOREARGS → epsilon',
             '10': 'BLOCK → STMT BLOCK',
             '11': 'BLOCK → epsilon',
             '12': 'STMT → VDECL',
             '13': 'STMT → id assign RHS semi',
             '14': 'STMT → if lparen COND rparen lbrace BLOCK rbrace else lbrace BLOCK rbrace',
             '15': 'STMT → while lparen COND rparen lbrace BLOCK rbrace',
             '16': 'RHS → EXPR',
             '17': 'RHS → literal',
             '18': 'EXPR → TERM addsub EXPR',
             '19': 'EXPR → TERM',
             '20': 'TERM → FACTOR multdiv TERM',
             '21': 'TERM → FACTOR',
             '22': 'FACTOR → lparen EXPR rparen',
             '23': 'FACTOR → id',
             '24': 'FACTOR → num',
             '25': 'COND → FACTOR comp FACTOR',
             '26': 'RETURN → return FACTOR semi'}

    # SLR table
    SLR_TABLE = [{'vtype': 's4', '$': 'r3', 'CODE': 1, 'VDECL': 2, 'FDECL': 3},
                 {'$': 'acc'},
                 {'vtype': 's4', '$': 'r3', 'CODE': 5, 'VDECL': 2, 'FDECL': 3},
                 {'vtype': 's4', '$': 'r3', 'CODE': 6, 'VDECL': 2, 'FDECL': 3},
                 {'id': 's7'},
                 {'$': 'r1'},
                 {'$': 'r2'},
                 {'semi': 's8', 'lparen': 's9'},
                 {'vtype': 'r4', 'id': 'r4', 'rbrace': 'r4', 'if': 'r4', 'while': 'r4', 'return': 'r4', '$': 'r4'},
                 {'vtype': 's11', 'rparen': 'r7', 'ARG': 10},
                 {'rparen': 's12'},
                 {'id': 's13'},
                 {'lbrace': 's14'},
                 {'rparen': 'r9', 'comma': 's16', 'MOREARGS': 15},
                 {'vtype': 's23', 'id': 's20', 'rbrace': 'r11', 'if': 's21', 'while': 's22', 'return': 'r11', 'VDECL': 19, 'BLOCK': 17, 'STMT': 18},
                 {'rparen': 'r6'},
                 {'vtype': 's24'},
                 {'return': 's26', 'RETURN': 25},
                 {'vtype': 's23', 'id': 's20', 'rbrace': 'r11', 'if': 's21', 'while': 's22', 'return': 'r11', 'VDECL': 19, 'BLOCK': 27, 'STMT': 18},
                 {'vtype': 'r12', 'id': 'r12', 'rbrace': 'r12', 'if': 'r12', 'while': 'r12', 'return': 'r12'},
                 {'assign': 's28'},
                 {'lparen': 's29'},
                 {'lparen': 's30'},
                 {'id': 's31'},
                 {'id': 's32'},
                 {'rbrace': 's33'},
                 {'id': 's36', 'lparen': 's35', 'num': 's37', 'FACTOR': 34},
                 {'rbrace': 'r10', 'return': 'r10'},
                 {'id': 's36', 'lparen': 's35', 'literal': 's40', 'num': 's37', 'RHS': 38, 'EXPR': 39, 'TERM': 41, 'FACTOR': 42},
                 {'id': 's36', 'lparen': 's35', 'num': 's37', 'FACTOR': 44, 'COND': 43},
                 {'id': 's36', 'lparen': 's35', 'num': 's37', 'FACTOR': 44, 'COND': 45},
                 {'semi': 's8'},
                 {'rparen': 'r9', 'comma': 's16', 'MOREARGS': 46},
                 {'vtype': 'r5', '$': 'r5'},
                 {'semi': 's47'},
                 {'id': 's36', 'lparen': 's35', 'num': 's37', 'EXPR': 48, 'TERM': 41, 'FACTOR': 42},
                 {'semi': 'r23', 'rparen': 'r23', 'addsub': 'r23', 'multdiv': 'r23', 'comp': 'r23'},
                 {'semi': 'r24', 'rparen': 'r24', 'addsub': 'r24', 'multdiv': 'r24', 'comp': 'r24'},
                 {'semi': 's49'},
                 {'semi': 'r16'},
                 {'semi': 'r17'},
                 {'semi': 'r19', 'rparen': 'r19', 'addsub': 's50'},
                 {'semi': 'r21', 'rparen': 'r21', 'addsub': 'r21', 'multdiv': 's51'},
                 {'rparen': 's52'}, {'comp': 's53'}, {'rparen': 's54'},
                 {'rparen': 'r8'},
                 {'rbrace': 'r26'},
                 {'rparen': 's55'},
                 {'vtype': 'r13', 'id': 'r13', 'rbrace': 'r13', 'if': 'r13', 'while': 'r13', 'return': 'r13'},
                 {'id': 's36', 'lparen': 's35', 'num': 's37', 'EXPR': 56, 'TERM': 41, 'FACTOR': 42},
                 {'id': 's36', 'lparen': 's35', 'num': 's37', 'TERM': 57, 'FACTOR': 42},
                 {'lbrace': 's58'},
                 {'id': 's36', 'lparen': 's35', 'num': 's37', 'FACTOR': 59},
                 {'lbrace': 's60'},
                 {'semi': 'r22', 'rparen': 'r22', 'addsub': 'r22', 'multdiv': 'r22', 'comp': 'r22'},
                 {'semi': 'r18', 'rparen': 'r18'},
                 {'semi': 'r20', 'rparen': 'r20', 'addsub': 'r20'},
                 {'vtype': 's23', 'id': 's20', 'rbrace': 'r11', 'if': 's21', 'while': 's22', 'return': 'r11', 'VDECL': 19, 'BLOCK': 61, 'STMT': 18},
                 {'rparen': 'r25'},
                 {'vtype': 's23', 'id': 's20', 'rbrace': 'r11', 'if': 's21', 'while': 's22', 'return': 'r11', 'VDECL': 19, 'BLOCK': 62, 'STMT': 18},
                 {'rbrace': 's63'},
                 {'rbrace': 's64'},
                 {'else': 's65'},
                 {'vtype': 'r15', 'id': 'r15', 'rbrace': 'r15', 'if': 'r15', 'while': 'r15', 'return': 'r15'},
                 {'lbrace': 's66'},
                 {'vtype': 's23', 'id': 's20', 'rbrace': 'r11', 'if': 's21', 'while': 's22', 'return': 'r11', 'VDECL': 19, 'BLOCK': 67, 'STMT': 18},
                 {'rbrace': 's68'},
                 {'vtype': 'r14', 'id': 'r14', 'rbrace': 'r14', 'if': 'r14', 'while': 'r14', 'return': 'r14'}]

    analyzer_table = []   # lexical analyzer result table
    error_table = []
    error_row = 1

    def __init__(self, analyzer_table):
        for row in analyzer_table:
            self.analyzer_table.append(row[0])

        self.analyzer_table.append(self.END_MARK)
        self.error_table = list(self.analyzer_table)

    def run(self):
        if len(self.analyzer_table) == 1:
            return True

        syntax_stack = [0]  # slr stack
        spliter_position = 0   # spliter position

        while True:
            current_state = syntax_stack[-1]
            next_terminal = self.analyzer_table[spliter_position]

            if next_terminal not in self.SLR_TABLE[current_state].keys():
                return False

            # shift
            if self.SLR_TABLE[current_state][next_terminal] == 'acc':
                return True

            elif self.SLR_TABLE[current_state][next_terminal][0] == 's':
                # move position of spliter
                spliter_position += 1
                self.error_row += 1
                # push stack to next state
                syntax_stack.append(int(self.SLR_TABLE[current_state][next_terminal][1:]))

            elif self.SLR_TABLE[current_state][next_terminal][0] == 'r':
                reduce_num = self.SLR_TABLE[current_state][next_terminal][1:]
                reduce_cfg_rule = self.RULES[reduce_num].split()

                for i in range(len(reduce_cfg_rule) - 2):
                    if reduce_cfg_rule[2] != 'epsilon':  # if not epsilon
                        del self.analyzer_table[spliter_position - i - 1]
                        syntax_stack.pop()
                if reduce_cfg_rule[2] != 'epsilon':  # if not epsilon
                    spliter_position -= len(reduce_cfg_rule) + 3
                else:  # if epsilon
                    spliter_position += 1

                self.analyzer_table.insert(spliter_position - 1, reduce_cfg_rule[0])
                current_state = syntax_stack[-1]
                if reduce_cfg_rule[0] not in self.SLR_TABLE[current_state].keys():
                    return False
                syntax_stack.append(self.SLR_TABLE[current_state][reduce_cfg_rule[0]])

    def print_error(self):
        return f"Line {str(self.error_row)} : {self.error_table[self.error_row-1]}"


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
        read_f = open(file_name)  # 파일 열기
        lexical_analyzer = LexicalAnalyzer(read_f)  # class 불러오기
        analyzer_table = lexical_analyzer.run()  # LexicalAnalyzer에서 run() 실행후 result_table을 symbol_table에 넣기
        read_f.close()  # 파일 닫기

        write_f = open(file_name[:-2] + '_lexical.out', 'w')
        # out 파일에 결과 적기
        for i in analyzer_table:
            token = i[0]
            lexeme = i[1]
            write_f.writelines(str(token) + ' ' + str(lexeme) + '\n')
        write_f.close()  # 파일 닫기

        syntax_analyzer = SyntaxAnalyzer(analyzer_table)
        is_accepted = syntax_analyzer.run()

        if is_accepted:
            print("This Program is Accepted")
        else:
            print("This Program is Rejected")
            try:
                syntax_error_f = open(file_name[:-2] + '_error.out', 'w')
                syntax_error_f.write(f"Line {syntax_analyzer.error_row} : {syntax_analyzer.error_table[syntax_analyzer.error_row - 1]}")
                syntax_error_f.close()
            except IOError as e:
                print("Fail to read/write file " + e.filename)
                exit()

    except IOError as e:  # IO Error 처리
        print("Fail to read/write file " + e.filename)
        exit()