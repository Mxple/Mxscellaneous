import sys, os, copy, time, random

# global_list is all possible guesses
# answer_list is all possible solutions
mode = input("Are you playing Unlimited? ")
if mode[0].lower() == "y":
    answer_file = "all_words.txt"
    all_file = "all_words.txt"
else:
    answer_file = "answers.txt"
    all_file = "all_words.txt"

with open(os.path.join(sys.path[0], all_file),"r") as file:
    global_list = file.read().splitlines()
with open(os.path.join(sys.path[0], answer_file),"r") as file:
    answer_list = file.read().splitlines()

# best_guesses_list is precalculated best guesses for first solution
with open(os.path.join(sys.path[0], "best_words2.txt"),"r") as file:
    best_guesses_list = file.read().splitlines()
best_guesses = {}

for i in range(len(best_guesses_list)):
    key = best_guesses_list[i][:5]
    value = float(best_guesses_list[i][8:])
    best_guesses[key] = value
best_guesses = {k: v for k, v in sorted(best_guesses.items(), key = lambda x: x[1], reverse=True)}

# takes a word and outputs its point value, aka, how good of a guess it is
# point value calculated by determining the total number of words it can rule out over every combination of grey, yellow, green,
# then adjusting it based on probability of ruling out such a case 
# grey:0, yellow:1, green:2
def calculate_point_value(_word) -> int:
    total = len(answer_list)
    pts = 0
    for first in range(3):
        for second in range(3):
            for third in range(3):
                for fourth in range(3):
                    for fifth in range(3):
                        clue = str(first) + str(second) + str(third) + str(fourth) + str(fifth)
                        if is_valid(_word, clue):
                            temp = rule_outs(_word, clue) 
                            pts += (temp/total)*(total-temp)/total
    return pts
    
# returns the number of words ruled out given a word and a clue
def rule_outs(_word: str , _clue: str , alist = None) -> int:
    if alist is None:
        alist = copy.deepcopy(answer_list)
    original_len = len(alist)
    for i in range(5):
        if _clue[i] == "0":
            # soft parse for duplicates
            if _word[i] in _word[i:]:
                alist = [w for w in alist if _word[i] != w]
            # hard parse
            else:
                alist = [w for w in alist if _word[i] not in w]
        elif _clue[i] == "1":
            alist = [w for w in alist if _word[i] in w]
            alist = [w for w in alist if _word[i] != w[i]]
        else:
            alist = [w for w in alist if _word[i] == w[i]]
    return (original_len-len(alist))

# confirms whether a clue is valid
# a clue is valid if all recurring letters are lit if at least one is lit
def is_valid(_word: str , _clue: str) -> bool:
    yellows = [_word[i] for i in range(5) if _clue[i] == "1"]
    for i in range(5):
        if _word[i] in yellows and _clue[i] == "0":
            return False
    return True

# mutates the lists and computes the new best guesses
def compute_guess(_word: str , _clue: str):
    global global_list, answer_list, best_guesses
    # checks for right answer
    if _clue == "22222":
        print("Woohoo! We got it!")
        done()
        return

    # checks for number in word
    if len(_word) == 1 and _word.isnumeric():
        _word = list(best_guesses.keys())[int(_word)-1]

    # checks for invalid guesses
    if len(_word) != 5 or len(_clue) != 5:
        print("Invalid guess or clue, please re-enter.")
        return

    # first parse guesses and then solutions (simultaneously)
    flg  = False
    for i in range(5):
        if _clue[i] == "0":
            for j in range(5):
                if _clue[j] != "0" and _word[j] == _word[i]:
                    answer_list = [w for w in answer_list if _word[i] != w]
                    global_list = [w for w in global_list if _word[i] != w]
                    flg = True
                    break
            if flg:
                continue

            answer_list = [w for w in answer_list if _word[i] not in w]
            global_list = [w for w in global_list if _word[i] not in w]

        elif _clue[i] == "1":
            global_list = [w for w in global_list if _word[i] in w]
            global_list = [w for w in global_list if _word[i] != w[i]]
            answer_list = [w for w in answer_list if _word[i] in w]
            answer_list = [w for w in answer_list if _word[i] != w[i]]
        else:
            global_list = [w for w in global_list if _word[i] == w[i]]
            answer_list = [w for w in answer_list if _word[i] == w[i]]
    
    toProcess = len(global_list)
    print("Processing rating: "+str(toProcess*len(answer_list)))
    if input("Enter to process, any key to overide") != "":
        return
    if len(answer_list) < 15:
        global_list = answer_list
    # recalculate best guesses
    best_guesses = {}

    for word in range(len(global_list)):
        print(str(word)+"/"+str(toProcess))
        best_guesses.update({global_list[word]:calculate_point_value(global_list[word])})

    # sort best_guesses by values
    best_guesses = {k: v for k, v in sorted(best_guesses.items(), key = lambda x: x[1], reverse=True)}
    if len(best_guesses) > 1:
        print("I think these word(s) would be a good next guess...")
        print(list(best_guesses.keys())[:10])
    elif len(best_guesses) == 1:
        print("I've got the answer! It's "+list(best_guesses.keys())[0])
        done()
        return
    else:
        print("Uh oh, something went wrong...")
        sys.exit()

def done():
    global global_list, answer_list
    more = input("Wanna go again? ")
    if more[0].lower() == "y":
        with open(os.path.join(sys.path[0], all_file),"r") as file:
            global_list = file.read().splitlines()
        with open(os.path.join(sys.path[0], answer_file),"r") as file:
            answer_list = file.read().splitlines()
        return
    else:
        print("Cya next time!")
        sys.exit()
# progress = 0
# maxProgress = len(global_list)
# start = time.perf_counter()
# for word in global_list:
#     stop = time.perf_counter()
#     progress += 1
#     with open(os.path.join(sys.path[0], "best_words.txt"),"a") as file:
#         file.write(word+" : "+str(calculate_point_value(word))+"\n")
#     print(str(progress)+"/"+str(maxProgress)+"\tETA: "+str(round((stop-start)*(maxProgress/progress)-(stop-start)))+" s")

# aesthetics~ 
print("\n"+"-"*50)
print(" "*5+"Hi~ I'm RIN, I'm very good at wordle...")
print(" "*9+"But I can't play unfortunately-")
print(" "*5+"At least not without someone to help me")
print(" "*5+"That's where you come in, I think we'll")
print(" "*3+"make a great team! You play, I'll give tips!")
print("-"*50+"\n")

print("Maybe start out with ",end="")
print(list(best_guesses.keys())[:5])

while True:
    guess = input("Enter guess: ")
    clue = input("Enter clue: ")
    print("One sec...")
    compute_guess(guess,clue)
