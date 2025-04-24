from random import choice, randint, shuffle
import os, sys
from os import path, remove
from datetime import datetime, timedelta

# ------------- program parameters ---------------#
doc_path = f"{os.getcwd()}\\test.csv" # Path to origin .csv with word-meaning pairs
log_name = "logfile.txt" # Path to a log file, where current progress will be stored
max_repeats = 5 # Maximum times you need guess the word
# ------------- parameters end ---------------#

# reading rows from the passed .csv and saving them into the list of 2-element tuples
def read_raw_doc(d_path, length):
    lines = []
    lis = []
    with open(d_path, 'r', encoding='utf8') as file:
        for f in file:
            lines.append(f.rstrip("\n"))

    for line in lines:
        m, k = line.split(',')
        lis.append({"word": m, "tr": k})
    file.close()
    shuffle(lis)
    return lis[:length], tuple(lis)


def check_limit_reached(pair, logged_dic, repeats):
    if tuple([pair["word"], pair["tr"]]) in logged_dic.keys():
        if logged_dic[tuple([w["word"], w["tr"]])] == repeats:
            return True
        else:
            return False
    return False


#Most likely won't be used. Yet if someday you will repeat all words max_repeats times - this function will output congrats.
def check_all_words_learned(logged_dic, learning_pairs, repeats):
    if len(logged_dic) == len(learning_pairs):
        if all(map(lambda x: logged_dic[x] == repeats, logged_dic)):
            return True
        else:
            return False
    return False


# Adjusting working mode. Edit delta for decrease\increase of attempts\time per session
def check_mode():
    a = sys.argv
    if "--mode" in a:
        mode = a[a.index('--mode') + 1]
        if mode == "timer":
            start = datetime.now()
            delta = timedelta(minutes=5)
            end = start + delta
            print(f"Timer mode enabled, you have {delta.seconds // 60} minutes\n")
        elif mode == "counter":
            start, delta = 0, 5
            end = 5
            print(f"Counter mode enabled, you have {end} shots\n")
        else:
            start, end, delta, mode = 0, 10, 1, "counter"
            print(f"Default mode enabled, you have {end} shots\n")
        return start, end, delta, mode
    # If mode is not defined use default mode with "end" shots
    else:
        start, end, delta, mode = 0, 10, 1, "counter"
        print(f"Default mode enabled, you have {end} shots\n")
        return start, end, delta, mode



# Function for work with existing log values and further modification or addition of keys and values when word is guessed
def log_file_work(guessed_pair, inventory):
    if guessed_pair in inventory.keys():
        inventory[guessed_pair] += 1
    else:
        inventory.setdefault(tmp_tup, 1)
    return inventory


# Function for parsing an existing log file and converting it into a dictionary
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
    opts = []
    for i in range(len(c_set)):
        opts.append(f'{i + 1}. {c_set[i]["tr"]}')
    return word, opts


# Main block of the program #
pairs, all_pairs = read_raw_doc(doc_path, 20)
guessed_per_session = dict()
logged = log_file_parse(log_name) if path.exists(log_name) else dict()
# Defining how will we count progress (timer \ counter)
start, end, delta, mode = check_mode()

while start < end:
    if check_all_words_learned(logged, all_pairs, max_repeats):
        print("\n\033[97m\033[102mNo words for guessing anymore, you're such a cute learner! Go eat some buisquits.\033[0m\n")
        break
    cur_set = choose_four(pairs)
    w, op = try_guess(cur_set)
    if check_limit_reached(w, logged, max_repeats):
        continue
    print(f"Guess word {w['word'].upper()} \n")
    print(*op, sep='\n')

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
                    if mode == "counter":
                        start += 1
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
    if mode == "timer":
        start = datetime.now()
        if start < end:
            mins, secs = (end - start).seconds // 60, (end - start).seconds % 60
            print(f'\033[0;35m\033[3mMinutes left: {mins}:{secs if len(str(secs)) == 2 else f"0{secs}"}\033[0m\033[0m\n')
    
else:
    # Coloring ascii codes can be found on 
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