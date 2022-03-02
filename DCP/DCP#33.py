# Good morning! Here's your coding interview problem for today.
# This problem was asked by Microsoft.
# Compute the running median of a sequence of numbers. That is, given a stream of numbers, print out the median of the list so far on each new element.
# Recall that the median of an even-numbered list is the average of the two middle numbers.
# For example, given the sequence [2, 1, 5, 7, 2, 0, 5], your algorithm should print out:
# 2
# 1.5
# 2
# 3.5
# 2
# 2
# 2
def getMedian(array,l):
    if l%2 == 0:
        return array[l//2]
    return (array[l//2]+array[(l+1)//2])/2

def printRunningMedian(input: list[int]) -> None:
    print(getMedian(input, 0))
    for i in range(1,len(input)):
        currValue = input.pop(i)
        currIndex = i
        while currIndex>0 and currValue < input[currIndex-1]:
            currIndex -= 1
        input.insert(currIndex, currValue)
        print(getMedian(input,i))
    return(input)

#driver code
input = [2, 1, 5, 7, 2, 0, 5]
print(printRunningMedian(input))