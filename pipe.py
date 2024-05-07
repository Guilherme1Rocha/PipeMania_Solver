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

rotation = {'C':'DE', 'B':'ED', 'E':'CB', 'D':'BC','H':'VV','V':'HH'}
last_moved_piece = ()
pieces = {'F': ['FE','FB','FC','FD'], 'V': ['VE','VC','VB','VD'], 'B': ['BE','BD','BC','BB'], 'L': ['LV','LH']}
class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

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

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respetivamente."""
        return self.get_value(row-1, col) if row > 0 else None , self.get_value(row+1,col) if row < (self.board_size-1) else None
    
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respetivamente."""
        return self.get_value(row, col-1) if col > 0 else None , self.get_value(row,col+1) if col < (self.board_size-1) else None
    
    def rotate_piece(self,action) -> str:
        direction = 0 if action[2] else 1
        piece = self.get_value(action[0],action[1])
        return(piece[0] + (rotation[piece[1]])[direction])

    def are_connected(self, row1, col1, row2, col2) -> bool:
        if (row2 < 0 or row2 >= self.board_size or col2 < 0 or col2 >= self.board_size): return False
        if row2 > row1: return self.get_value(row2,col2) in ['FC','BC','BE','BD','VC','VD','LV'] #peças com ligação cima
        if row2 < row1: return self.get_value(row2,col2) in ['FB','BB','BE','BD','VB','VE','LV'] #peças com ligação baixo
        if col2 > col1: return self.get_value(row2,col2) in ['FE','BC','BB','BE','VC','VE','LH'] #peças com ligação esquerda
        if col2 < col1: return self.get_value(row2,col2) in ['FD','BC','BB','BD','VB','VD','LH'] #peças com ligação direita
    
    def get_neighbours(self, row, col) -> list:
        neighbours = []
        piece_value = self.get_value(row,col)
        if piece_value[0] == 'F':
            if piece_value[1] == 'C':
                if (not self.are_connected(row,col,row-1,col)): return []
                neighbours.append((row-1,col))
            if piece_value[1] == 'B':
                if (not self.are_connected(row,col,row+1,col)): return []
                neighbours.append((row+1,col))
            if piece_value[1] == 'E':
                if (not self.are_connected(row,col,row,col-1)): return []
                neighbours.append((row,col-1))
            if piece_value[1] == 'D':
                if (not self.are_connected(row,col,row,col+1)): return []
                neighbours.append((row,col+1))
       
        if piece_value[0] == 'B':
            if piece_value[1] == 'C':
                if (not (self.are_connected(row,col,row,col-1) and self.are_connected(row,col,row-1,col) and self.are_connected(row,col,row,col+1))): return []
                neighbours.append((row,col-1))
                neighbours.append((row-1,col))
                neighbours.append((row,col+1))
            if piece_value[1] == 'B':
                if (not (self.are_connected(row,col,row,col-1) and self.are_connected(row,col,row+1,col) and self.are_connected(row,col,row,col+1))): return []
                neighbours.append((row,col-1))
                neighbours.append((row+1,col))
                neighbours.append((row,col+1))
            if piece_value[1] == 'E':
                if (not (self.are_connected(row,col,row,col-1) and self.are_connected(row,col,row+1,col) and self.are_connected(row,col,row-1,col))): return []
                neighbours .append((row,col-1))
                neighbours .append((row+1,col))
                neighbours .append((row-1,col))
            if piece_value[1] == 'D':
                if (not (self.are_connected(row,col,row-1,col) and self.are_connected(row,col,row,col+1) and self.are_connected(row,col,row+1,col))): return []
                neighbours .append ((row-1,col))
                neighbours .append ((row,col+1))
                neighbours .append ((row+1,col))
                
        if piece_value[0] == 'V':
            if piece_value[1] == 'C':
                if (not (self.are_connected(row,col,row-1,col) and self.are_connected(row,col,row,col-1))): return []
                neighbours .append ((row-1,col))
                neighbours .append ((row,col-1))
            if piece_value[1] == 'B':
                if (not (self.are_connected(row,col,row+1,col) and self.are_connected(row,col,row,col+1))): return []
                neighbours .append ((row+1,col))
                neighbours .append ((row,col+1))
            if piece_value[1] == 'E':
                if (not (self.are_connected(row,col,row+1,col) and self.are_connected(row,col,row,col-1))): return []
                neighbours .append ((row+1,col))
                neighbours .append ((row,col-1))
            if piece_value[1] == 'D':
                if (not (self.are_connected(row,col,row-1,col) and self.are_connected(row,col,row,col+1))): return []
                neighbours .append ((row-1,col))
                neighbours .append ((row,col+1))
        if piece_value[0] == 'L':
            if piece_value[1] == 'H':
                if (not (self.are_connected(row,col,row,col-1) and self.are_connected(row,col,row,col+1))): return []
                neighbours .append ((row,col-1))
                neighbours .append ((row,col+1))
            if piece_value[1] == 'V':
                if (not (self.are_connected(row,col,row+1,col) and self.are_connected(row,col,row-1,col))): return []
                neighbours .append ((row-1,col))
                neighbours .append ((row+1,col))
        return neighbours

    def in_corner(self, row, col) -> bool: return (row == 0 or row == self.board_size-1) and (col == 0 or col == self.board_size-1)

    def in_border(self, row ,col) -> bool: return row == 0 or row == self.board_size-1 or col == 0 or col == self.board_size-1

    def add_possibility(self, possibilities, piece_value, new_possibility):
        if piece_value != new_possibility: possibilities.append(new_possibility)
        return possibilities
    
    def possibilities_no_constraints(self, piece_value) -> list:
        return [piece for piece in pieces[piece_value[0]] if piece != piece_value]

    def get_piece_possibilities(self, row, col) -> list:
        possibilities = []
        piece = self.get_Piece(row, col)
        if piece.is_locked(): return []
        piece_value = self.get_value(row, col)
        if self.in_corner(row , col):
            if piece_value[0] == 'V':
                piece.lock()
                if row == 0:
                    piece_value = 'VB' if col == 0 else 'VE'
                else:
                    piece_value = 'VD' if col == 0 else 'VC'
                self.set_value(row, col, piece_value)
                return []
            else:
                self.add_possibility(possibilities, piece_value, 'FB' if row == 0 else 'FC')
                self.add_possibility(possibilities, piece_value, 'FD' if col == 0 else 'FE')
                return possibilities
        if self.in_border(row, col):
            if piece_value[0] == 'L':
                piece.lock()
                self.set_value(row, col, 'LH' if row == 0 or row == self.board_size-1 else 'LV')
                return []
            if piece_value[0] == 'B':
                piece.lock()
                if row == 0 or row == self.board_size-1:
                    self.set_value(row, col , 'BB' if row == 0 else 'BC')
                else:
                    self.set_value(row, col , 'BD' if col == 0 else 'BE')
                return []
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
                    return [piece for piece in pieces[piece_value[0]] if piece != ('FC' or piece_value)]
                if row == self.board_size-1:
                    return [piece for piece in pieces[piece_value[0]] if piece != ('FB' or piece_value)]
                if col == 0:
                    return [piece for piece in pieces[piece_value[0]] if piece != ('FE' or piece_value)]
                if col == self.board_size-1:
                    return [piece for piece in pieces[piece_value[0]] if piece != ('FD' or piece_value)]
        else:
            return self.possibilities_no_constraints(piece_value)

    def dfs(self) -> bool:
        counter = 0
        for value in self.pieces.values():
            value.visited_state = False
        stack = []
        stack.append((0,0))
        while (len(stack) > 0):
            piece_coords = stack[-1]
            stack.pop()
            piece = self.get_Piece(piece_coords[0],piece_coords[1])
            if (not piece.visited_state):
                piece.visited_state = True
                counter += 1
            neighbours = self.get_neighbours(piece_coords[0],piece_coords[1])
            print(neighbours)
            if neighbours == []: return False
            for piece in neighbours:
                if (not self.get_Piece(piece[0],piece[1]).visited_state):
                    stack.append(piece)
        return counter == self.board_size**2
    
    # def copy(self) -> dict:
    #     pieces_copy = {}
    #     for key,piece in self.pieces.items():
    #         pieces_copy[key] = Piece(piece.value,piece.locked_state,piece.visited_state)
    #     return pieces_copy
    
    def print(self):
        """Escreve a grelha de peças no standard output(stdout)"""
        piece_counter = 0
        board_str = ""
        for piece in self.pieces.values():
            piece_counter += 1
            if piece_counter == self.board_size*self.board_size: board_str += piece.value
            else: board_str += (piece.value + "\t") if piece_counter % self.board_size > 0  else (piece.value + "\n")
        print(board_str)
    
    # @staticmethod
    # def is_corner(row ,col, board_size) -> bool:
    #     return ((row == 0 or row == board_size-1) and (col == 0 or col == board_size-1))
    # @staticmethod
    # def piece_lock(row, col, value, board_size) -> str:
    #     if (value[0] == 'L'):
    #         if (col == 0 or col == board_size): return 'LV'
    #         if (row == 0 or row == board_size): return 'LH'
    #     else:
    #         if (row == 0):
    #             if col == 0: return 'VB'
    #             else: return 'VE'
    #         else:
    #             if col == 0: return 'VD'
    #             else: return 'VC'
    #     return ''       
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
        pieces = {}
        line = stdin.readline().split()
        pieces_per_row = len(line)
        for i in range(pieces_per_row):
            pieces[(row,i)] = Piece(line[i],False,False)
        for i in range(pieces_per_row-1):
            line = stdin.readline().split()
            pieces_per_row = len(line)
            row+=1
            for j in range(pieces_per_row):
                pieces[(row,j)] = Piece(line[j],False,False)
        # for key,value in pieces.items():
        #     print(key,':',value)
        return Board(pieces,pieces_per_row)

    # TODO: outros metodos da classe


class PipeMania(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = PipeManiaState(board)
        super().__init__(state)

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        actions_test = []
        for row in range(state.board.board_size):
            for col in range(state.board.board_size):
                if not state.board.get_Piece(row,col).is_locked() and last_moved_piece != (row,col):
                    possibilities = state.board.get_piece_possibilities(row, col)
                    if len(possibilities) > 0:
                        actions_test += map(lambda piece_value: (row, col, piece_value), possibilities)
                actions.append((row,col,False))
                actions.append((row,col,True))
        print(actions_test)
        return actions_test

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        last_moved_piece = (action[0],action[1])
        (row, col, piece_value) = action
        result_state = PipeManiaState(state.board)
        result_state.board.set_value(row,col,piece_value)
        # result_state.board.print()
        # print('\n')
        return result_state

    def goal_test(self, state: PipeManiaState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.dfs()

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
    goal_node = breadth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    #print("Is goal?", problem.goal_test(goal_node.state))
    goal_node.state.board.print()
    #print("Solution:\n", goal_node.state.board.print(), sep="")
    pass
