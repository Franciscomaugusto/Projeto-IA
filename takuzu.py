# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 12:
# 99218 Francisco Augusto
# 99265 Luis Marques

import sys
import numpy

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


def list_creation(number):
    lst = [[]] * number
    for i in range(number):
        lst[i] = [] * number
    return lst


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, positions, n):
        self.structure = positions
        self.number = n

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.positions[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row == 0:
            lista = [None][self.positions[row + 1][col]]
        elif row == self.number:
            lista = [self.positions[row - 1][col]][None]
        else:
            lista = [self.positions[row - 1][col]][self.positions[row + 1][col]]
        return lista

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        if col == 0:
            lista = [None][self.positions[row][col + 1]]
        elif col == self.number:
            lista = [self.positions[row][col - 1]][None]
        else:
            lista = [self.positions[row][col - 1]][self.positions[row][col + 1]]
        return lista

    def search_three_follow_vertical(self, row: int, col: int):
        if row >= 2:
            if self.positions[row - 1][col] == self.positions[row - 2][col]:
                return True
        elif row <= self.number - 2:
            if self.positions[row + 1][col] == self.positions[row + 2][col]:
                return True
        return False

    def search_three_follow_horizontal(self, row: int, col: int):
        if col >= 2:
            if self.positions[row][col - 1] == self.positions[row][col - 2]:
                return True
        elif col <= self.number - 2:
            if self.positions[row][col - 1] == self.positions[row][col - 2]:
                return True
        return False

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        Por exemplo:
            $ python3 takuzu.py < input_T01
            > from sys import stdin
            > stdin.readline()
        """
        m = int(sys.stdin.readline())
        temp = list_creation(m)
        for i in range(m):
            line = sys.stdin.readline()
            row = [int(s) for s in line.split() if s.isdigit()]
            temp[i] = row
        return Board(temp, m)

    def write(self):
        representation = ''
        for i in range(self.number):
            print(self.structure[i])

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    b1 = Board.parse_instance_from_stdin()
    b1.write()
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
