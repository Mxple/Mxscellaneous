# Mxscellaneous
Small projects that I've worked on including LeetCode, Daily Coding Problems, bots, simulations, etc

DCP:
- Daily Coding Problems, mostly algoritmic and data structure questions and solutions

N-body diagram Simulation:
- Simulates an N-body system using Newtonian laws of physics. The included save file is an example of a three body system (encoded in binary)
- Adjustable parameters are universal gravitational constant, G, number of bodies, N
- Press R to restart, A to add a few new bodies, S to save current system, UP/DOWN to zoom, LEFT/RIGHT to change perspective, LEFT BRACKET and RIGHT_BRACKET to change the tick speed
Known issues:
- Adding bodies (and occasionally, restarting) unbalances the system
- Energy is incorrectly calculated

Dependencies:
- random, pickle, copy, pygame

SudokuSolver
- Simple Sudoku solver using recursive backtracking
Known issues:
- Will fail to solve certain sudokus due to the nature of DFS

Dependencies:
- numpy

Wordle
- Wordle Solver using information bytes to maximize number of words eliminated by word given clues
- Differing word lists for Unlimited, normal, and a midway list
- Unlimited > Midway > Normal in length and processing time
- Has a precalculated list for first word
- Override calculation with any key
Known issues:
- Some words will fail due to errors in grey/yellow duplicates

Dependencies:
copy
