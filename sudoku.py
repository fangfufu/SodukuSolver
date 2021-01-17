#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sudoku solver using depth first search
@author: fangfufu
"""

import numpy
import math
import sys

class OutOfdecision(Exception):
    ''' For use by SudokuConfig, when running out of decisions'''
    pass

class InvalidConfiguration(ValueError):
    ''' For use by SudokuConfig, when the sudoku configuration is valid '''
    def __init__(self, val):
        message = "Invalid sudoku configuration."
        super().__init__(message, str(val))

class SudokuConfig():
    '''
    SudokuConfig -- Container for the state information for a sudoku 
    configuration
    
    Args:
        config: The configuration to generate the state information for.
        
    Attributes:
        valid_decisions: a 9x9x9 boolean numpy array indicating the valid decisions
            for each square
        priority list: a list of tuples (row, col), indicating which squares 
            should be filled first.
        current_level: the square that needs to be tried, counting from the 
            top of the priority list
    '''
    
    def __init__(self, config):
        if config.shape != (9, 9):
                raise ValueError("Invalid input configuration dimension")
        self.config = config.copy()
        self.valid_decisions = self.__gen_valid_decisions_array()
        self.priority_list = self.__gen_priority_list()
        self.current_level = 0
        self.current_decision = 0
        self.decision_cache = []
        
    def __eq__(self, other):
        return numpy.array_equal(self.config, other.config)
    
    def __ne__(self, other):
        return not numpy.array_equal(self.config, other.config)
    
    def __next__(self):
        '''Make the class iterable'''
        try:
            return self.gen_config(len(self.decision_cache))
        except OutOfdecision:
            raise StopIteration
            
    def __repr__(self):
        return (self.config.__repr__())
    
    def __str__(self):
        return (self.config.__str__()).replace("0", "_")
    
    @staticmethod
    def __is_valid_unit(unit):
        '''
        Check if a unit has a valid configuration
        
        Args:
            unit: a unit of 9 squares
        Returns:
            -1: invalid configuration
             0: complete and valid configuration
             positive int: incomplete configuration, the number of 0s remaining
                 in the unit
        '''
        unit = unit.flatten()
        assert(len(unit) == 9)
        
        # Note that we need to check for number 0-9, and there are 10 numbers!
        check = [0] * 10
        # Check if each number appear exactly once
        for i in unit:
            check[i] += 1
            if check[i] > 1 and i != 0:
                raise InvalidConfiguration(unit)
        # return how many 0s are left. 
        return check[0]

    def is_valid(self): 
        ''' 
        Check if a sudoku configuration is valid 
        
        Returns:
             0: complete and valid configuration
             positive int: incomplete configuration, the number of 0s remaining
                 in the puzzle
        '''
        for i in range(0,9):
            # scan for rows and columns
            self.__is_valid_unit(self.config[i, :]) < 0
            self.__is_valid_unit(self.config[:, i]) < 0
    
        total = 0
        for i in range(0,3):
            for j in range(0,3):
                total += self.__is_valid_unit(
                        self.config[3*i:3*(i+1), 3*j:3*(j+1)])
        
        return total
        
    def __gen_valid_decisions_array(self):
        ''' Generate the valid decisions array '''
        # Initially every number is possible in every square, as we discover
        # existing numbers, they get masked out. 
        # We use the value in the puzzle to do indexing directly, 
        row_arr = numpy.full((9, 9), True)
        col_arr = numpy.full((9, 9), True)
        square_arr = numpy.full((3, 3, 9), True)
        for i in range(0,9):
            for j in range(0,9):
                # Skip the 0s
                if self.config[i,j] > 0:
                    num = self.config[i,j] - 1
                    row_arr[i, num] = False
                    col_arr[j, num] = False
                    square_arr[math.floor(i/3), math.floor(j/3), num] = False
                    
        # Calculate the valid decisions
        valid_decisions = numpy.full((9, 9, 9), True)
        for i in range(0,9):
            for j in range(0,9):
                valid_decisions[i,j] = row_arr[i] & col_arr[j] & \
                square_arr[math.floor(i/3), math.floor(j/3)]
        return valid_decisions
                
    def __gen_priority_list(self):
        ''' Generate the priority list for a sudoku configuration '''
        self.priority2d = numpy.sum(self.valid_decisions, 2)
        prioritytbl = []
        for i in range(0, 9):
            for j in range(0, 9):
                if self.config[i,j] == 0:
                    prioritytbl.append((i, j, self.priority2d[i, j]))
        return [(x[0], x[1]) for x in sorted(prioritytbl, key=lambda x: x[2]) 
                              if x[2] != 0]
    
    def __gen_decision(self, n):
        '''
        Generate the nth decision from a priority list and valid decisions pair
        
        Args: 
            n: the nth decision to generate
            
        Returns:
            The nth decision at the current configuration in the format of 
            (row, col, num), so square at (row, col) needs to be filled with 
            num. (0, 0, 0) will be returned if a decision cannot be generated.
        '''
        
        # We have cached the previous decisions for backtracking
        if n < len(self.decision_cache):
            return self.decision_cache[n]
        
        # Generate new decisions
        for i in range(self.current_level, len(self.priority_list)):
            self.current_level = i
            coord = self.priority_list[i]
            decisions = self.valid_decisions[coord]
            for j in range(self.current_decision, len(decisions)):
                self.current_decision = j
                if decisions[j]:
                    self.decision_cache.append((coord[0], coord[1], j + 1))
                    if n == (len(self.decision_cache) - 1):
                        # Manually increase the loop counter by 1, because we
                        # are exiting
                        self.current_decision += 1
                        return self.decision_cache[-1]       
                
        # We have reached the end without getting a solution 
        return (0, 0, 0)
    
    def gen_config(self, n):
        '''
        Generate a new sudoku configuration based on the nth decision
        
        Args:
            n: the nth new configuration to generate
            
        Returns:
            The nth new sudoku configuration
        '''
        decision = self.__gen_decision(n)
        if decision == (0, 0, 0):
            raise OutOfdecision();
        new_config = numpy.copy(self.config)
        new_config[decision[0], decision[1]] = decision[2]
        return SudokuConfig(new_config)
        
    
class SudokuSolver():
    '''
    SudokuSolver -- a sudoku solver that uses numpy array

    Args:
        input_array: the puzzle that needs to be solved
        limit: the maximun number of step to attempt before terminating
        check_identical_config: check whether the newly generated configuration
            is identical to a previously generated configuration. 
        
    Attributes:
        config_stack: the sudoku configuration stack
        tried_config: the sudoku configuration we have tried
        solution: the sudoku solution
        self.limit: the maximum step count before aborting
        n: the number of steps taken
    '''

    def __init__(self, 
                 input_array, 
                 limit=sys.maxsize, 
                 check_identical_config=True):
        ''' Constructor '''
        self.config_init = SudokuConfig(input_array)
        validity = self.config_init.is_valid()
        if validity == 0:
            raise ValueError("The input puzzle has already been solved.")
        
        # The configurations we have tried
        self.config_stack = [self.config_init]
        self.tried_config = []
        self.solution = None
        self.limit = limit
        self.step = 0
        self.check_identical_config = check_identical_config
    
    def __repr__(self):
        return "<SudokuSolver: len:" + str(self.__len__()) + ">"
    
    def __str__(self):
        return "--- SudokuSolver --- \n" + \
            "Step count: " + str( self.step) + "\n" + \
            "Tried length: " + str(self.tried_config.__len__()) + "\n" + \
            "Stack length: " + str(self.config_stack.__len__()) + "\n" + \
            self.config_stack[-1].__str__() + "\n"
    
    def __getitem__(self, i):
        return self.config_stack[i]
    
    def solve(self):
        '''
        Solve a sudoku puzzle using depth-first search with backtracking
        '''
        # While we still have squares to fill, try and fill the squares
        while self.config_stack[-1].is_valid() > 0 and  self.step < self.limit:
            if not ( self.step % 10000):
                print(self)
            try:
                self.step += 1
                next_config = next(self.config_stack[-1])
                if not self.check_identical_config:
                    self.config_stack.append(next_config)
                else:
                    if self.config_already_exists(next_config):
                        continue
                    else:
                        self.tried_config.append(next_config)
                        self.config_stack.append(next_config)
                    
            except StopIteration:
                self.config_stack.pop()

        self.solution = self.config_stack[-1]
        return self.solution

    def config_already_exists(self, this_config):
        for i in range(-1, -len(self.tried_config)-1, -1):
            if this_config == self.tried_config[i]:
                return True
                        
