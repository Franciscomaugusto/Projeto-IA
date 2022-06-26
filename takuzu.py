# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 12:
# 99218 Francisco Augusto
# 99265 Luis Marques

import sys
import time

import numpy as np

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    depth_first_graph_search,
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
        self.positions = np.copy(structure)
        self.number = n

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.positions[row, col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row == 0:
            lista = [self.positions[row + 1, col],None]
        elif row == self.number-1:
            lista = [None,self.positions[row - 1, col]]
        else:
            lista = [self.positions[row + 1, col], self.positions[row - 1, col]]
        return lista

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        if col == 0:
            lista = [None, self.positions[row, col + 1]]
        elif col == self.number-1:
            lista = [self.positions[row, col - 1], None]
        else:
            lista = [self.positions[row, col - 1], self.positions[row, col + 1]]
        return lista

    def search_three_follow_vertical(self, row: int, col: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers vertically"""
        if self.positions[row,col] == 2:
            return False
        if (row == 0):
            if self.positions[row,col] == self.positions[row + 1, col] == self.positions[row + 2, col]:
                return True
        if row == self.number - 1:
            if self.positions[row,col] == self.positions[row - 1, col] == self.positions[row - 2, col]:
                return True
        if (self.number == 3 and row == 1):
            if self.positions[row,col] ==  self.positions[row - 1, col] == self.positions[row + 1, col]:
                return True
        if(self.number == 3 and row == 2):
            if self.positions[row,col] == self.positions[row - 1, col] == self.positions[row - 2, col]:
                return True
        if self.number > 3 and row == 1:
            if self.positions[row,col] == self.positions[row - 1, col] == \
                    self.positions[row + 1, col] or self.positions[row,col] == self.positions[row + 1, col] == self.positions[row + 2, col]:
                return True
        if(self.number > 3 and row == self.number-2):
           if self.positions[row - 1, col] == self.positions[row + 1, col]== self.positions[row,col] or self.positions[row,col] == self.positions[row - 1, col] == self.positions[row - 2, col]:
               return True
        if self.number > 4 and row in range(self.number)[2:self.number-2]:
            if self.positions[row,col] == self.positions[row - 1, col] == self.positions[row + 1, col] or self.positions[row,col] == self.positions[row + 1, col] == self.positions[row + 2, col] or self.positions[row,col] == self.positions[row - 1, col] == self.positions[row - 2, col]:
                return True
        return False

    def search_three_follow_horizontal(self, row: int, col: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers horizontally"""
        if self.positions[row,col] == 2:
            return False
        if col == 0:
            if self.positions[row,col] ==  self.positions[row , col+1] == self.positions[row, col+2] :
                return True
        if col == self.number - 1:
            if self.positions[row,col] == self.positions[row, col-1] == self.positions[row, col-2]:
                return True
        if (self.number == 3 and col == 1):
            if self.positions[row,col] == self.positions[row, col-1] == self.positions[row, col+1]:
                return True
        if (self.number == 3 and col == 2):
            if self.positions[row,col] == self.positions[row, col-1] == self.positions[row, col - 2]:
                return True
        if self.number > 3 and col == 1:
            if self.positions[row,col] == self.positions[row, col-1] == \
                    self.positions[row, col+1] or self.positions[row,col] == self.positions[row, col+1] == self.positions[row, col+2]:
                return True
        if (self.number > 3 and col == self.number - 2):
            if self.positions[row,col] == self.positions[row , col-1] == \
                    self.positions[row, col+1] or self.positions[row,col] == self.positions[row , col-1] == self.positions[row , col-2]:
                return True
        if self.number > 4 and col in range(self.number)[2:self.number-2]:
            if self.positions[row,col] == self.positions[row, col-1] == self.positions[row, col+1] or self.positions[row,col] == self.positions[row, col+1] == self.positions[row, col+2] or self.positions[row,col] == self.positions[row, col-1] == \
                    self.positions[row, col-2]:
                return True
        return False

    def place_num(self, row: int, col: int, numb: int):
        self.positions[row, col] = numb

    def get_empty_positions(self):
        ls = [[]]
        for i in range(self.number):
            for j in range(self.number):
                if self.positions[i, j] == 2:
                    ls.append([i, j])
        return ls[1:]

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

    def count_num_by_column(self,num:int,column:int):
        l = self.get_columns()[column]
        count = 0
        for i in range(self.number):
            if l[i] == num:
                count = count + 1
        return count

    def count_num_by_lines(self,num:int,line:int):
        l = self.get_lines()[line]
        count = 0
        for i in range(self.number):
            if l[i] == num:
                count = count + 1
        return count

    def count_line(self, num: int):
        list1 = np.array([0],dtype = 'int8')
        number = self.number
        for i in range(number):
            list1 = np.append(list1,[self.count_num_by_lines(num,i)])
        return list1[1:]

    def count_column(self, num: int):
        list1 = np.array([0],dtype = 'int8')
        number = self.number
        for i in range(number):
            list1 = np.append(list1,[self.count_num_by_column(num,i)])
        return list1[1:]

    def three_follow(self, linha: int, coluna: int):
        if self.search_three_follow_vertical(linha, coluna):
            return False
        if self.search_three_follow_horizontal(linha,coluna):
            return False
        return True

    def three_vert(self, row: int, col: int, num: int):
        if row == 0:
            if num == self.positions[row + 1, col] == self.positions[row + 2, col]:
                return False
        if row == self.number - 1:
            if num == self.positions[row - 1, col] == self.positions[row - 2, col]:
                return False
        if self.number == 3 and row == 1:
            if num == self.positions[row - 1, col] == self.positions[row + 1, col]:
                return False
        if self.number == 3 and row == 2:
            if num == self.positions[row - 1, col] == self.positions[row - 2, col]:
                return False
        if self.number > 3 and row == 1:
            if num == self.positions[row - 1, col] == \
                    self.positions[row + 1, col] or num == self.positions[row + 1, col] == \
                    self.positions[row + 2, col]:
                return False
        if self.number > 3 and row == self.number - 2:
            if self.positions[row - 1, col] == self.positions[row + 1, col] == num or \
                    num == self.positions[row - 1, col] == self.positions[row - 2, col]:
                return False
        if self.number > 4 and row in range(self.number)[2:self.number - 2]:
            if num == self.positions[row - 1, col] == self.positions[row + 1, col] or \
                    num == self.positions[row + 1, col] == self.positions[row + 2, col] or \
                    num == self.positions[row - 1, col] == self.positions[row - 2, col]:
                return False
        return True

    def three_horiz(self, row: int, col: int, num: int):
        if col == 0:
            if num == self.positions[row, col + 1] == self.positions[row, col + 2]:
                return False
        if col == self.number - 1:
            if num == self.positions[row, col - 1] == self.positions[row, col - 2]:
                return False
        if self.number == 3 and col == 1:
            if num == self.positions[row, col - 1] == self.positions[row, col + 1]:
                return False
        if self.number == 3 and col == 2:
            if num == self.positions[row, col - 1] == self.positions[row, col - 2]:
                return False
        if self.number > 3 and col == 1:
            if num == self.positions[row, col - 1] == \
                    self.positions[row, col + 1] or num == self.positions[row, col + 1] == \
                    self.positions[row, col + 2]:
                return False
        if self.number > 3 and col == self.number - 2:
            if num == self.positions[row, col - 1] == \
                    self.positions[row, col + 1] or num == self.positions[row, col - 1] == \
                    self.positions[row, col - 2]:
                return False
        if self.number > 4 and col in range(self.number)[2:self.number - 2]:
            if num == self.positions[row, col - 1] == self.positions[row, col + 1] or \
                    num == self.positions[row, col + 1] == self.positions[row, col + 2] or \
                    num == self.positions[row, col - 1] == \
                    self.positions[row, col - 2]:
                return False
        return True

    def write(self):
        linhas = self.get_lines()
        for i in range(self.number - 1):
            print('\t'.join(map(str, linhas[i])))
        print('\t'.join(map(str, linhas[self.number - 1])))


class TakuzuState:
    state_id = 0

    # Alterado empty_positions como argumento da criação do takuzu state

    def __init__(self, board: Board, empty: list, line_0: np.array, line_1: np.array, column_0: np.array, column_1: np.array):
        self.board = board
        self.id = TakuzuState.state_id
        self.empty_positions = empty.copy()
        self.line_0 = np.copy(line_0)
        self.line_1 = np.copy(line_1)
        self.column_0 = np.copy(column_0)
        self.column_1 = np.copy(column_1)
        self.restriction_safe = True
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

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
        return False

    def equal_columns(self):
        for i in range(self.board.number):
            if i + 1 <= self.board.number:
                for j in range(self.board.number)[i+1:]:
                  if self.is_full_column(i) and self.is_full_column(j):
                    if np.array_equal(self.board.get_columns()[i], self.board.get_columns()[j]):
                        return True
        return False

    def place_num_state(self, linha: int, coluna: int, num: int):
        self.board.place_num(linha, coluna, num)
        if not self.verify_restrictions(linha,coluna):
            self.restriction_safe = False
        try:
            del self.empty_positions[self.empty_positions.index([linha, coluna])]
        except ValueError:
            pass
        if num == 0:
            self.line_0[linha] = self.line_0[linha] + 1
            self.column_0[coluna] = self.column_0[coluna] + 1
        if num == 1:
            self.line_1[linha] = self.line_1[linha] + 1
            self.column_1[coluna] = self.column_1[coluna] + 1

    def num_restrict(self, linha: int, coluna: int):
        number = self.board.number
        if number % 2 == 0:
            if self.line_0[linha] == number / 2:
                print('First option', linha, coluna)
                self.place_num_state(linha, coluna, 1)
            elif self.line_1[linha] == self.board.number / 2:
                print('Second option', linha, coluna)
                self.place_num_state(linha, coluna, 0)
            elif self.column_0[coluna] == self.board.number / 2:
                print('Third option', linha, coluna)
                self.place_num_state(linha, coluna, 1)
            elif self.column_1[coluna] == self.board.number / 2:
                print('Fourth option', linha, coluna)
                self.place_num_state(linha, coluna, 0)
        if self.board.number % 2 != 0:
            if self.line_0[linha] == self.board.number / 2 and self.line_1[linha] == self.board.number / 2 + 1:
                print('Fifth option', linha, coluna)
                self.place_num_state(linha, coluna, 1)
            elif self.line_1[linha] == self.board.number / 2 and self.line_0[linha] == self.board.number / 2 + 1:
                print('Sixth option', linha, coluna)
                self.place_num_state(linha, coluna, 0)
            elif self.column_0[coluna] == self.board.number / 2 and self.column_1[coluna] == self.board.number / 2 + 1:
                print('Seventh option', linha, coluna)
                self.place_num_state(linha, coluna, 1)
            elif self.column_1[coluna] == self.board.number / 2 and self.column_0[coluna] == self.board.number / 2 + 1:
                print('Eighth option', linha, coluna)
                self.place_num_state(linha, coluna, 0)

    def put_obv_three(self, linha: int, coluna: int, num: int):
        board = self.board
        if board.three_horiz(linha, coluna, num) and board.three_vert(linha, coluna, num):
            self.place_num_state(linha, coluna, num)

    def count_num_restrict(self, linha: int, coluna: int):
        number = self.board.number
        valor = self.board.positions[linha,coluna]
        if number % 2 == 0:
            if valor == 0:
                if self.line_0[linha] > number / 2:
                    print('Corta ramo: mais 0 linha: ',linha)
                    print(self.line_0[linha],number/2)
                    self.board.write()
                    print('\n')
                    return False
                if self.column_0[coluna] > number / 2:
                    print('Corta ramo: mais 0 coluna ',coluna)
                    print(self.column_0[coluna], number / 2)
                    self.board.write()
                    print('\n')
                    return False
            if valor == 1:
                if self.line_1[linha] > number / 2:
                    print('Corta ramo: mais 1 linha: ',linha)
                    print(self.line_1)
                    print(self.line_1[linha], number / 2)
                    self.board.write()
                    print('\n')
                    return False
                if self.column_1[coluna] > number / 2:
                    print('Corta ramo: mais 1 coluna: ',coluna)
                    print(self.column_1[coluna], number / 2)
                    self.board.write()
                    print('\n')
                    return False
            self.board.write()
            print('goal True:')
            return True
        if number % 2 != 0:
            if valor == 0:
                if self.line_0[linha] >= number / 2 + 2:
                    self.board.write()
                    print('goal false: mais 0')
                    return False
                if self.column_0[coluna] >= number / 2 + 2 :
                    self.board.write()
                    print('goal false: mais 1')
                    return False
            if valor == 1:
                if self.line_1[linha] >= number / 2 + 2 :
                    self.board.write()
                    print('goal false: mais 0')
                    return False
                if self.column_1[coluna] >= number / 2 + 2:
                    self.board.write()
                    print('goal false: mais 1')
                    return False
            self.board.write()
            print('goal True:')
            return True

    def verify_restrictions(self, linha: int, coluna: int):
        board = self.board
        if not board.three_follow(linha,coluna):
            return False
        if self.equal_columns():
            return False
        if self.equal_lines():
            return False
        return True

    def pre_processing(self):
        empty = self.empty_positions
        for pos in empty:
            self.put_obv_three(pos[0], pos[1], 0)
            self.put_obv_three(pos[0], pos[1], 1)


class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        board.write()
        empty = board.get_empty_positions()
        line1 = board.count_line(1)
        print(line1)
        line0 = board.count_line(0)
        print(line0)
        column0 = board.count_column(0)
        print(column0)
        column1 = board.count_column(1)
        print(column1)
        self.initial = TakuzuState(board, empty, line0, line1, column0, column1)


    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        if (type(state) != type(None)):
            if state.restriction_safe:
                for i in range(state.board.number):
                    for j in range(state.board.number):
                        if state.board.positions[i][j] == 2:
                            if i == j == state.board.number-1:
                                print('PREENCHER A ULTIMA\n')
                            return np.array([[i, j, 0], [i, j, 1]], dtype='int8')
            else:
                print('action corta ramo')
                return []
        else:
            raise NotImplementedError

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        new_board = Board(state.board.positions, state.board.number)
        new_state = TakuzuState(new_board, state.empty_positions,state.line_0,state.line_1,state.column_0,state.column_1)
        new_state.place_num_state(action[0],action[1],action[2])


        print('linhas 0',new_state.line_0)
        print('linhas 1',new_state.line_1)
        print('Colunas 0',new_state.column_0)
        print('Colunas 1',new_state.column_1)
        print('\n')
        return new_state



    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        if type(state) != type(None) :
            print(state.state_id)
            print(state.empty_positions)
            state.pre_processing()
            if state.equal_lines():
                print('goal false: linhas')
                return False
            if state.equal_columns():
                print('goal false: colunas')
                return False
            number = state.board.number
            board = state.board

            for i in range(number):
                for j in range(number):
                    if not board.three_follow(i,j):
                        print('goal false: seguidas 0 e 1')
                        return False
                    if not state.count_num_restrict(i,j):
                        return False
            return True
        return False


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    if goal_node is None:
        print("Is goal?\nFalse\n")
    else:
        print('True\n')
        goal_node.state.board.write()
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
