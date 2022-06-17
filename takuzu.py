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
        self.positions = structure
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

    def search_three_follow_vertical(self, row: int, col: int, num: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers vertically"""
        if (row == 0):
            if self.positions[row + 1, col] == self.positions[row + 2, col] == num:
                return True
        if row == self.number - 1:
            if self.positions[row - 1, col] == self.positions[row - 2, col] == num:
                return True
        if (self.number == 3 and row == 1):
            if self.positions[row - 1, col] == self.positions[row + 1, col] == num:
                return True
        if(self.number == 3 and row == 2):
            if self.positions[row - 1, col] == self.positions[row - 2, col] == num:
                return True
        if self.number > 3 and row == 1:
            if self.positions[row - 1, col] == \
                    self.positions[row + 1, col]==num or self.positions[row + 1, col] == self.positions[row + 2, col] == num :
                return True
        if(self.number > 3 and row == self.number-2):
           if self.positions[row - 1, col] == self.positions[row + 1, col]==num or self.positions[row - 1, col] == self.positions[row - 2, col] == num:
               return True

        if self.number > 4 and row in range(self.number)[2:self.number-2]:
            if self.positions[row - 1, col] == self.positions[row + 1, col] == num or self.positions[row + 1, col] == self.positions[row + 2, col] == num or self.positions[row - 1, col] == self.positions[row - 2, col] == num :
                return True
        return False



    def search_three_follow_horizontal(self, row: int, col: int, num: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers horizontally"""
        if col == 0:
            if self.positions[row , col+1] == self.positions[row, col+2] == num:
                return True
        if col == self.number - 1:
            if self.positions[row, col-1] == self.positions[row, col-2] == num:
                return True
        if (self.number == 3 and col == 1):
            if self.positions[row, col-1] == self.positions[row, col+1] == num:
                return True
        if (self.number == 3 and col == 2):
            if self.positions[row, col-1] == self.positions[row, col - 2] == num:
                return True
        if self.number > 3 and col == 1:
            if self.positions[row, col-1] == \
                    self.positions[row, col+1]==num or self.positions[row, col+1] == self.positions[row, col+2] == num :
                return True
        if (self.number > 3 and col == self.number - 2):
            if self.positions[row , col-1] == \
                    self.positions[row, col+1]==num or self.positions[row , col-1] == self.positions[row , col-2] == num :
                return True
        if self.number > 4 and col in range(self.number)[2:self.number-2]:
            if self.positions[row, col-1] == self.positions[row, col+1]==num or self.positions[row, col+1] == self.positions[row, col+2] == num or self.positions[row, col-1] == \
                    self.positions[row, col-2]==num :
                return True
        return False

    def place_num(self, row: int, col: int, numb: int):
        if row != -1:
            self.positions[row, col] = numb

    def get_empty_positions(self):
        ls = [[]]
        for i in range(self.number):
            for j in range(self.number):
                if self.positions[i][j] == 2:
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

    def count_num_by_collumn(self,num:int,column:int):
        l = self.get_columns()[column]
        count = 0
        for i in self.number:
            if l[i] == num:
                count = count + 1
        return count

    def count_num_by_lines(self,num:int,line:int):
        l = self.get_lines()[line]
        count = 0
        for i in self.number:
            if l[i] == num:
                count = count + 1
        return count

    def write(self):
        representation = ''
        for i in range(self.number):
            print(self.positions[i])

    # TODO: outros metodos da classe


class TakuzuState:
    state_id = 0

    # Alterado empty_positions como argumento da criação do takuzu state

    def __init__(self, board: Board, empty: list):
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

    def find_obvious_positions(self):
        lst_obv_pos = [[]]
        empty = self.empty_positions
        for i in empty:
            if(isinstance(i,list)):
                print('obvious:',i)
                if self.number%2 == 0:

                if self.board.search_three_follow_vertical(i[0], i[1], 0):
                    lst_obv_pos.append([i[0], i[1], 1])
                elif self.board.search_three_follow_horizontal(i[0], i[1], 0):
                    lst_obv_pos.append([i[0], i[1], 1])
                if self.board.search_three_follow_vertical(i[0], i[1], 1):
                    lst_obv_pos.append([i[0], i[1], 0])
                elif self.board.search_three_follow_horizontal(i[0], i[1], 1):
                    lst_obv_pos.append([i[0], i[1], 0])
        return lst_obv_pos[1:]



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
        self.initial = TakuzuState(board, empty)


    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        if (type(state) != type(None)):
            array = state.find_obvious_positions()
            if len(array)== 0:
                for i in range(state.board.number):
                    for j in range(state.board.number):
                        if state.board.positions[i][j] == 2:
                            print('return ',state.id,'\n')
                            return np.array([[i, j, 1], [i, j, 0]], dtype='int8')
                return []
            else:
                return array
        else:
            raise NotImplementedError

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        state.board.place_num(action[0], action[1], action[2])
        empty = state.empty_positions
        try:
            del empty[empty.index([action[0], action[1]])]
        except ValueError:
            pass
        state.board.write()
        print('\n')
        new_state = TakuzuState(state.board, empty)
        return new_state



    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        if(type(state) != type(None) ):
            if state.equal_lines():
                print('linha')
                return False
            if state.equal_columns():
                print('coluna')
                return False
            number = state.board.number
            board = state.board
            for i in range(number):
                num_1_line = 0
                num_0_line = 0
                num_1_col = 0
                num_0_col = 0
                for j in range(number):
                    if board.positions[i][j] == 1:
                        num_1_line += 1
                    else:
                        num_0_line += 1
                    if board.positions[j][i] == 1:
                        num_1_col += 1
                    else:
                        num_0_col += 1
                if (number % 2) == 0:
                    if (num_1_line != num_0_line) or (num_1_col != num_0_col):
                        print('1')
                        return False
                else:
                    if (num_1_line >= num_0_line + 2) or (num_1_col >= num_0_col + 2):
                        print('2')
                        return False
                    if (num_1_line + 2 <= num_0_line) or (num_1_col + 2 <= num_0_col + 2):
                        print('3')
                        return False
            return True
        else:
            pass



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
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")

    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass