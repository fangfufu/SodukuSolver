#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example sodoku puzzles to be tested

@author: fangfufu
"""

if __name__ == '__main__':
    # http://www.theprintablesudokupuzzlesite.com/very-easy-sudoku/sudoku-a1-easycheesy.pdf
    easy_puzzle = numpy.array([
            [1, 6, 5, 7, 9, 4, 0, 3, 8],
            [4, 0, 7, 0, 0, 2, 0, 5, 0],
            [9, 3, 0, 0, 0, 6, 0, 0, 4],
            [8, 1, 0, 4, 0, 5, 0, 0, 2],
            [5, 7, 6, 2, 3, 9, 4, 0, 0],
            [2, 0, 0, 6, 0, 1, 0, 7, 5],
            [3, 0, 1, 5, 0, 7, 8, 4, 9],
            [6, 9, 0, 0, 0, 0, 5, 2, 7],
            [0, 5, 0, 0, 2, 8, 1, 0, 3]
            ])

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
    # https://www.7sudoku.com/view-puzzle?date=20201126
    very_difficult_puzzle = numpy.array([
            [0, 0, 0, 8, 0, 0, 0, 7, 0],
            [4, 0, 0, 0, 0, 9, 0, 0, 5],
            [0, 0, 0, 0, 3, 0, 0, 9, 0],
            [0, 5, 1, 0, 0, 0, 8, 0, 0],
            [0, 0, 7, 1, 6, 5, 2, 0, 0],
            [0 ,0, 2, 0, 0, 0, 5, 6, 0],
            [0, 6, 0, 0, 9, 0, 0, 0, 0],
            [1, 0, 0, 7, 0, 0, 0, 0, 8],
            [0, 9, 0, 0, 0, 2, 0, 0, 0]
            ])
    
    # http://www.mathsphere.co.uk/downloads/sudoku/10202-medium.pdf
    solver = SodokuSolver(christmas_puzzle_2)
    solver.solve()
    print(solver)