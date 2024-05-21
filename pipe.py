# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 70:
# 106171 Guilherme Vaz Rocha
# 106454 Manuel Tiago Martins

import sys
#import time
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
unlocked_pieces = []
counter = 0
class PipeManiaState:
    state_id = 0
    last_moved_piece = () 
    def __init__(self, pieces, board_size, last_moved_piece):
        self.pieces = pieces
        self.board_size = board_size
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.last_moved_piece = last_moved_piece

    def __lt__(self, other):
        return self.id < other.id
    
    def copy_pieces_board(self) -> tuple:
        pieces_copy = {}
        for key,piece in self.pieces.items():
            pieces_copy[key] = [piece[0],piece[1],False]
        return pieces_copy
    
    def get_last_moved_piece(self) -> tuple: return self.last_moved_piece

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

    def adjacent_pieces(self, row: int, col: int) -> (tuple, tuple,tuple,tuple,tuple):
        """Devolve os valores imediatamente acima e abaixo,
        respetivamente."""
        return (row-1, col) if row > 0 else None , (row+1,col) if row < (self.board_size-1) else None, (row, col-1) if col > 0 else None , (row,col+1) if col < (self.board_size-1) else None
    
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
                next_row, next_col = self.board_size-1,self.board_size-1
                break
        return next_row,next_col

    def are_connected(self, row1, col1, row2, col2, piece_value) -> bool:
        if row2 > row1: return piece_value in ['FC','BC','BE','BD','VC','VD','LV'] #peças com ligação cima
        if row2 < row1: return piece_value in ['FB','BB','BE','BD','VB','VE','LV'] #peças com ligação baixo
        if col2 > col1: return piece_value in ['FE','BC','BB','BE','VC','VE','LH'] #peças com ligação esquerda
        if col2 < col1: return piece_value in ['FD','BC','BB','BD','VB','VD','LH'] #peças com ligação direita

    def are_connected_full(self, row1, col1, piece_value1, row2, col2, piece_value2) -> bool:
        if row2 > row1: return piece_value1 in ['FB','BB','BE','BD','VB','VE','LV'] and piece_value2 in ['FC','BC','BE','BD','VC','VD','LV']
        if row2 < row1: return piece_value1 in ['FC','BC','BE','BD','VC','VD','LV'] and piece_value2 in ['FB','BB','BE','BD','VB','VE','LV'] #peças com ligação baixo
        if col2 > col1: return piece_value1 in ['FD','BC','BB','BD','VB','VD','LH'] and piece_value2 in ['FE','BC','BB','BE','VC','VE','LH'] #peças com ligação esquerda
        if col2 < col1: return piece_value1 in ['FE','BC','BB','BE','VC','VE','LH'] and piece_value2 in ['FD','BC','BB','BD','VB','VD','LH'] #peças com ligação direita
    
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

    def add_possibility(self, possibilities, piece_value, new_possibility):
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
            self.add_possibility(possibilities, piece_value, 'FB' if row == 0 else 'FC')
            self.add_possibility(possibilities, piece_value, 'FD' if col == 0 else 'FE')
            return possibilities
        if self.in_border(row, col):
            if piece_value[0] == 'V':
                if row == 0:
                    self.add_possibility(possibilities, piece_value,'VB')
                    self.add_possibility(possibilities, piece_value,'VE')
                if row == self.board_size-1:
                    self.add_possibility(possibilities, piece_value,'VC')
                    self.add_possibility(possibilities, piece_value,'VD')
                if col == 0:
                    self.add_possibility(possibilities, piece_value,'VB')
                    self.add_possibility(possibilities, piece_value,'VD')
                if col == self.board_size-1:
                    self.add_possibility(possibilities, piece_value,'VE')
                    self.add_possibility(possibilities, piece_value,'VC')
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

    def lock_consequences(self,locked_pieces):
        possibilities_piece = []
        remove_possibilities = []
        pieces_counter = 0
        while pieces_counter < len(locked_pieces):
            piece = locked_pieces[pieces_counter]
            adj_pieces = self.adjacent_pieces(piece[0],piece[1])
            for neighbour in adj_pieces:
                if not neighbour == None:
                    if not self.is_locked(neighbour[0],neighbour[1]):
                        possibilities_total = self.get_total_piece_possibilities(neighbour[0],neighbour[1]) if len(possibilities[(neighbour[0],neighbour[1])]) == 0 \
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
                            locked_pieces.append((neighbour[0],neighbour[1]))
                            unlocked_pieces.remove((neighbour[0],neighbour[1]))
                            possibilities[(neighbour[0],neighbour[1])] = []
                        else: possibilities[(neighbour[0],neighbour[1])] = possibilities_piece
                    possibilities_piece = []
                    remove_possibilities = []
            pieces_counter+=1

    def dfs(self,moved_piece) -> bool:
        counter = 0
        stack = []
        stack.append(unlocked_pieces[moved_piece] if len(unlocked_pieces) > 0 and moved_piece < len(unlocked_pieces)-1 else (0,0))
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
                            self.get_value(neighbour[0],neighbour[1])): return False
                if (not self.is_visited(neighbour[0],neighbour[1])):
                    stack.append(neighbour)
        return counter == self.board_size**2
    
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
            else: unlocked_pieces.append((row,i))
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
                else: unlocked_pieces.append((row,j))
                board.add_Piece(row, j, piece)
        board.lock_consequences(locked_pieces)
        #print(possibilities)
        # print('unlocked pieces')
        # print(unlocked_pieces)
        # print(len(unlocked_pieces))
        return board

    # TODO: outros metodos da classe

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board.get_pieces(), board.get_board_size(), 0)
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        board = Board(state.get_board_pieces(),state.get_board_size())
        #last_piece = state.get_last_moved_piece()
        #if last_piece == (board.board_size-1, board.board_size-1): return actions
        if state.get_last_moved_piece() >= len(unlocked_pieces):
            print('yup')
            return []
        else: (row,col) = unlocked_pieces[state.get_last_moved_piece()]
        # print(row,col)
        # print ("->")
        # print((row,col))
        #if (row == board.board_size-1 and col == board.board_size-1 and board.is_locked(row,col)): return actions
        if len(possibilities[(row,col)]) == 0:
            possibilities[(row,col)] = board.get_total_piece_possibilities(row,col)
        possibilities_piece = possibilities[(row,col)]
        real_possibilities = []
        neighbours = board.adjacent_pieces(row,col)
        entered = False
        #print(neighbours)
        for neighbour in neighbours:
            #print(board.is_connection(neighbour[0],neighbour[1],row,col))
            if neighbour is not None:
                if board.is_locked(neighbour[0],neighbour[1]) and board.is_connection(neighbour[0],neighbour[1],row,col):
                    #print(board.is_connection(neighbour[0],neighbour[1],row,col))
                    entered = True
                    for possiblity in possibilities_piece:
                        if board.are_connected_full(neighbour[0], neighbour[1],board.get_value(neighbour[0], neighbour[1]), row, col , possiblity) and possiblity not in real_possibilities:
                            real_possibilities.append(possiblity)

        if len(real_possibilities) == 0 and entered: return actions

        #     print(row,col)
        #     print(possibilities_piece)
        #     return actions

        # for neighbour in neighbours:
        #     for possiblity in possibilities_piece:
        #         if board.are_connected(neighbour[0],neighbour[1], row,col, possiblity) and possiblity not in real_possibilities:
        #             real_possibilities.append(possiblity)
        actions += map(lambda piece_value: (row, col, piece_value), real_possibilities if len(real_possibilities) > 0 else possibilities_piece)
        #print(actions)
        #if (row,col) in unlocked_pieces: print(actions)
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, piece_value) = action
        print(action)
        result_board = Board(state.copy_pieces_board(),state.get_board_size)
        result_board.set_value(row,col,piece_value)
        result_board.lock(row,col)
        move_piece = state.get_last_moved_piece()+1
        neighbours = result_board.get_neighbours(row,col)
        #print(row,col)
        for neighbour in neighbours:
            if result_board.is_locked(neighbour[0],neighbour[1]) and not \
                result_board.are_connected(row,col,neighbour[0],neighbour[1], result_board.get_value(neighbour[0],neighbour[1])): move_piece = len(unlocked_pieces)+1
        print(move_piece)
        #result_board.lock(row,col)
        # print((row,col))
        # print(result_board.get_pieces()[(row,col)][0])
        #last_moved_piece = state.get_last_moved_piece() + 1 if state.get_last_moved_piece() < len(unlocked_pieces)-1 else len(unlocked_pieces)-1
        #print(last_moved_piece)
        return PipeManiaState(result_board.get_pieces(),state.get_board_size(), move_piece)

    def goal_test(self, state: PipeManiaState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        board = Board(state.get_board_pieces(),state.get_board_size())
        if state.get_last_moved_piece() != len(unlocked_pieces): return False
        # for piece in unlocked_pieces:
        #     if not board.is_locked(piece[0],piece[1]):
        #         pieces_unlocked.append(piece)
                #return False
        # print (pieces_unlocked)
        # print(state.get_last_moved_piece())
        # print(board.to_string())
        # print('\n')
        #print(state.get_last_moved_piece())

        
        

        #     neighbours = board.get_neighbours(piece[0], piece[1])
        #     for neighbour in neighbours:
        #         if neighbour in unlocked_pieces and board.is_locked(neighbour[0],neighbour[1]) and \
        #             not board.are_connected(piece[0], piece[1], neighbour[0], neighbour[1], board.get_value(neighbour[0], neighbour[1])): return False
        last_moved_piece = len(unlocked_pieces)
        #print(last_moved_piece)
        # counter = 0
        # for piece in unlocked_pieces:
        #     neighbours = board.get_neighbours(piece[0],piece[1])
        #     for neighbour in neighbours:
        #         if not board.are_connected(piece[0],piece[1],neighbour[0],neighbour[1],board.get_value(neighbour[0],neighbour[1])):
        #             return False
        # print(counter)
        return board.dfs(last_moved_piece)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        pass

if __name__ == "__main__":
    #start_time = time.time()
    
    board = Board.parse_instance()

    problem = PipeMania(board)

    goal_node = depth_first_tree_search(problem)

    print(Board(goal_node.state.get_board_pieces(),goal_node.state.get_board_size()).to_string())
    
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"Elapsed time: {elapsed_time*1000} ms")