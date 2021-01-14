import numpy
import math

class OutOfChoice(Exception):
    ''' For use by SodukuConfig, when running out of choices'''
    pass

class InvalidConfiguration(ValueError):
    ''' For use when SodukuConfig is valid '''
    def __init__(self, val):
        message = "Invalid soduku configuration."
        super().__init__(message, str(val))

class SodukuConfig():
    '''
    SodukuConfig -- Container for the state information for a soduku 
    configuration
    
    Args:
        config: The configuration to generate the state information for.
        
    Attributes:
        valid_choices: a 9x9x9 boolean numpy array indicating the valid choices
            for each square
        priority list: a list of tuples (row, col), indicating which squares 
            should be filled first.
    '''
    
    def __init__(self, config):
        config = numpy.array(config)
        if config.shape != (9, 9):
                raise ValueError("Invalid input configuration dimension")
        self.config = config.copy()
        self.__gen_valid_choices()
        self.__gen_priority_list()
        self.current_square = 0
        self.current_num = 0
        self.choice_list = []
    
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
        Check if a soduku configuration is valid 
        
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
        
    def __gen_valid_choices(self):
        ''' Generate the valid choices array '''
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
                    
        # Calculate the valid choices
        self.valid_choices = numpy.full((9, 9, 9), True)
        for i in range(0,9):
            for j in range(0,9):
                self.valid_choices[i,j] = row_arr[i] & col_arr[j] & \
                square_arr[math.floor(i/3), math.floor(j/3)]
                
    def __gen_priority_list(self):
        ''' Generate the priority list for a soduku configuration '''
        self.priority2d = numpy.sum(self.valid_choices, 2)
        prioritytbl = []
        for i in range(0, 9):
            for j in range(0, 9):
                if self.config[i,j] == 0:
                    prioritytbl.append((i, j, self.priority2d[i, j]))
        self.priority_list = [(x[0], x[1]) for x in 
                              sorted(prioritytbl, key=lambda x: x[2]) 
                              if x[2] != 0]
    
    def gen_choice(self, n):
        '''
        Generate the nth choice from a priority list and valid choices pair
        
        Args: 
            n: the nth choice to generate
            
        Returns:
            The nth choice at the current configuration in the format of 
            (row, col, num), so square at (row, col) needs to be filled with 
            num. (0, 0, 0) will be returned if a choice cannot be generated.
        '''
        
        # We have cached the previous choice
        if n < len(self.choice_list):
            return self.choice_list[n]
        
        # Generate new choices
        for i in range(self.current_square, len(self.priority_list)):
            self.current_square = i
            coord = self.priority_list[i]
            choices = self.valid_choices[coord]
            for j in range(self.current_num, len(choices)):
                self.current_num = j
                if choices[j]:
                    self.choice_list.append((coord[0], coord[1], j + 1))
                    if n == (len(self.choice_list) - 1):
                        # Manually increase the loop counter by 1, because we
                        # are exiting
                        self.current_num += 1
                        return self.choice_list[-1]       
                
        # We have reached the end without getting a solution 
        return (0, 0, 0)
    
    def gen_config(self, n):
        '''
        Generate a new soduku configuration based on the nth choice
        
        Args:
            n: the nth new configuration to generate
            
        Returns:
            The nth new soduku configuration
        '''
        choice = self.gen_choice(n)
        if choice == (0, 0, 0):
            raise OutOfChoice();
        new_config = numpy.copy(self.config)
        new_config[choice[0], choice[1]] = choice[2]
        return SodukuConfig(new_config)
    
    def __next__(self):
        '''Make the class iterable'''
        try:
            return self.gen_config(len(self.choice_list))
        except OutOfChoice:
            raise StopIteration
            
    def __repr__(self):
        return (self.config.__repr__())
    
    def __str__(self):
        return (self.config.__str__())
        
    
class SodukuSolver():
    '''
    SodukuSolver -- a soduku solver that uses numpy array

    Args:
        puzzle: the puzzle that needs to be solved
    '''

    def __init__(self, input_array):
        ''' Constructor '''
        self.config_init = SodukuConfig(input_array)
        validity = self.config_init.is_valid()
        if validity == 0:
            raise ValueError("The input puzzle has already been solved.")
        
        # The configurations we have tried
        self.configs = [self.config_init]
        self.solution = None
        self.n = 0
    
    def solve(self):
        '''
        Solve a Soduku puzzle using depth-first search with backtracking
        '''

        # While we still have squares to fill, try to fill the squares
        while self.configs[-1].is_valid() > 0 and self.n < 100:
            try:
                self.configs.append(next(self.configs[-1]))
            except StopIteration:
                self.configs.pop()
                next(self.configs[-1])
            self.n += 1
        self.solution = self.configs[-1]
        return self.solution

    def __len__(self):
        return self.configs.__len__()
    
    def __repr__(self):
        return "<SodokuSolver: " + str(self.__len__()) + ">"
    
    def __str__(self):
        return "SodukuSolver: " + str(self.__len__()) + "\n" + self.configs[-1].__str__()
    
    def __getitem__(self, i):
        return self.configs[i]
    
if __name__ == '__main__':
    current_config = numpy.array(
                    [[0, 0, 3, 0, 4, 2, 0, 9, 0],
                    [0, 9, 0, 0, 6, 0, 5, 0, 0],
                    [5, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 1, 7, 0, 0, 2, 8, 5],
                    [0, 0, 8, 0, 0, 0, 1, 0, 0],
                    [3, 2, 9, 0, 0, 8, 7, 0, 0],
                    [0, 3, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 5, 0, 9, 0, 0, 2, 0],
                    [0, 8, 0, 2, 1, 0, 6, 0, 0]])
#    state = SodukuConfig(current_config)
#    print(next(state))
#    print(next(state))
#    print(next(state))
#    print(state.choice_list)
#    print(state.gen_choice(0))
#    print(state.gen_choice(1))
#    print(state.gen_choice(2))
#    print(state)

    solver = SodukuSolver(current_config)
    print(solver.config_init)
    print(solver.solve())


