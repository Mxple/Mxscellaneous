#Find the kth largest value in an array
#Assumptions: 
# array is made up of only integers 
# has at least 1 value
# k is in bounds
from timeit import default_timer as timer

#Algorithm
#uses quicksort algo combined with minimizing worst case through initial if statement
def findkthlargest(array: list[int], k: int) -> int:
    k = len(array) - k
    #"sort" the array only up until the kth value
    start = 0
    end = len(array)-1
    pIndex = k-1
    p = array[k-1]

    while start < end:
        while start < len(array) and array[start] <= p:
            start += 1
        while array[end] > p:
            end -= 1
        if start < end:
            array[start],array[end] = array[end],array[start]

    array[pIndex],array[end] = array[end],array[pIndex]

    #return the correct index
    return (array[k-1])

#Driver code
arr = [4, 7, 3, 8, 4, 5, 7, 2, 9, 4, 1, 5, 4, 8]
print(findkthlargest(arr, 3))