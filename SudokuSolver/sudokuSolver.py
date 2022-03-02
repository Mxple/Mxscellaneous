import numpy as np
import sys

# input
sudoku = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [0,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,0],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,0,1,9,0,0,5],
    [0,0,0,0,8,0,0,0,0]
]

sudoku = np.matrix(sudoku)

# functions
# n is potential input number, actual value on grid is 0
def possible(r,c,n):
    # check rows
    for j in range(9):
        if sudoku[r,j] == n:
            return False

    # check cols
    for i in range(9):
        if sudoku[i,c] == n:
            return False

    # check square
    for x in range(3):
        for y in range(3):
            if sudoku[3*(r//3)+x,3*(c//3)+y] == n:
                return False
    return n

def isValid(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i,j] != 0:
                temp = sudoku[i,j]
                sudoku[i,j] = 0
                if not possible(i,j,temp):
                    print("Not a valid puzzle")
                    return False
                sudoku[i,j] = temp
    print("Valid puzzle!\nNow solving...")
    return True

def solve():
    global sudoku
    for i in range(9):
        for j in range(9):
            if sudoku[i,j] == 0:
                for n in range(9,0,-1):
                    if possible(i,j,n):
                        #print(sudoku)
                        sudoku[i,j] = n
                        solve()
                sudoku[i,j] = 0
                return
    print(sudoku)
    inp = input("Find more solutions? ")
    if inp.lower() == "n":
        print("Done!")
        sys.exit()

# driver
print("Input:")
print(sudoku)


if isValid(sudoku):
    solve()
    print("All solutions found!")
