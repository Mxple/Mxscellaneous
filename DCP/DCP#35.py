# Given an array of strictly the characters 'R', 'G', and 'B', segregate the values of the array so that all the Rs come first, the Gs come second, and the Bs come last. You can only swap elements of the array.
# Do this in linear time and in-place.
# For example, given the array ['G', 'B', 'R', 'R', 'B', 'R', 'G'], it should become ['R', 'R', 'R', 'G', 'G', 'B', 'B'].
def sortRGB(input: list[str]) -> list[str]:
    R_insert = 0
    B_insert = len(input)-1
    for index,letter in enumerate(input):
        if letter=="R":
            input[R_insert], input[index] = input[index], input[R_insert]
            R_insert += 1
    for i in range(len(input)-1,0,-1):
        if input[i]=="B":
            input[B_insert], input[i] = input[i], input[B_insert]
            B_insert -= 1
    return input


#driver code
input = ["R","G","B","B","B","R","G","R","G","G","G","B","R"]
print(sortRGB(input))