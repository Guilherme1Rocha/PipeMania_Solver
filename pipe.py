from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
pieces_board = {'F': ['FE','FB','FC','FD'], 'V': ['VE','VC','VB','VD'], 'B': ['BE','BD','BC','BB'], 'L': ['LV','LH']}
possibilities = {}
class PipeManiaState:
    state_id = 0
    last_moved_piece = () 
    def __init__(self, pieces, board_size, next_piece):
        self.pieces = pieces
        self.board_size = board_size
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.next_piece = next_piece

    def __lt__(self, other):
        return self.id < other.id
    
    def copy_pieces_board(self) -> tuple:
        pieces_copy = {}
        for key,piece in self.pieces.items():
            pieces_copy[key] = [piece[0],piece[1],False]
        return pieces_copy
    
    def get_next_move_piece(self) -> tuple: return self.next_piece

    def get_board_pieces(self) -> dict: return self.pieces

    def get_board_size(self) -> int: return self.board_size
    
class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, pieces, board_size):
        self.pieces = pieces
        self.board_size = board_size

    def get_pieces(self) -> dict: return self.pieces

    def get_board_size(self) -> int: return self.board_size

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.pieces[(row,col)][0]
        
    def set_value(self, row: int , col:int , value:str):
        """Atualiza o valor na respetiva posição do tabuleiro"""
        self.pieces[(row,col)][0] = value

    def get_Piece(self, row:int , col:int) -> list:
        return self.pieces[(row,col)]
    
    def add_Piece(self, row, col, piece):
        self.pieces[(row,col)] = piece

    def lock(self, row, col):
        self.pieces[(row,col)][1] = True
    
    def is_locked(self, row, col):
        return self.pieces[(row,col)][1]
    
    def visited(self, row, col):
        self.pieces[(row,col)][2] = True
    
    def is_visited(self, row, col):
        return self.pieces[(row,col)][2]

    def adjacent_pieces(self, row , col, ) -> (tuple, tuple,tuple,tuple):
        """Devolve os valores imediatamente acima e abaixo,
        respetivamente."""
        return (
            (row-1, col) if row > 0 else None , 
            (row+1,col) if row < (self.get_board_size()) - 1 else None, 
            (row, col-1) if col > 0 else None , 
            (row,col+1) if col < self.board_size - 1 else None
        )
    
    def get_next_piece(self, row, col) -> tuple:
        if row > self.board_size-1:
            return self.board-1,self.board_size-1
        if col < self.board_size-1: next_row, next_col = row,col+1
        else: next_row, next_col = row+1,0
        if row > self.board_size-1:
            next_row, next_col = self.board-1,self.board_size-1
        while (self.is_locked(next_row,next_col)):
            if next_col < self.board_size-1: 
                next_row, next_col = next_row,next_col+1
            else: next_row, next_col = next_row+1, 0
            if next_row > self.board_size-1:
                return self.board_size-1,self.board_size-1
        return next_row,next_col

    def are_connected(self, row1, col1, row2, col2, piece_value) -> bool:
        if row2 > row1: return piece_value in {'FC','BC','BE','BD','VC','VD','LV'} #peças com ligação cima
        if row2 < row1: return piece_value in {'FB','BB','BE','BD','VB','VE','LV'} #peças com ligação baixo
        if col2 > col1: return piece_value in ['FE','BC','BB','BE','VC','VE','LH'] #peças com ligação esquerda
        if col2 < col1: return piece_value in ['FD','BC','BB','BD','VB','VD','LH'] #peças com ligação direita

    def are_connected_full(self, row1, col1, piece_value1, row2, col2, piece_value2) -> bool:
        if row2 > row1: return piece_value1 in {'FB','BB','BE','BD','VB','VE','LV'} and piece_value2 in {'FC','BC','BE','BD','VC','VD','LV'}
        if row2 < row1: return piece_value1 in {'FC','BC','BE','BD','VC','VD','LV'} and piece_value2 in {'FB','BB','BE','BD','VB','VE','LV'} #peças com ligação baixo
        if col2 > col1: return piece_value1 in {'FD','BC','BB','BD','VB','VD','LH'} and piece_value2 in {'FE','BC','BB','BE','VC','VE','LH'} #peças com ligação esquerda
        if col2 < col1: return piece_value1 in {'FE','BC','BB','BE','VC','VE','LH'} and piece_value2 in {'FD','BC','BB','BD','VB','VD','LH'} #peças com ligação direita
    
    def is_connection(self, row1, col1, row2, col2):
        return (row2,col2) in self.get_neighbours(row1,col1)
    
    def get_neighbours(self, row, col) -> list:
        neighbours = []
        piece_value = self.get_value(row,col)
        if piece_value[0] == 'F':
            if piece_value[1] == 'C':
                neighbours.append((row-1,col))
            if piece_value[1] == 'B':
                neighbours.append((row+1,col))
            if piece_value[1] == 'E':
                neighbours.append((row,col-1))
            if piece_value[1] == 'D':
                neighbours.append((row,col+1))
        if piece_value[0] == 'B':
            if piece_value[1] == 'C':
                neighbours.append((row,col-1))
                neighbours.append((row-1,col))
                neighbours.append((row,col+1))
            if piece_value[1] == 'B':
                neighbours.append((row,col-1))
                neighbours.append((row+1,col))
                neighbours.append((row,col+1))
            if piece_value[1] == 'E':
                neighbours .append((row,col-1))
                neighbours .append((row+1,col))
                neighbours .append((row-1,col))
            if piece_value[1] == 'D':
                neighbours .append ((row-1,col))
                neighbours .append ((row,col+1))
                neighbours .append ((row+1,col))
        if piece_value[0] == 'V':
            if piece_value[1] == 'C':
                neighbours .append ((row-1,col))
                neighbours .append ((row,col-1))
            if piece_value[1] == 'B':
                neighbours .append ((row+1,col))
                neighbours .append ((row,col+1))
            if piece_value[1] == 'E':
                neighbours .append ((row+1,col))
                neighbours .append ((row,col-1))
            if piece_value[1] == 'D':
                neighbours .append ((row-1,col))
                neighbours .append ((row,col+1))
        if piece_value[0] == 'L':
            if piece_value[1] == 'H':
                neighbours .append ((row,col-1))
                neighbours .append ((row,col+1))
            if piece_value[1] == 'V':
                neighbours .append ((row-1,col))
                neighbours .append ((row+1,col))
        return neighbours

    def in_corner(self, row, col) -> bool: return ((row == 0 or row == self.board_size-1) and (col == 0 or col == self.board_size-1))

    def in_border(self, row ,col) -> bool: return (row == 0 or row == self.board_size-1 or col == 0 or col == self.board_size-1)

    def add_possibility(self, possibilities, new_possibility):
        possibilities.append(new_possibility)
        return possibilities
    
    def remove_possibility(self, possibilities_total, possibilities_remove) -> list:
        for possiblity in possibilities_remove:
            if possiblity in possibilities_total: possibilities_total.remove(possiblity)
        return possibilities_total
    
    def possibilities_no_constraints(self, piece_value) -> list:
        return [piece for piece in pieces_board[piece_value[0]]]
    
    def lock_position_piece(self, row ,col, piece_value) -> tuple:
        if self.in_corner(row , col):
            if piece_value[0] == 'V':
                if row == 0:
                    piece_value = 'VB' if col == 0 else 'VE'
                else:
                    piece_value = 'VD' if col == 0 else 'VC'
                return True, piece_value
        if self.in_border(row, col):
            if piece_value[0] == 'L':
                return True,'LH' if row == 0 or row == self.board_size-1 else 'LV'
            if piece_value[0] == 'B':
                if row == 0 or row == self.board_size-1:
                    return True,'BB' if row == 0 else 'BC'
                else:
                    return True, 'BD' if col == 0 else 'BE'
        return False,''

    def get_total_piece_possibilities(self, row, col) -> list:
        possibilities = []
        if self.is_locked(row,col): return []
        piece_value = self.get_value(row, col)
        if self.in_corner(row , col):
            possibilities.append('FB' if row == 0 else 'FC')
            self.add_possibility(possibilities, 'FD' if col == 0 else 'FE')
            return possibilities
        if self.in_border(row, col):
            if piece_value[0] == 'V':
                if row == 0:
                    self.add_possibility(possibilities,'VB')
                    self.add_possibility(possibilities,'VE')
                if row == self.board_size-1:
                    self.add_possibility(possibilities,'VC')
                    self.add_possibility(possibilities,'VD')
                if col == 0:
                    self.add_possibility(possibilities,'VB')
                    self.add_possibility(possibilities,'VD')
                if col == self.board_size-1:
                    self.add_possibility(possibilities,'VE')
                    self.add_possibility(possibilities,'VC')
                return possibilities
            if piece_value[0] == 'F':
                if row == 0:
                    return [piece for piece in pieces_board[piece_value[0]] if piece != 'FC' ]
                if row == self.board_size-1:
                    return [piece for piece in pieces_board[piece_value[0]] if piece != 'FB' ]
                if col == 0:
                    return [piece for piece in pieces_board[piece_value[0]] if piece != 'FE' ]
                if col == self.board_size-1:
                    return [piece for piece in pieces_board[piece_value[0]] if piece != 'FD' ]
        else:
            return self.possibilities_no_constraints(piece_value)
        
    def get_real_possibilities_piece(self, row, col) -> list:
        adj_pieces = self.adjacent_pieces(row,col)
        total_possiblities = self.get_total_piece_possibilities(row,col)
        remove_possibilities = []
        piece_possibilities = []
        for neighbour in adj_pieces:
            if not neighbour == None:
                if self.is_locked(neighbour[0],neighbour[1]):
                    for possibility in total_possiblities:
                        if self.are_connected_full(neighbour[0],neighbour[1],self.get_value(neighbour[0],neighbour[1]), row, col,possibility) \
                            and possibility not in piece_possibilities:
                                piece_possibilities.append(possibility)
                        else:
                            if self.are_connected(neighbour[0],neighbour[1], row, col,possibility):
                                remove_possibilities.append(possibility)
                    total_possiblities = piece_possibilities if len(piece_possibilities) > 0 else self.remove_possibility(total_possiblities,remove_possibilities)
                    piece_possibilities = []
        return total_possiblities
                
    def lock_consequences(self,locked_pieces, value):
        possibilities_piece = []
        remove_possibilities = []
        pieces_counter = 0
        while pieces_counter < len(locked_pieces):
            piece = locked_pieces[pieces_counter]
            adj_pieces = self.adjacent_pieces(piece[0],piece[1])
            for neighbour in adj_pieces:
                if not neighbour == None:
                    if not self.is_locked(neighbour[0],neighbour[1]):
                        possibilities_total = self.get_total_piece_possibilities(neighbour[0],neighbour[1]) if len(possibilities[(neighbour[0],neighbour[1])]) == 0 or value\
                            else possibilities[(neighbour[0],neighbour[1])]
                        for possibility in possibilities_total:
                            if self.are_connected_full(piece[0],piece[1],self.get_value(piece[0],piece[1]), neighbour[0],neighbour[1],possibility): \
                                possibilities_piece.append(possibility)
                            else:
                                if self.are_connected(piece[0],piece[1], neighbour[0],neighbour[1],possibility):
                                    remove_possibilities.append(possibility)
                        if len(possibilities_piece) == 0:
                            possibilities_piece = self.remove_possibility(possibilities_total,remove_possibilities)
                        else: possibilities_piece = self.remove_possibility(possibilities_piece,remove_possibilities)
                        if len(possibilities_piece) == 1:
                            self.set_value(neighbour[0],neighbour[1],possibilities_piece[0])
                            self.lock(neighbour[0],neighbour[1])
                            locked_pieces.append(neighbour)
                        else: possibilities[(neighbour[0],neighbour[1])] = possibilities_piece
                    possibilities_piece = []
                    remove_possibilities = []
            pieces_counter+=1

    def dfs(self,moved_piece) -> int:
        counter = 0
        stack = []
        stack.append(moved_piece)
        while (len(stack) > 0):
            piece_coords = stack[-1]
            stack.pop()
            if not self.is_visited(piece_coords[0],piece_coords[1]):
                self.visited(piece_coords[0],piece_coords[1])
                counter += 1
            neighbours = self.get_neighbours(piece_coords[0],piece_coords[1])
            for neighbour in neighbours:
                if (neighbour[0] < 0 or neighbour[0] >= self.board_size or neighbour[1] < 0 or neighbour[1] >= self.board_size) or \
                not self.are_connected(piece_coords[0],piece_coords[1],neighbour[0],neighbour[1],
                            self.get_value(neighbour[0],neighbour[1])): return counter
                if (not self.is_visited(neighbour[0],neighbour[1])):
                    stack.append(neighbour)
        return counter
    
    def copy(self) -> dict:
        pieces_copy = {}
        for key,piece in self.pieces.items():
            pieces_copy[key] = [piece[0],piece[1],False]
        return pieces_copy
    
    def to_string(self)->str:
        """Escreve a grelha de peças no standard output(stdout)"""
        piece_counter = 0
        board_str = ""
        for piece in self.pieces.values():
            piece_counter += 1
            if piece_counter == self.board_size**2: board_str += piece[0]
            else: board_str += (piece[0] + "\t") if piece_counter % self.board_size > 0  else (piece[0] + "\n")
        return board_str
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        row = 0
        locked_pieces = []
        pieces = {}
        line = stdin.readline().split()
        board = Board(pieces, len(line))
        pieces_per_row = len(line)
        for i in range(pieces_per_row):
            possibilities[(row,i)] = []
            (locked_state, value_piece) = board.lock_position_piece(row,i,line[i])
            piece = [value_piece if locked_state else line[i],locked_state,False]
            if locked_state: locked_pieces.append((row,i))
            board.add_Piece(row, i, piece)
        for i in range(pieces_per_row-1):
            line = stdin.readline().split()
            pieces_per_row = len(line)
            row+=1
            for j in range(pieces_per_row):
                possibilities[(row,j)] = []
                (locked_state,value_piece) = board.lock_position_piece(row,j,line[j])
                piece = [value_piece if locked_state else line[j],locked_state,False]
                if locked_state: locked_pieces.append((row,j))
                board.add_Piece(row, j, piece)
        board.lock_consequences(locked_pieces,False)
        return board

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board.get_pieces(), board.get_board_size(), board.get_next_piece(0,0))
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        board = Board(state.get_board_pieces(),state.get_board_size())
        if state.get_next_move_piece() == (state.get_board_size()-1, state.get_board_size()-1): return []
        (row,col) = state.get_next_move_piece()
        possibilities = board.get_real_possibilities_piece(row,col)
        actions += map(lambda piece_value: (row, col, piece_value),possibilities)
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, piece_value) = action
        result_board = Board(state.copy_pieces_board(),state.get_board_size())
        result_board.set_value(row,col,piece_value)
        result_board.lock(row,col)
        result_board.lock_consequences([(row,col)],True)
        return PipeManiaState(result_board.get_pieces(),state.get_board_size(), result_board.get_next_piece(row,col))
    
    def goal_test(self, state: PipeManiaState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = Board(state.get_board_pieces(),state.get_board_size())
        if state.get_next_move_piece() != (state.get_board_size()-1, state.get_board_size()-1): return False
        return board.dfs(state.get_next_move_piece()) == state.get_board_size()**2
    
    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""

if __name__ == "__main__":
    
    board = Board.parse_instance()

    problem = PipeMania(board)

    goal_node = depth_first_tree_search(problem)

    print(Board(goal_node.state.get_board_pieces(),goal_node.state.get_board_size()).to_string())
