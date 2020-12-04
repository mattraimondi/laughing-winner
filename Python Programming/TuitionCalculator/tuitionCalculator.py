# Matthew Raimondi
# Tuition Calculator
# 05 November 2020


# Import Statements
import sys
from datetime import date


# Program Data and Information (variable definitions (declaration and initialization))
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
inflationRates = [1.5, 3.0, 1.7, 1.5, 0.8, 0.7, 2.1, 2.1, 1.9, 2.3, 1.4]
averageInflation = sum(inflationRates) / len(inflationRates)
helpText = "Welcome to the college tuition calculator. The commands are as follows:\n\tfind - find tuition information about a college\n\tadd - add a new college to the database\n\tcolleges - list the available colleges\n\thelp - print out help to the screen\n\tquit - stop the program\n\nYou may use the quit command from within any part of the program in order to stop the program. When you issue a command, if you change your mind while answering questions, you may type \"back\""
fileName = "colleges.csv"


# Function Definitions
def write_history(input_stream):
    f = open("TCH", 'a')
    f.write(input_stream + "\n")
    f.close()


def ask_question(question_to_ask):
    q = input(question_to_ask + ": ")
    write_history(q)
    if "quit" in q.lower() or "exit" in q.lower():
        exit(0)
    elif "back" in q.lower():
        doer()
    return q


def beautify_money(incoming_number):
    money_array = []
    money_input = str(incoming_number)
    holder_array = money_input.split(".")

    if isinstance(incoming_number, int):
        money_string = ".00"
        for c in money_input:  # Make array from string
            money_array.append(c)
    else:
        money_string = ""
        money_array = holder_array[0]

    money_array_r = money_array[::-1]  # Reverse order of list/array

    k = 0  # Implement counter variable

    for n in money_array_r:

        if k % 3 == 0:  # Comma after after 3 digits
            if k == 0:  # Omit first time around
                money_string = n + money_string
            else:
                money_string = n + "," + money_string
            k += 1

        else:
            money_string = n + money_string
            k += 1

    money_string = "$" + money_string

    if isinstance(incoming_number, int):
        return money_string
    else:
        if holder_array[1] == "0":
            return money_string + '.' + holder_array[1] + "0"
        else:
            return money_string + '.' + holder_array[1]


def beautify_money_reverse(incoming_price):
    number_string_array = []
    for o in incoming_price:
        if o in numbers:
            number_string_array.append(o)

    return float(''.join(number_string_array))


def run_college_file_load(filename):
    f = open(filename, 'r')
    data_dump = f.readlines()
    f.close()
    return data_dump


def load_college_data(incoming_data):
    college_list = {}

    for line in incoming_data:
        line_split = line.split(',')
        new_key = line_split[0]
        new_val = eval(line_split[1])
        college_list.update({new_key: new_val})

    return college_list


def print_colleges(dictionary):
    print("We have information on the following colleges:")
    for key in dictionary:
        print(key + ": " + beautify_money(dictionary[key]))


def get_tuition(college_dict, what_college):
    for key in college_dict:
        if what_college.lower() == key.lower():
            return [key, college_dict[key]]
        elif what_college.lower() in key.lower():
            print("Could not find exact match. Searching for similar")
            return [key, college_dict[key]]


def total_cost(tuition):
    year1 = tuition
    year2 = year1 + (year1 * averageInflation)
    year3 = year2 + (year2 * averageInflation)
    year4 = year3 + (year3 * averageInflation)
    total_years = year1 + year2 + year3 + year4
    return year1, year2, year3, year4, total_years


def put_away_data(filename, college_data):
    f = open(filename, 'a')
    f.write(college_data + "\n")
    f.close()


def parse_input(input_stream):
    if "find" in input_stream.lower():
        # what_name = ask_question("What is your name?")
        # child_name = ask_question("What is your child's name?")

        while True:
            what_year = ask_question("Which year will your child enroll in college?")
            try:
                start_year = eval(what_year)
                this_year = date.today().year
                if start_year <= this_year:
                    print("Can't find tuition for past years")
                    continue
                else:
                    break
            except Exception as not_number:
                print(f"{not_number}\nSorry, {what_year} is not a valid number.")

        what_college = ask_question("Which college would you like information about?")

        try:
            tuition = get_tuition(load_college_data(run_college_file_load(fileName)), what_college)
            print(f"The tuition for {tuition[0]} is {beautify_money(tuition[1])}")
        except Exception as no_college:
            print(f"{no_college}\nSorry, we do not have information on {what_college}.")

    elif "add" in input_stream.lower():
        new_college = ask_question("What is the name of the college you would like to add?")
        new_cost = ask_question("What is their total cost per year?")
        new_data = (new_college + ',' + str(beautify_money_reverse(new_cost)) + ',')
        put_away_data(fileName, new_data)

    elif "help" in input_stream.lower():
        print(helpText)

    elif "colleges" in input_stream.lower():
        print_colleges(load_college_data(run_college_file_load(fileName)))

    elif "clear" in input_stream.lower():
        pass

    elif "quit" in input_stream.lower() or "exit" in input_stream.lower():
        exit(0)

    else:
        print("Not a valid command")


def main():
    print("Tuition Calculator> ", end="")
    stream = sys.stdin.readline().strip("\n")
    write_history(stream)
    parse_input(stream)


def doer():
    while True:
        main()


# Executed Code
print(helpText)
print_colleges(load_college_data(run_college_file_load(fileName)))
doer()
