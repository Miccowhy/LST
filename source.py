import re

operations = {'N0': '1', 'N1': '0', 'A00': '0', 'A01': '1', 'A10': '1', 'A11': '1', 'K00': '0', 'K01': '0', 'K10': '0', 'K11': '0', 'C00': '1', 'C01': '1', 'C10': '0', 'C11': '1', 'E00': '1', 'E01': '0', 'E10': '0', 'E11': '1'}

regex = r"([AKCE][p][\d]*[p][\d]*|[N][p][\d]*)"
regex_forbidden = r"([p][0][\d]*|[BDF-JL-MO-Za-oq-z_]|[\W])"
regex_variables = r"([p][\d]*)"

def printer(truth_dict, var_list):
    truth_table = sorted(truth_dict, reverse=True)
    no_false = True

    output = "False for:\n"
    for x in var_list:
        output += x + ' '
    output += "\n"

    for var in truth_table:
        if truth_dict[var] == '0':
            no_false = False
            for x in range(len(var)):
                output += var[x] + ' ' * len(var_list[x])
            output += "\n"

    if no_false == False:
        print(output, end = '')
    else:
        print("No occurences where formula is false")

def solver(var_value, var_list, formula):
    for x in range(len(var_list)-1, -1, -1):
        formula = formula.replace(var_list[x], var_value[x])
    while len(formula) != 1:
        for op, val in operations.items():
            formula = formula.replace(op, val)
    return formula

def manipulator(formula):
    var_list = sorted(set(re.findall(regex_variables, formula)))
    var_amount = len(var_list)
    power = 2**var_amount
    truth_dict = dict()

    for x in range(power):
        var_value = bin(x)[2:].zfill(var_amount)
        truth_dict[var_value] = solver(var_value, var_list, formula)
    printer(truth_dict, var_list)

def syntax(formula):
    checker = formula

    validity = True
    i = 0

    forbidden = re.findall(regex_forbidden, checker)
    if forbidden == []:
        single_var = re.findall(regex_variables, formula)
        if formula == single_var[0]:
            print("False for:\n" + formula + "\n0")
        else:
            while checker != "p0":
                parser = re.findall(regex, checker)
                if parser == []:
                    print("Formula not valid")
                    validity = False
                    break

                for x in parser:
                    i = parser.index(x)
                    checker = checker.replace(x, "p0", 1)
                i += 1
            if validity == True:
                manipulator(formula)
    else:
        print("Non-valid characters used")

while True:
    formula = input()
    syntax(formula)
    print("-----------------------------------------")
