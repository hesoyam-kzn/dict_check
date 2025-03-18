from random import choice, randint, shuffle
import os
from os import path, remove


# ------------- program parameters ---------------#
# path to origin .csv with word-meaning pairs
doc_path = f"{os.getcwd()}\\test.csv"
# path to the .csv, which we'll fill with the pair of word-meaning + counter incrementation
guessed_path = ''
log_name = "logfile.txt"
# ------------- parameters end ---------------#

# reading rows from the passed .csv and saving them into the list of 2-element tuples
def read_raw_doc(d_path):
    lines = []
    lis = []
    with open(d_path, 'r', encoding='utf8') as file:
        for f in file:
            lines.append(f.rstrip("\n"))

    for line in lines:
        m, k = line.split(',')
        lis.append({"word": m, "tr": k})

    file.close()
    return lis


# Erasing existing progress data file (TODO: implement better, now is not working as expected)
def clear_progress(args):
    for i in range(len(args)):
        if args[i] == "-mode":
            if args[i+1].lower() == "c":
                if path.exists(log_name):
                    remove(log_name)
            else:
                print("Continuing with existing data about learning\n")


def log_file_work(guessed_pair, inventory):
    if guessed_pair in inventory.keys():
        inventory[guessed_pair] += 1
    else:
        inventory.setdefault(tmp_tup, 1)
    return inventory


def log_file_parse(file):
    words = {}
    f = open(file, "r", encoding="utf-8")
    for st in f:
        words.setdefault(tuple(st[:st.index(":")].split(",")),int(st[st.index(":")+1:].rstrip()))
    f.close()
    return words


def choose_four(seq):
    res = []
    while len(res) < 4:
        tmp_val = choice(seq)
        if tmp_val not in res:
            res.append(tmp_val)
    return res


# method shows you one a word and several options for answer, you need to choose a correct translation
def try_guess(c_set):
    word = c_set[randint(0, 3)]
    shuffle(c_set)
    print(f"Guess word {word['word'].upper()} \n")
    opts = []
    for i in range(len(c_set)):
        opts.append(f'{i + 1}. {c_set[i]["tr"]}')
    print(*opts, sep='\n')

    return word, opts



# Main block of the program #
pairs = read_raw_doc(doc_path)
guessed_per_session = dict()
sums = 0
logged = log_file_parse(log_name) if path.exists(log_name) else dict()

while sums < 15:
    cur_set = choose_four(pairs)
    w, op = try_guess(cur_set)
    correctly = False
    while not correctly:
        us_in = input(f'\nHow to translate? \n')
        tmp_tup = (w["word"], w["tr"])
        if len(us_in) > 0 and us_in.isdigit():
            variant = int(us_in)
            if us_in in '1234':
                a = w['tr']
                b = op[variant - 1][3:]
                if a == b:
                    print('\n\033[32mYou god damn right.\033[0m\n')
                    correctly = True
                    logged = log_file_work(tmp_tup, logged)
                    guessed_per_session[tmp_tup] = guessed_per_session.setdefault(tmp_tup, 0) + 1
                    sums += 1
                else:
                    print('\n\033[33mYou lost, filthy liar!\033[0m\n')
                    print(f'\033[34m{w["word"].capitalize()} - {a.capitalize()}\033[0m\n')
                    correctly = True
                    guessed_per_session[tmp_tup] = guessed_per_session.setdefault(tmp_tup, 0)
            else:
                print("\033[31mTry once more time, wrong character. Use 1-4 digits.\033[0m")
                continue
        else:
            print("\033[31mTry once more time, empty \\ wrong character. Use 1-4 digits.\033[0m")
            continue
else:
    print("\033[1m-------------------------------------------\033[0m")
    print("\033[1m--------\033[5m\033[33mSession finished for today\033[0m\033[0m---------\033[0m")
    print("\033[1m-------------------------------------------\033[0m")
    print("\033[1m\033[36mSummary:\033[0m\033[0m")
    for g, u in guessed_per_session.items():
        print(f'{g[0]} ({g[1]}) +{u}')

# Adding files to logfile.txt for measuring progress and filtering
with open(log_name, "w", encoding="utf-8") as final_log:
    for k,v in logged.items():
        final_log.write(f'{k[0]},{k[1]}:{v}\n')