import sys
import os
import copy


class SyntaxAnalyzer(object):
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

    # Variables
    file = None  # input text file
    terminal_list = []  # input terminal
    list_for_error_check = []

    def __init__(self, file):
        # Get text file
        self.file = file

    def readFile(self):
        lines = self.file.readlines()
        for line in lines:
            terminal = line.split()[0]
            self.terminal_list.append(terminal)

            # Print for debugging
            #print(terminal)
        self.terminal_list.append(self.END_MARK)
        self.list_for_error_check = copy.deepcopy(self.terminal_list)

    def run(self):
        # Read file
        self.readFile()
        # only includes end mark
        if (len(self.terminal_list) == 1):
            return True, ''

        SLR_stack = [0]  # stack
        spliter_pos = 0  # position of spliter
        error_line = 1

        while (True):
            # current state
            current_state = SLR_stack[-1]
            print("current_state: "+ str(current_state))

            # next input symbol is deicded by position of spliter
            next_input_symbol = self.terminal_list[spliter_pos]
            #print(next_input_symbol, spliter_pos)
            # next input symbol shoud be in SLR_TABLE
            # if not, error
            if next_input_symbol not in self.SLR_TABLE[current_state].keys():
                report = "Error occurred in line " + str(error_line) + ", " + self.list_for_error_check[error_line - 1]
                print(report)
                return False, report

            # shift
            if self.SLR_TABLE[current_state][next_input_symbol] == 'acc':
                return True, ''

            elif self.SLR_TABLE[current_state][next_input_symbol][0] == 's':
                # move position of spliter
                spliter_pos = spliter_pos + 1
                error_line = error_line + 1
                # push stack to next state
                SLR_stack.append(int(self.SLR_TABLE[current_state][next_input_symbol][1:]))
            # reduce
            elif self.SLR_TABLE[current_state][next_input_symbol][0] == 'r':
                buf_string = self.SLR_TABLE[current_state][next_input_symbol][1:]
                # get rule , type is list
                buf_rule = self.RULES[buf_string].split()
                print(buf_string, buf_rule)`
                buf_length = len(buf_rule) - 2  # ex) 'STMT → VDECL' , we only need VDECL
                # revise terminal list
                for i in range(buf_length):
                    if (buf_rule[2] != 'epsilon'):  # if not epsilon
                        # pop out from stack
                        SLR_stack.pop()
                        self.terminal_list.pop(spliter_pos - i - 1)
                if (buf_rule[2] != 'epsilon'):  # if not epsilon
                    spliter_pos = spliter_pos - buf_length + 1
                else:  # if epsilon
                    spliter_pos = spliter_pos + 1
                # revise terminal list
                self.terminal_list.insert(spliter_pos - 1, buf_rule[0])
                current_state = SLR_stack[-1]
                # Print for debugging
                #print(self.terminal_list)
                print("check : "+str(buf_rule) +" "+str(len(self.terminal_list))+ " " +str(spliter_pos))
                if buf_rule[0] not in self.SLR_TABLE[current_state].keys():
                    report = "Error occurred in line2 " + str(error_line) + ", " + self.list_for_error_check[
                        error_line - 1]
                    #print(report)
                    return False, report
                SLR_stack.append(self.SLR_TABLE[current_state][buf_rule[0]])


# Main function
if __name__ == "__main__":
    # Check the input commend
    if len(sys.argv) != 2:
        print("Input error")
        exit()

    # Check the file existence
    if os.path.isfile(sys.argv[1]):
        # Open file for reading
        try:
            file_name = sys.argv[1]
            f = open(file_name)
        except:
            print("Fail to read file")
            exit()
    else:
        print("Cannot find file")
        exit()

    sa = SyntaxAnalyzer(f)
    result, report = sa.run()

    # Close the file
    f.close()

    # Result
    if result:
        print("Accepted")
    else:
        print("Reject")

        # Open file for writing result
        try:
            f = open(file_name[:-4] + '_error.out', 'w')
        except:
            print("Fail to write file")
            exit()
        f.writelines(report + '\n')
        f.close()
