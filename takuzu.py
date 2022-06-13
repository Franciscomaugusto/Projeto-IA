# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 12:
# 99218 Francisco Augusto
# 99265 Luis Marques

import sys
import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


# Functions of no specific class

def list_creation(number):
    lst = [[]] * number
    for i in range(number):
        lst[i] = [] * number
    return lst

class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, structure: np.array, n: int):
        self.positions = structure
        self.number = n

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.positions[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row == 0:
            lista = [None, self.positions[row + 1, col]]
        elif row == self.number:
            lista = [self.positions[row - 1, col], None]
        else:
            lista = [self.positions[row - 1, col], self.positions[row + 1, col]]
        return lista

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        if col == 0:
            lista = [None, self.positions[row, col + 1]]
        elif col == self.number:
            lista = [self.positions[row, col - 1], None]
        else:
            lista = [self.positions[row, col - 1], self.positions[row, col + 1]]
        return lista

    def search_three_follow_vertical(self, row: int, col: int, num: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers vertically"""
        if row >= 2:
            if self.positions[row - 1, col] == self.positions[row - 2, col] == num:
                return True
        elif row <= self.number - 2:
            if self.positions[row + 1, col] == self.positions[row + 2, col] == num:
                return True
        return False

    def search_three_follow_horizontal(self, row: int, col: int, num: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers horizontally"""
        if col >= 2:
            if self.positions[row, col - 1] == self.positions[row, col - 2] == num:
                return True
        elif col <= self.number - 2:
            if self.positions[row, col + 1] == self.positions[row, col + 2] == num:
                return True
        return False

    def place_num(self, row: int, col: int, numb: int):
        self.positions[row, col] = numb

    def get_empty_positions(self):
        ls = np.array([[-1, -1]], dtype='int8')
        for i in range(self.number):
            for j in range(self.number):
                if self.positions[i][j] == 2:
                    ls = np.append(ls, [[i, j]], axis=0)
        ls = np.delete(ls, 0, 0)
        return ls

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
        temp2 = np.array(temp, dtype='int8')
        return Board(temp2, m)

    def get_lines(self):
        list_of_lines = np.array([list(range(self.number))], dtype='int8')
        for i in range(self.number):
            list_of_lines = np.append(list_of_lines, [self.positions[i]], axis=0)
        list_of_lines = np.delete(list_of_lines, 0, 0)
        return list_of_lines

    def get_columns(self):
        list_of_columns = np.array([list(range(self.number))], dtype='int8')
        for i in range(self.number):
            list_of_column = np.array(list(), dtype='int8')
            for j in range(self.number):
                list_of_column = np.append(list_of_column, self.positions[j][i])
            list_of_columns = np.append(list_of_columns, [list_of_column], axis=0)
        list_of_columns = np.delete(list_of_columns, 0, 0)
        return list_of_columns

    def write(self):
        representation = ''
        for i in range(self.number):
            print(self.positions[i])

    # TODO: outros metodos da classe


class TakuzuState:
    state_id = 0

    # Alterado empty_positions como argumento da criação do takuzu state

    def __init__(self, board: Board, empty: np.array):
        self.board = board
        self.id = TakuzuState.state_id
        self.empty_positions = empty
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def verify_num(self, row: int, col: int, num: int):
        return self.board.search_three_follow_horizontal(row, col, num) and self.board.search_three_follow_vertical(row,
                                                                                                                    col,
                                                                                                                    num)

    def find_obvious_position(self):
        for i in self.empty_positions:
            if self.board.search_three_follow_vertical(i[0], i[1], 0):
                return np.array([i[0], i[1], 1], dtype='int8')
            elif self.board.search_three_follow_horizontal(i[0], i[1], 0):
                return np.array([i[0], i[1], 1], dtype='int8')
            if self.board.search_three_follow_vertical(i[0], i[1], 1):
                return np.array([i[0], i[1], 0], dtype='int8')
            elif self.board.search_three_follow_horizontal(i[0], i[1], 1):
                return np.array([i[0], i[1], 0], dtype='int8')
        return -1

    def find_obvious_positions(self):
        lst_obv_pos = np.array([[-1, -1, -1]], dtype='int8')
        for i in self.empty_positions:
            if self.board.search_three_follow_vertical(i[0], i[1], 0):
                lst_obv_pos = np.append(lst_obv_pos, [[i[0], i[1], 1]], axis=0)
            elif self.board.search_three_follow_horizontal(i[0], i[1], 0):
                lst_obv_pos = np.append(lst_obv_pos, [[i[0], i[1], 1]], axis=0)
            if self.board.search_three_follow_vertical(i[0], i[1], 1):
                lst_obv_pos = np.append(lst_obv_pos, [[i[0], i[1], 0]], axis=0)
            elif self.board.search_three_follow_horizontal(i[0], i[1], 1):
                lst_obv_pos = np.append(lst_obv_pos, [[i[0], i[1], 0]], axis=0)
        lst_obv_pos = np.delete(lst_obv_pos, 0, 0)
        return lst_obv_pos

    def is_full_line(self, line: int):
        list_lines = self.board.get_lines()
        for i in range(self.board.number):
            if list_lines[line][i] == 2:
                return False
        return True

    def is_full_column(self, column: int):
        list_columns = self.board.get_columns()
        for i in range(self.board.number):
            if list_columns[column][i] == 2:
                return False
        return True

    def equal_lines(self):
        for i in range(self.board.number):
            if i+1 <= self.board.number:
                for j in range(self.board.number)[i+1:]:
                    if self.is_full_line(i) and self.is_full_line(j):
                        if np.array_equal(self.board.get_lines()[i], self.board.get_lines()[j]):
                            return True
                    else:
                        return True
        return False

    def equal_columns(self):
        for i in range(self.board.number):
            if i + 1 <= self.board.number:
                for j in range(self.board.number)[i+1:]:
                    if self.is_full_column(i) and self.is_full_column(j):
                        if np.array_equal(self.board.get_columns()[i], self.board.get_columns()[j]):
                            return True
                    else:
                        return True
        return False

    # TODO: outros metodos da classe


class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        empty = board.get_empty_positions()
        state = TakuzuState(board, empty)


    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        array = state.find_obvious_positions()
        if array.is_integer():
            for i in range(state.board.number):
                for j in range(state.board.number):
                    if state.board.positions[i][j] == 2:
                        return np.array([i, j, 1], [i, j, 0], dtype='int8')
        else:
            return array

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        state.board.place_num(action[0], action[1], action[2])
        empty = state.empty
        index = np.argwhere(empty == [action[0], action[1]])
        new_empty = empty.delete(index)
        new_state = TakuzuState(state.board, new_empty)
        return new_state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        if state.equal_lines():
            return False
        if state.equal_columns():
            return False
        number = state.board.number
        board = state.board
        for i in range(number):
            num_1_line = 0
            num_0_line = 0
            num_1_col = 0
            num_0_col = 0
            for j in range(number):
                if board[i][j] == 1:
                    num_1_line += 1
                else:
                    num_0_line += 1
                if board[j][i] == 1:
                    num_1_col += 1
                else:
                    num_0_col += 1
            if (num % 2) == 2:
                if (num_1 != num_0) or (num_1_col != num_0_col):
                    return False
            else:
                if (num_1 >= num_0 + 2) or (num_1_col >= num_0_col + 2):
                    return False
                if (num_1 + 2 <= num_0) or (num_1_col + 2 <= num_0_col + 2):
                    return False
        return True



    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board = Board.parse_instance_from_stdin()
    Tk = Takuzu(board)
    final_state = depth_first_tree_search(Tk)
    final_state.state.board.write()



    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
