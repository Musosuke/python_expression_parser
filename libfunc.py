# to validate numbers and symbols
import re

# import a queue
from queue import Queue
# import a stack
from queue import LifoQueue


def IsNumber(param):
    # to write rule in BNF form
    # determine whether this string is in the form of a number
    # . symbol  -> + | -
    # . digit   -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    # . point   -> .
    # . number  -> digit | digit number
    # . decimal -> digit | digit decimal
    # . number  -> decimal | decimal point decimal
    # . grammar -> ( symbol | none ) number
    # below is the code to implement the above grammar by using regex

    # check if param is a integer or float
    realNumber_pattern = '^[+-]?(\d+|\d+\.\d+)$'
    match = re.fullmatch(realNumber_pattern, param)

    if match:
        return True
    else:
        return False


def IsVariable(param):
    # determine which param is algebraic variable or not,
    # variable name rule same as like programming languauge
    # cannot start with number
    # can only contain number and alphabet
    # reserved symbols are not allowed to be used
    # reserved symbols: + - * / % ^ ( ) . , ; : ' " [ ] { } = ! ? < > | & ~

    for item in param:
        # why there's a test function for python to check param is composed of number or alphabet?
        if not item.isalnum():
            return False
    return True


def IsSymbol(param):
    # just another verify function to return bool result
    # for in case of my code flow will be apparently readable
    symbol_pattern = r'+-/*%^()'
    if not len(param) == 1:
        #raise Exception("IsSymbol: param is not a single symbol")
        return False
    if param in symbol_pattern:
        return True
    return False


def parseExpression_Dijkstra(expression):
    # split numbers and symbols
    # if match pattern,append to a new list
    symbol_pattern = r'[+-/*%^()]'
    num_pattern = r'[+-]?(\d+|\d+\.\d+)'
    # using test_pattern to split number and symbol in same list
    test_pattern = r'('+symbol_pattern+')|('+num_pattern+')'
    match_lists = re.findall(test_pattern, expression)
    # select non-empty result to append,
    # avoid return result of re.findall is group structure
    # because there are three types of result in group structure
    result = []
    for match in match_lists:
        for item in match:
            if item != '':
                result.append(item)
                break

    return result


def solution(expression):
    # using queue to store numbers and operators
    # RPN ,an type of suffix expression
    # after processed, 
    # queue will have numbers and symbols present in suffix way 
    processing_queue = Queue()
    # using stack to store symbols
    symbol_stack = LifoQueue()

    exception_flag = False

    symbol_priority = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '%': 2,
        '^': 3,
        # there's no need to store '(' in stack,
        # a tricky point will be that parenthesis has no priority
        '(': 0,
        ')': 0
    }

    for item in expression:
        # numbers always push into queue
        # symbol push into stack, then back to queue by priority
        if IsNumber(item):
            processing_queue.put(item)
        # if is not number
        elif IsSymbol(item):
            # compare stack top's priority with current item
            # if stack is empty, push item into stack
            if symbol_stack.empty():
                symbol_stack.put(item)

            else:
                if item == '(':
                    # if item is '(' , push into stack unconditional
                    symbol_stack.put(item)
                elif item == ')':
                    # check whether parentheses are paired or not
                    while True:
                        if symbol_stack.empty():
                            exception_flag = True
                            break
                        else:
                            stack_top = symbol_stack.get()
                            if stack_top == '(':
                                # paired to last '(' on top of stack
                                break
                            else:
                                processing_queue.put(stack_top)
                else:
                    stack_top = symbol_stack.get()

                    if stack_top == '^' and item == '^':
                        # ^ priority is increment when stack top is '^',
                        # so keep it in stack to remain the priority
                        symbol_stack.put(stack_top)
                        symbol_stack.put(item)
                        
                    elif symbol_priority[stack_top] < symbol_priority[item]:
                        # if stack top priority is lower than current item
                        # push item to stack
                        symbol_stack.put(stack_top)
                        symbol_stack.put(item)

                    elif symbol_priority[stack_top] == symbol_priority[item]:
                        # if stack top priority equal to current item
                        # pop stack top push to queue, push current item to stack
                        processing_queue.put(stack_top)
                        symbol_stack.put(item)

                    else:
                        # if stack top priority is higher than current item
                        # pop stack top push to queue, push current item to stack
                        processing_queue.put(stack_top)
                        symbol_stack.put(item)

        else:
            if exception_flag:
                #raise Exception("Invalid equation: suffix, symbol issue, or parentheses are not paired")
                return "Invalid equation: suffix, symbol issue, or parentheses are not paired"

    # push remain symbols to queue, 
    # because itemlist is looped to end
    # if leave stack only,and itemlist is looped to end
    # push all stack to queue
    while not symbol_stack.empty():
        stack_top = symbol_stack.get()
        processing_queue.put(stack_top)

    # using stack to calculate is better /
    # for processing expression /
    # while finding operator,lhs and rhs
    calculate_stack = LifoQueue()

    while not processing_queue.empty():
        item = processing_queue.get()
        if IsNumber(item):
            calculate_stack.put(item)
        elif IsSymbol(item):
            RHS = calculate_stack.get()
            LHS = calculate_stack.get()
            if item == '+':
                result = float(LHS) + float(RHS)
            elif item == '-':
                result = float(LHS) - float(RHS)
            elif item == '*':
                result = float(LHS) * float(RHS)
            elif item == '/':
                if float(RHS) == 0:
                    #raise Exception("Divide by zero")
                    return "invalid input."
                result = float(LHS) / float(RHS)
            elif item == '%':
                if float(RHS) == 0:
                    #raise Exception("Divide by zero")
                    return "invalid input."
                result = float(LHS) % float(RHS)
            elif item == '^':
                result = float(LHS) ** float(RHS)
            else:
                raise Exception("Invalid equation: calculate issue, no such symbol")
            calculate_stack.put(result)

    result_num = calculate_stack.get()
    result_num = round(result_num, 2)
    return result_num


def find_solution(expression):
    expression_Items = parseExpression_Dijkstra(expression)
    if expression_Items is None:
        return "invalid input: without numbers and symbols"
    elif len(expression_Items) == 1:
        return float(expression_Items[0])
    result_num = solution(expression_Items)
    return result_num


if __name__ == '__main__':
    # below is for test code while running this file directly
    equation = "(7-5*9)/2"
    result_num = find_solution(equation)
    print(result_num)
