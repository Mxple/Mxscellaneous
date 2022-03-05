# Mxscellaneous
Small projects that I've worked on including LeetCode, Daily Coding Problems, bots, simulations, etc

## DCP:
- Daily Coding Problems, mostly algoritmic and data structure questions and solutions

## N-body diagram Simulation:
- Simulates an N-body system using Newtonian laws of gravitation
- Press R to restart, A to add a few new bodies, S to save current system, UP/DOWN to zoom, LEFT/RIGHT to change perspective, =/- to change the speed
- Initialized to a simple model of the Solar System
- Time complexity of O(n)^2, Solar System model runs smoothly at 30 days/second (100 ticks per day) on Ryzen 5 3600x

Dependencies:
- random, pickle, pygame

## SudokuSolver
- Simple Sudoku solver using recursive backtracking
- 
Known issues:
- Will fail to solve certain sudokus due to the nature of DFS

Dependencies:
- numpy

## Wordle
- Wordle Solver using information bytes to maximize number of words eliminated by word given clues
- Differing word lists for Unlimited, normal, and a midway list
- Unlimited > Midway > Normal in length and processing time
- Has a precalculated list for first word
- Override calculation with any key
- 
Known issues:
- Some words will fail due to errors in grey/yellow duplicates

Dependencies:
copy
