import sys, os, copy, time, math
    
with open(os.path.join(sys.path[0], "all_words.txt"),"r") as file:
    global_list = file.read().splitlines()
with open(os.path.join(sys.path[0], "answers.txt"),"r") as file:
    answer_list = file.read().splitlines()

# takes a word and outputs its point value, aka, how good of a guess it is
# point value calculated by determining the total number of words it can rule out over every combination of grey, yellow, green,
# then adjusting it based on probability of ruling out such a case 
# grey:0, yellow:1, green:2
def calculate_point_value(_word) -> int:
    entropy = 0
    total = math.log(len(answer_list),2)
    for first in range(3):
        for second in range(3):
            for third in range(3):
                for fourth in range(3):
                    for fifth in range(3):
                        clue = str(first) + str(second) + str(third) + str(fourth) + str(fifth)
                        if is_valid(_word, clue):
                            temp = rule_outs(_word, clue)
                            entropy += temp * (total - temp)                            
                            print(clue+"\t"+str(temp))
    return entropy
    
# returns the entropy of a word-clue pair * probability of it occuring
def rule_outs(_word: str , _clue: str , alist = None) -> int:
    if alist is None:
        alist = copy.deepcopy(answer_list)
    original_len = len(alist)

    for i in range(5):
        if _clue[i] == "0": # grey
            # case: yellow dupe before curr
            for j in range(5):
                if _clue[j] != "0" and _word[j] == _word[i]:
                    alist = [w for w in alist if _word[i] != w]
                    if len(alist) == 0:
                        return 0

                    return (math.log((original_len/len(alist)),2))

            alist = [w for w in alist if _word[i] not in w]
        elif _clue[i] == "1": # yellow
            alist = [w for w in alist if _word[i] in w and _word[i] != w[i]]
        else: # green
            alist = [w for w in alist if _word[i] == w[i]]
    if len(alist) == 0:
        return 0

    return (math.log((original_len/len(alist)),2)) # bits

# confirms whether a clue is valid
# a clue is valid if all recurring letters are not yellow if the first is yellow
def is_valid(_word: str , _clue: str) -> bool:
    yellows = []
    for i in range(5):
        if _clue[i] == "0":
            yellows.append(_word[i])
            continue
        if _clue[i] == "1" and _word[i] in yellows:
            return False
    return True

# progress = 0
# maxProgress = len(global_list)
# start = time.perf_counter()
# for word in global_list:
#     stop = time.perf_counter()
#     progress += 1

#     with open(os.path.join(sys.path[0], "best_words3.txt"),"a") as file:
#         file.write(word+" : "+str(calculate_point_value(word))+"\n")

#     print(str(progress)+"/"+str(maxProgress)+"\tETA: "+str(round((stop-start)*(maxProgress/progress)-(stop-start)))+" s")
print(calculate_point_value("roost"))
