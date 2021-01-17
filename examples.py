#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example sodoku puzzles to be tested

@author: fangfufu
"""
import time
import numpy
from sudoku import SudokuSolver

if __name__ == '__main__':
    #Step count: 43
    #Stack length: 44
    christmas_puzzle_1 = numpy.array([
            [3, 9, 0, 0, 7, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 3, 4, 7, 2],
            [0, 2, 7, 0, 0, 0, 6, 3, 0],
            [0, 0, 1, 0, 0, 9, 2, 0, 7],
            [0, 3, 0, 7, 0, 5, 0, 1, 0],
            [4, 0, 6, 8, 0, 0, 3, 0, 0],
            [0, 4, 8, 0, 0, 0, 7, 5, 0],
            [9, 5, 2, 3, 8, 0, 0, 0, 0],
            [7, 0, 0, 0, 5, 0, 0, 2, 8]
            ])
    #Step count: 43
    #Stack length: 44        
    christmas_puzzle_2 = numpy.array([
            [4, 0, 8, 6, 0, 0, 0, 5, 0],
            [0, 0, 0, 0, 0, 8, 1, 2, 3],
            [2, 3, 9, 0, 0, 1, 0, 0, 0],
            [6, 2, 0, 8 ,4, 5, 0, 0, 0],
            [1, 7, 0, 0, 0, 0, 0, 8, 5],
            [0, 0, 0, 1, 2, 7, 0, 3, 6],
            [0, 0, 0, 2, 0, 0, 5, 7, 9],
            [9, 8, 7, 5, 0, 0, 0, 0, 0],
            [0, 6, 0, 0, 0, 3, 8, 0, 4]
            ])
    
    # http://www.mathsphere.co.uk/downloads/sudoku/10202-medium.pdf
    medium_puzzle_1 = numpy.array([
            [6, 5, 9, 0, 1, 0, 2, 8, 0],
            [1, 0, 0, 0, 5, 0, 0, 3, 0], 
            [2, 0, 0, 8, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 3, 5, 0, 7, 0],
            [8, 0, 0, 9, 0, 0, 0, 0, 2],
            [0, 0, 3, 0, 7, 8, 6, 4, 0],
            [3, 0, 2, 0, 0, 9, 0, 0, 4],
            [0, 0, 0, 0, 0, 1, 8, 0, 0],
            [0 ,0, 8, 7, 6, 0, 0, 0, 0]
            ])
    
    medium_puzzle_10 = numpy.array([
            [0, 5, 7, 1, 0, 0, 0, 0, 8],
            [1, 8, 3, 0, 0, 0, 0, 9, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0],
            [8, 0, 2, 0, 3, 0, 0, 0, 0],
            [0, 7, 0, 0, 1, 0, 8, 0, 0],
            [5, 0, 0, 4, 8, 9, 0, 0, 0],
            [0, 4, 9, 0, 0, 0, 7 ,6, 0],
            [0, 6, 0, 0, 7, 0, 9, 0, 0],
            [7, 1, 5, 3, 9, 0, 0, 0, 0]
            ])
    
    # http://www.mathsphere.co.uk/downloads/sudoku/10203-hard.pdf
    
    # check_identical_config=True
    #Step count: 1140
    #Tried length: 483
    #Stack length: 56
    #process_time: 129.753542497
    hard_puzzle_1 = numpy.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 9, 4, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 5],
            [0, 9, 2, 3, 0, 5, 0, 7, 4], 
            [8, 4, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 7, 0, 9, 8, 0, 0, 0],
            [0, 0, 0, 7, 0, 6, 0, 0, 0],
            [0, 0, 0, 9, 0, 0, 0, 2, 0],
            [4, 0, 8, 5, 0, 0, 3, 6, 0]
            ])
    
    
    #check_identical_config=False 
    #Step count: 46068
    #Tried length: 0
    #Stack length: 51
    
    #check_identical_config=True     
    #Step count: 1149
    #Tried length: 489
    #Stack length: 51
    hard_puzzle_10 = numpy.array([
            [0, 0, 3, 0, 0, 7, 0, 6, 0],
            [0, 0, 7, 8, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1],
            [0, 0, 5, 4, 0, 8, 3, 7, 9],
            [0, 3, 0, 2, 7, 9, 6, 4, 0],
            [5, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 7, 6, 3, 9, 4, 0, 0, 0],
            [0, 0, 4, 0, 0, 5, 0, 8, 0]
            ])
    
    ## http://www.mathsphere.co.uk/downloads/sudoku/10204-fiendish.pdf
    fiendish_1 = numpy.array([
            [9, 5, 0, 0, 0, 1, 0, 0, 2],
            [6, 3, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 8, 0, 6, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 5, 0, 0],
            [0, 6, 1, 7, 0, 9, 0, 0, 0],
            [0, 0, 2, 0, 4, 0, 0, 0, 8],
            [0, 9, 0, 0, 0, 0, 0, 0, 5],
            [0, 1, 0, 0, 5, 6, 4, 8, 0],
            [0, 8, 0, 0, 1, 7, 0, 0, 6]
            ])
    
    fiendish_5 = numpy.array([
            [0, 0, 7, 3, 0, 0, 2, 0, 5],
            [0, 0, 4, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 6, 0],
            [4, 0, 0, 0, 0, 0, 0, 7, 8],
            [0, 1, 0, 5, 0, 0, 0, 0, 2],
            [0, 0, 8, 0, 0, 6, 1, 0, 0],
            [0, 2, 0, 0, 0, 1, 4, 0, 0],
            [0, 0, 0, 8, 0, 0, 0, 3, 7],
            [0 ,0, 0, 0, 0, 5, 0, 0, 0]
            ])
    
    solver = SudokuSolver(fiendish_5, check_identical_config=True)
    solver.solve()
    print(solver)
    print(time.process_time())
