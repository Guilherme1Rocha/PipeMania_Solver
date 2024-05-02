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
class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = PipeManiaState.state_id
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, pieces, board_size):
        self.pieces = pieces
        self.board_size = board_size
    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.pieces[(row,col)]
    def set_value(self, row: int , col:int , value:str):
        """Atuliza o valor na respetiva posição do tabuleiro"""
        self.pieces[(row,col)] = value
    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return self.get_value(row-1, col) if row > 0 else None , self.get_value(row+1,col) if row < (self.board_size-1) else None
    
    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return self.get_value(row, col-1) if col > 0 else None , self.get_value(row,col+1) if col < (self.board_size-1) else None
    
    def rotate(self,action) -> str:
        direction = 0 if action[2] else 1
        piece = self.get_value(action[0],action[1])
        return(piece[0] + (rotation[piece[1]])[direction])

    def print_board(self):
        piece_counter = 0
        board_str = ""
        for piece in self.pieces.values():
            piece_counter += 1
            if piece_counter == self.board_size*self.board_size: board_str += piece
            else: board_str += (piece + "\t") if piece_counter % self.board_size > 0  else (piece + "\n")
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
        pieces = {}
        line = stdin.readline().split()
        pieces_per_row = len(line)
        for i in range(pieces_per_row):
            pieces[(row,i)] = line[i]
        for i in range(pieces_per_row-1):
            line = stdin.readline().split()
            pieces_per_row = len(line)
            row+=1
            for j in range(pieces_per_row):
                pieces[(row,j)] = line[j]
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
        for row in range(state.board.board_size):
            for col in range(state.board.board_size):
                actions.append((row,col,False))
                actions.append((row,col,True))
        return actions

    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        result_state = PipeManiaState(state.board)
        result_state.board.set_value(action[0],action[1],result_state.board.rotate(action))
        return result_state

    def goal_test(self, state: PipeManiaState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board = Board.parse_instance()
    board.print_board()
    print('\n')
    problem = PipeMania(board)
    initial_state = PipeManiaState(board)
    result_state = problem.result(initial_state,(0,0,True))

    result_state.board.print_board()
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
