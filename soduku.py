import numpy
from numpy import array

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
        self.__puzzle_init = array(puzzle)
        if len(self.__puzzle_init.shape) != 2 or \
            self.__puzzle_init.shape[0] != 9 or \
            self.__puzzle_init.shape[1] != 9 :
                raise ValueError("Invalid input puzzle dimension")
        
        result = SodukuSolver.is_valid_puzzle(puzzle)
        if result == -1:
            raise ValueError("Invalid input puzzle")
        elif result == 0:
            raise ValueError("The input puzzle has already been solved.")
    
    @staticmethod
    def is_valid_puzzle(puzzle): 
        ''' 
        Check if a puzzle configuration is valid 
        
        Args:
            puzzle: The puzzle to be checked
        
        Returns:
            -1: invalid configuration
             0: valid configuration
             1: incomplete configuration
        '''
        assert(isinstance(puzzle, numpy.ndarray))
        total = 0
        for i in range(0,9):
            # scan for rows and columns
            result = SodukuSolver.is_valid_subunit(puzzle[i, :])
            if result > -1:
                total += result
            else:
                return -1

            # scan for columns
            result = SodukuSolver.is_valid_subunit(puzzle[:, i])
            if result > -1:
                total += result
            else: 
                return -1

        for i in range(0,3):
            for j in range(0,3):
                result = SodukuSolver.is_valid_subunit(
                        puzzle[3*i:(i+1)*3, 3*j:(j+1)*3])
                if result > -1:
                    total += result
                else:
                    return -1

        
        # clamp the return value to a maximum of 1
        if total > 1:
            return 1
        else:
            return 0
    
    @staticmethod  
    def is_valid_subunit(subunit):
        '''
        Check if a sub-unit has a valid configuration
        Returns:
            -1: invalid configuration
             0: valid configuration
             1: incomplete configuration
        '''
        assert(isinstance(puzzle, numpy.ndarray))
        
        subunit = subunit.flatten()
        if len(subunit) != 9:
            raise  ValueError("Invalid subunit dimension")
        
        # Note that we need to check for number 0-9, and there are 10 numbers!
        check = [0] * 10
        # Check if each number appear exactly once
        for i in subunit:
            check[i] += 1
            if check[i] > 1 and i != 0:
                return -1
        # Check how many 0s we have left. 
        if check[0] == 0:
            return 0
        else:
            return 1
        
if __name__ == '__main__':
    puzzle = array([[0, 0, 3, 0, 4, 2, 0, 9, 0],
                    [0, 9, 0, 0, 6, 0, 5, 0, 0],
                    [5, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 1, 7, 0, 0, 2, 8, 5],
                    [0, 0, 8, 0, 0, 0, 1, 0, 0],
                    [3, 2, 9, 0, 0, 8, 7, 0, 0],
                    [0, 3, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 5, 0, 9, 0, 0, 2, 0],
                    [0, 8, 0, 2, 1, 0, 6, 0, 0]])
    solver = SodukuSolver(puzzle)
