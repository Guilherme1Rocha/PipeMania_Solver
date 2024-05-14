# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 70:
# 106171 Guilherme Vaz Rocha
# 106454 Manuel Tiago Martins

import sys
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

#rotation = {'C':'DE', 'B':'ED', 'E':'CB', 'D':'BC','H':'VV','V':'HH'}
pieces = {'F': ['FE','FB','FC','FD'], 'V': ['VE','VC','VB','VD'], 'B': ['BE','BD','BC','BB'], 'L': ['LV','LH']}
second_piece = []
locked_state = False
possibilities = {}
class PipeManiaState:
    state_id = 0
    last_moved_piece = ()

    def __init__(self, board, last_moved_piece):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1
        self.last_moved_piece = last_moved_piece

    def __lt__(self, other):
        return self.id < other.id
    
    def get_last_moved_piece(self) -> tuple: return self.last_moved_piece

    # TODO: outros metodos da classe

class Piece:
    def __init__(self, value, locked_state, visited_state):
        self.value = value
        self.locked_state = locked_state
        self.visited_state = visited_state

    def get_value_piece(self) -> str:
        return self.value
    
    def set_value_piece(self,value):
        self.value = value

    def is_locked(self) -> bool:
        return self.locked_state
    
    def lock(self):
        self.locked_state = True
    
    def unlock(self):
        self.locked_state = False

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, pieces, board_size):
        self.pieces = pieces
        self.board_size = board_size
    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        piece = self.pieces[(row,col)]
        return piece.get_value_piece()
    
    def set_value(self, row: int , col:int , value:str):
        """Atualiza o valor na respetiva posição do tabuleiro"""
        piece = self.pieces[(row,col)]
        piece.set_value_piece(value)

    def get_Piece(self, row:int , col:int) -> Piece:
        return self.pieces[(row,col)]
    
    def add_Piece(self, row, col, piece):
        self.pieces[(row,col)] = piece

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respetivamente."""
        return self.get_value(row-1, col) if row > 0 else None , self.get_value(row+1,col) if row < (self.board_size-1) else None
    
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respetivamente."""
        return self.get_value(row, col-1) if col > 0 else None , self.get_value(row,col+1) if col < (self.board_size-1) else None
    
    def get_next_piece(self, row, col) -> tuple:
        if col < self.board_size-1: next_row, next_col = row,col+1
        else: next_row, next_col = row+1,0
        if (row < 0 or col < 0):
            next_row = 0
            next_col = 0
        # if row == self.board_size-1 and col ==  self.board_size-1:
        #     next_row, next_col = 0,0
        while (self.get_Piece(next_row,next_col).is_locked()):
            if next_col < self.board_size-1: 
                next_row, next_col = next_row,next_col+1
            else: next_row, next_col = next_row+1, 0
        # if next_row == 0 and next_col == 0:
        #     print("first piece or over: ")
        #     print(next_row,next_col)
        return next_row,next_col

    # def rotate_piece(self,action) -> str:
    #     direction = 0 if action[2] else 1
    #     piece = self.get_value(action[0],action[1])
    #     return(piece[0] + (rotation[piece[1]])[direction])

    def are_connected(self, row1, col1, row2, col2, piece_value) -> bool:
        if row2 > row1: return piece_value in ['FC','BC','BE','BD','VC','VD','LV'] #peças com ligação cima
        if row2 < row1: return piece_value in ['FB','BB','BE','BD','VB','VE','LV'] #peças com ligação baixo
        if col2 > col1: return piece_value in ['FE','BC','BB','BE','VC','VE','LH'] #peças com ligação esquerda
        if col2 < col1: return piece_value in ['FD','BC','BB','BD','VB','VD','LH'] #peças com ligação direita
    
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
        #if piece_value != new_possibility: possibilities.append(new_possibility)
        possibilities.append(new_possibility)
        return possibilities
    
    def possibilities_no_constraints(self, piece_value) -> list:
        #return [piece for piece in pieces[piece_value[0]] if piece != piece_value]
        return [piece for piece in pieces[piece_value[0]]]
    
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

    def get_piece_possibilities(self, row, col) -> list:
        possibilities = []
        piece = self.get_Piece(row, col)
        if piece.is_locked(): return []
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
                    return [piece for piece in pieces[piece_value[0]] if piece != 'FC' ]
                if row == self.board_size-1:
                    return [piece for piece in pieces[piece_value[0]] if piece != 'FB' ]
                if col == 0:
                    return [piece for piece in pieces[piece_value[0]] if piece != 'FE' ]
                if col == self.board_size-1:
                    return [piece for piece in pieces[piece_value[0]] if piece != 'FD' ]
        else:
            return self.possibilities_no_constraints(piece_value)
    
    def lock_consequences(self,locked_pieces):
        possibilities_piece = []
        pieces_counter = 0
        while pieces_counter < len(locked_pieces):
            #print(locked_pieces)
            piece = locked_pieces[pieces_counter]
            neighbours = self.get_neighbours(piece[0],piece[1])
            print(piece)
            print("neighbours: ")
            print(neighbours)
            #print('-----------------------')
            for neighbour in  neighbours:
                if not self.get_Piece(neighbour[0],neighbour[1]).is_locked():
                    print(neighbour)
                    possibilities_total = self.get_piece_possibilities(neighbour[0],neighbour[1])
                    print(possibilities_total)
                    for possibility in possibilities_total:
                        if self.are_connected(piece[0],piece[1], neighbour[0],neighbour[1],possibility): possibilities_piece.append(possibility)
                    print(possibilities_piece)
                    if len(possibilities) == 1:
                        self.set_value(neighbour[0],neighbour[1],possibilities_piece[0])
                        self.get_Piece(neighbour[0],neighbour[1]).lock()
                        locked_pieces.append((neighbour[0],neighbour[1]))
                    else: possibilities[(neighbour[0],neighbour[1])] = possibilities_piece
                    #print(possibilities_piece)
                    print('-----------------------')
                possibilities_piece = []
            pieces_counter+=1
        print(possibilities)

    def dfs(self,last_moved_piece) -> bool:
        #print("-----------------------")
        #self.print()
        #print('\n')
        counter = 0
        # for value in self.pieces.values():
        #     value.visited_state = False
        stack = []
        stack.append(last_moved_piece if last_moved_piece != (-1,-1) else (0,0))
        while (len(stack) > 0):
            piece_coords = stack[-1]
            stack.pop()
            piece = self.get_Piece(piece_coords[0],piece_coords[1])
            if (not piece.visited_state):
                piece.visited_state = True
                counter += 1
            neighbours = self.get_neighbours(piece_coords[0],piece_coords[1])
            for neighbour in neighbours:
                if (neighbour[0] < 0 or neighbour[0] >= self.board_size or neighbour[1] < 0 or neighbour[1] >= self.board_size) or \
                not self.are_connected(piece_coords[0],piece_coords[1],neighbour[0],neighbour[1],
                            self.get_value(neighbour[0],neighbour[1])): return False
            # print(piece.get_value_piece() + ": ")
            # print(piece_coords)
            # print(neighbours)

            # if neighbours == []:
            #     print('sai') 
            #     return False
            for piece in neighbours:
                if (not self.get_Piece(piece[0],piece[1]).visited_state):
                    stack.append(piece)
        #print("-----------------------")
        return counter == self.board_size**2
    
    def copy(self) -> dict:
        pieces_copy = {}
        for key,piece in self.pieces.items():
            pieces_copy[key] = Piece(piece.value,piece.locked_state,False)
        return pieces_copy
    
    def print(self):
        """Escreve a grelha de peças no standard output(stdout)"""
        piece_counter = 0
        board_str = ""
        for piece in self.pieces.values():
            piece_counter += 1
            if piece_counter == self.board_size*self.board_size: board_str += piece.value
            else: board_str += (piece.value + "\t") if piece_counter % self.board_size > 0  else (piece.value + "\n")
        print(board_str)
    
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
            piece = Piece(value_piece if locked_state else line[i],locked_state,False)
            if locked_state: locked_pieces.append((row,i))
            board.add_Piece(row, i, piece)
        for i in range(pieces_per_row-1):
            line = stdin.readline().split()
            pieces_per_row = len(line)
            row+=1
            for j in range(pieces_per_row):
                possibilities[(row,j)] = []
                (locked_state,value_piece) = board.lock_position_piece(row,j,line[j])
                piece = Piece(value_piece if locked_state else line[j],locked_state,False)
                if locked_state: locked_pieces.append((row,j))
                board.add_Piece(row, j, piece)
        print("locked_pieces: ")
        print(locked_pieces)
        board.lock_consequences(locked_pieces)
        
        #board.lock_consequences(locked_pieces)
        # for key,value in possibilities.items():
        #     print(key,':',value)
        return board

    # TODO: outros metodos da classe

class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board, (-1,-1))
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        last_piece = state.get_last_moved_piece()
        if last_piece == (state.board.board_size-1, state.board.board_size-1): return actions
        (row, col) = state.board.get_next_piece(last_piece[0],last_piece[1])
        print(last_piece)
        print ("->")
        print((row,col))
        if len(possibilities[(row,col)]) == 0:
            possibilities_piece = state.board.get_piece_possibilities(row,col)
            possibilities[(row,col)] = possibilities_piece
        else: possibilities_piece = possibilities[(row,col)]
        actions += map(lambda piece_value: (row, col, piece_value), possibilities_piece)
        #print(actions)
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        (row, col, piece_value) = action
        #print(action)
        pieces_copy = state.board.copy()
        result_board = Board(pieces_copy, state.board.board_size)
        result_state = PipeManiaState(result_board, (row,col))
        result_state.board.set_value(row,col,piece_value)
        # result_state.board.print()
        # print('\n')
        return result_state

    def goal_test(self, state: PipeManiaState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.dfs(state.last_moved_piece)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler grelha do figura 1a:
    board = Board.parse_instance()
    # Criar uma instância de PipeMania:
    problem = PipeMania(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    #print("Is goal?", problem.goal_test(goal_node.state))
    #goal_node.state.board.print()
    # print("special piece actions: " )
    # print(second_piece)
    # print("locked_state: ")
    # print(locked_state)
    print("Solution:\n", goal_node.state.board.print(), sep="")
    pass
