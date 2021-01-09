import numpy
import math

class SodukuSolver():
    '''
    SodukuSolver -- a soduku solver that uses numpy array

    Args:
        puzzle: the puzzle that needs to be solved
    '''

    def __init__(self, puzzle):
        ''' Constructor '''
        self.puzzle = puzzle

    @property
    def puzzle(self):
        ''' Return the initial puzzle '''
        return self.__puzzle_init

    @puzzle.setter
    def puzzle(self, puzzle):
        ''' Set the initial puzzle '''
        self.__puzzle_init = numpy.array(puzzle)
        if len(self.__puzzle_init.shape) != 2 or \
            self.__puzzle_init.shape[0] != 9 or \
            self.__puzzle_init.shape[1] != 9 :
                raise ValueError("Invalid input puzzle dimension")
        
        validity = self.is_valid_puzzle(puzzle)
        if validity == -1:
            raise ValueError("Invalid input puzzle")
        elif validity == 0:
            raise ValueError("The input puzzle has already been solved.")
    
    @staticmethod
    def is_valid_puzzle(puzzle): 
        ''' 
        Check if a puzzle configuration is valid 
        
        Args:
            puzzle: a 9x9 soduku configuration
        
        Returns:
            -1: invalid configuration
             0: complete and valid configuration
             positive int: incomplete configuration, the number of 0s remaining
                 in the puzzle
        '''
        assert(isinstance(puzzle, numpy.ndarray))
        assert(puzzle.shape == (9, 9))
        
        for i in range(0,9):
            # scan for rows and columns
            if SodukuSolver.is_valid_unit(puzzle[i, :]) < 0:
                return -1
            # scan for columns
            if SodukuSolver.is_valid_unit(puzzle[:, i]) < 0:
                return -1

        total = 0
        for i in range(0,3):
            for j in range(0,3):
                result = SodukuSolver.is_valid_unit(
                        puzzle[3*i:3*(i+1), 3*j:3*(j+1)])
                if result < 0:
                    return -1
                else:
                    total += result
        
        return result
    
    @staticmethod  
    def is_valid_unit(unit):
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
        assert(isinstance(puzzle, numpy.ndarray))
        assert(len(unit.flatten()) == 9)
        
        unit = unit.flatten()
        if len(unit) != 9:
            raise  ValueError("Invalid subunit dimension")
        
        # Note that we need to check for number 0-9, and there are 10 numbers!
        check = [0] * 10
        # Check if each number appear exactly once
        for i in unit:
            check[i] += 1
            if check[i] > 1 and i != 0:
                return -1
        # return how many 0s are left. 
        return check[0]
        
    @staticmethod
    def gen_valid_choices(puzzle):
        '''
        Output the valid choices each square can take, for the whole puzzle
        
        Args:
            puzzle: a 9x9 soduku configuration
            
        Returns:
            A 9x9x9 boolean numpy array indicating the valid choices
        '''
        assert(isinstance(puzzle, numpy.ndarray))
        assert(puzzle.shape == (9, 9))

        # Initially every number is possible in every square, as we discover
        # existing numbers, they get masked out. 
        # We use the value in the puzzle to do indexing directly, 
        row_arr = numpy.full((9, 9), True)
        col_arr = numpy.full((9, 9), True)
        square_arr = numpy.full((3, 3, 9), True)
        for i in range(0,9):
            for j in range(0,9):
                # Skip the 0s
                if puzzle[i,j] > 1:
                    num = puzzle[i,j] - 1
                    row_arr[i, num] = False
                    col_arr[j,num] = False
                    square_arr[math.floor(i/3), math.floor(j/3), num] = False
                    
        # Calculate the valid choices
        valid_choices = numpy.full((9, 9, 9), True)
        for i in range(0,9):
            for j in range(0,9):
                valid_choices[i,j] = row_arr[i] & col_arr[j] & \
                square_arr[math.floor(i/3), math.floor(j/3)]
        
        return valid_choices
    
    @staticmethod
    def gen_priority_list(valid_choices):
        '''
        Generate a priority list from a valid choices array
        
        Args: 
            valid_choices: a 9x9x9 boolean array indicating the valid choices
        
        Returns:
            priority list - a sorted list of tuples (row, col, num), indicating
            which squares should be filled first.
        '''
        
        assert(isinstance(valid_choices, numpy.ndarray))
        assert(valid_choices.shape == (9, 9 ,9))
        
        priority2d = numpy.sum(valid_choices, 2)
        prioritytbl = [(0, 0, 0)] * 81
        for i in range(0, 9):
            for j in range(0, 9):
                prioritytbl[i*9+j] = (i, j, priority2d[i, j])

        return [(x[0], x[1]) for x in sorted(prioritytbl, key=lambda x: x[2])]

    @staticmethod
    def gen_choice(valid_choices, priority_list, n):
        '''
        Generate the nth choice from a priority list and valid choices pair
        
        Args: 
            valid_choices: a 9x9x9 boolean numpy array indicating the valid 
            choices (generated from gen_valid_choices())
            priority_list: a sorted list of tuples (row, col, num), indicating
            which squares should be filled first. (generated from 
            gen_priority_list())
            n: the choice to output at the current configuration
            
        Returns:
            The nth choice at the current configuration in the format of 
            (row, col, num), so square at (row, col) needs to be filled with 
            num
        '''
        assert(isinstance(priority_list, list))
        assert(len(priority_list) == 81)
        assert(isinstance(valid_choices, numpy.ndarray))
        assert(valid_choices.shape == (9, 9 ,9))
        
        k = 0
        for coord in priority_list:
            for i, choice in enumerate(valid_choices[coord]):
                if choice:
                    if k == n:
                        return (coord[0], coord[1], i + 1)
                    else:
                        k += 1
                    
        raise OverflowError("The choice you specified is beyond all possible \
choices in the current configuration.")
        
    @staticmethod
    def gen_config(current_config, valid_choices, priority_list, n):
        '''
        Generate the nth next configuration from the current configuration
        
        Args:
            current_config: the current puzzle configuration
            valid_choices: a 9x9x9 boolean numpy array indicating the valid 
            choices (generated from gen_valid_choices()).
            priority_list: a sorted list of tuples (row, col, num), indicating
            which squares should be filled first. (generated from 
            gen_priority_list()).
            n: the nth next configuration to generate.
        '''
        assert(isinstance(priority_list, list))
        assert(len(priority_list) == 81)
        assert(isinstance(valid_choices, numpy.ndarray))
        assert(valid_choices.shape == (9, 9 ,9))
        assert(SodukuSolver.is_valid_puzzle(current_config) > 0)
        choice = SodukuSolver.gen_choice(valid_choices, priority_list,n)
        new_config = numpy.copy(current_config)
        new_config[choice[0], choice[1]] = choice[2]
        return new_config
    
if __name__ == '__main__':
    current_config = numpy.array([[0, 0, 3, 0, 4, 2, 0, 9, 0],
                    [0, 9, 0, 0, 6, 0, 5, 0, 0],
                    [5, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 1, 7, 0, 0, 2, 8, 5],
                    [0, 0, 8, 0, 0, 0, 1, 0, 0],
                    [3, 2, 9, 0, 0, 8, 7, 0, 0],
                    [0, 3, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 5, 0, 9, 0, 0, 2, 0],
                    [0, 8, 0, 2, 1, 0, 6, 0, 0]])
    solver = SodukuSolver(current_config)
    valid_choices = solver.gen_valid_choices(current_config)
    priority_list = solver.gen_priority_list(valid_choices)
    print(current_config)
    print(solver.gen_choice(valid_choices, priority_list, 0))
    print(solver.gen_config(current_config, valid_choices, priority_list, 0))
    print(solver.gen_choice(valid_choices, priority_list, 1))
    print(solver.gen_config(current_config, valid_choices, priority_list, 1))
    print(solver.gen_choice(valid_choices, priority_list, 2))
    print(solver.gen_config(current_config, valid_choices, priority_list, 2))



