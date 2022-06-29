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

    def sequencia_de_tres(self, coluna_linha: np.array):
        lista_de_seq = np.array([[0, 0, 0]], dtype='int8')
        number = self.number
        if coluna_linha.size >= 3:
            for i in range(number):
                if i + 3 <= number:
                    lista_de_seq = np.append(lista_de_seq,[coluna_linha[i:i+3]], axis=0)
        lista_de_seq = np.delete(lista_de_seq, 0, 0)
        return lista_de_seq

    def verifica_tripleto(self, coluna_linha: np.array):
        number = self.number
        if number >= 3:
            lista_de_seq = self.sequencia_de_tres(coluna_linha)
            for tripleto in lista_de_seq:
                if tripleto[0] == tripleto[1] == tripleto[2]:
                    return True
        return False

    def tripleto_com_vazio(self, coluna_linha: np.array):
        number = self.number
        lista_tripletos_vazios = np.array([[0, 0, 0, 0]], dtype='int8')
        if number >= 3:
            lista_de_seq = self.sequencia_de_tres(coluna_linha)
            index_inicial = 0
            for tripleto in lista_de_seq:
                if 2 in tripleto:
                    if np.count_nonzero(tripleto == 2) == 1:
                        if tripleto[0] == 2:
                            tripleto = np.append(tripleto, index_inicial)
                        if tripleto[1] == 2:
                            tripleto = np.append(tripleto, index_inicial + 1)
                        if tripleto[2] == 2:
                            tripleto = np.append(tripleto, index_inicial + 2)
                        lista_tripletos_vazios = np.append(lista_tripletos_vazios, [tripleto] ,axis=0)
                index_inicial +=1
            lista_tripletos_vazios = np.delete(lista_tripletos_vazios, 0, 0)
            return lista_tripletos_vazios

    def search_three_follow_vertical(self,col: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers vertically"""
        coluna = self.get_columns()[col]
        return self.verifica_tripleto(coluna)

    def search_three_follow_horizontal(self, row: int):
        """Returns true if the insertion of num leads to a sequence of three equal numbers horizontally"""
        number = self.number
        linha = self.get_lines()[row]
        return self.verifica_tripleto(linha)


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
        list1 = np.array([0], dtype = 'int8')
        number = self.number
        for i in range(number):
            list1 = np.append(list1, [self.count_num_by_column(num, i)])
        return list1[1:]

    def three_follow(self, linha: int, coluna: int):
        if self.search_three_follow_vertical(coluna):
            return False
        if self.search_three_follow_horizontal(linha):
            return False
        return True

    def three_follow_all_board(self):
        for i in range(self.number):
            if self.search_three_follow_vertical(i):
                return False
            if self.search_three_follow_horizontal(i):
                return False
        return True

    def three_vert(self,col: int, num: int):
        number = self.number
        coluna = self.get_columns()[col]
        if number >= 3:
            lista_de_seq = self.sequencia_de_tres(coluna)
            for tripletos in lista_de_seq:
                if tripletos[0] == tripletos[1] == num or tripletos[1] == tripletos[2] == num \
                        or tripletos[0] == tripletos[2] == num:
                    return True
            return False

    def three_horiz(self, row: int, num: int):
        number = self.number
        linha = self.get_lines()[row]
        if number >= 3:
            lista_de_seq = self.sequencia_de_tres(linha)
            for tripletos in lista_de_seq:
                if (tripletos[0] == tripletos[1]) == num or (tripletos[1] == tripletos[2]) == num \
                        or (tripletos[0] == tripletos[2]) == num:
                    return False
            return True

    def consecutive_restraint(self, linha: int, coluna: int):
        number = self.number
        if number >= 3:
            lista_linhas = self.sequencia_de_tres(self.get_lines()[linha])
            lista_col = self.sequencia_de_tres(self.get_columns()[coluna])
            for tripleto in lista_linhas:
                if tripleto[0] == tripleto[1] == tripleto[2] != 2:
                    return False
            for tripleto in lista_col:
                if tripleto[0] == tripleto[1] == tripleto[2] != 2:
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

    def __init__(self, board: Board, empty: list):
        self.board = board
        self.id = TakuzuState.state_id
        self.empty_positions = empty.copy()
        self.restriction_safe = True
        self.placed = True
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
                    if np.array_equal(self.board.get_lines()[i], self.board.get_lines()[j]):
                        return True
        return False

    def equal_columns(self):
        for i in range(self.board.number):
            if i + 1 <= self.board.number:
                for j in range(self.board.number)[i+1:]:
                    if np.array_equal(self.board.get_columns()[i], self.board.get_columns()[j]):
                        return True
        return False

    def full_board(self):
        for i in range(self.board.number):
            if not self.is_full_line(i):
                return False
        return True

    def place_num_state(self, linha: int, coluna: int, num: int):
        try:
            del self.empty_positions[self.empty_positions.index([linha, coluna])]
            self.board.place_num(linha, coluna, num)
            self.placed = True
        except ValueError:
            pass

    """
    def get_full_columns(self):
        number = self.board.number
        full_columns = numpy.zeros(number)
        for i in range(number):
    """

    """
    def put_obv_by_column(self,coluna: int):
        colunas = self.board.get_columns()
        if np.count_nonzero(colunas[coluna] == 2) == 2:
            for coluna_comp in colunas
    """
    def put_obv_three_all(self):
        number = self.board.number
        colunas = self.board.get_columns()
        linhas = self.board.get_lines()
        board_b = self.board
        for i in range(number):
            possible_line = board_b.tripleto_com_vazio(linhas[i])
            possible_col = board_b.tripleto_com_vazio(colunas[i])
            for pos in possible_line:
                if np.count_nonzero(pos == 0) == 2 and pos[3] != 0 or np.count_nonzero(pos == 0) == 3:
                    self.place_num_state(i, pos[3], 1)
                if np.count_nonzero(pos == 1) == 2 and pos[3] != 1 or np.count_nonzero(pos == 1) == 3:
                    self.place_num_state(i, pos[3], 0)
            for pos in possible_col:
                if np.count_nonzero(pos == 0) == 2 and pos[3] != 0 or np.count_nonzero(pos == 0) == 3:
                    self.place_num_state(pos[3], i, 1)
                if np.count_nonzero(pos == 1) == 2 and pos[3] != 1 or np.count_nonzero(pos == 1) == 3:
                    self.place_num_state(pos[3], i, 0)

    def find_index_full_column(self):
        colunas = self.board.get_columns()
        indexs = []
        for i in range(self.board.number):
            if np.count_nonzero(colunas[i] == 2) == 0:
                indexs.append(i)
        return indexs

    def find_index_2_empty_column(self):
        colunas = self.board.get_columns()
        indexs = []
        for i in range(self.board.number):
            if np.count_nonzero(colunas[i] == 2) == 2:
                indexs.append(i)
        return indexs

    def find_index_full_line(self):
        linhas = self.board.get_lines()
        indexs = []
        for i in range(self.board.number):
            if np.count_nonzero(linhas[i] == 2) == 0:
                indexs.append(i)
        return indexs

    def find_index_2_empty_line(self):
        linhas = self.board.get_lines()
        indexs = []
        for i in range(self.board.number):
            if np.count_nonzero(linhas[i] == 2) == 2:
                indexs.append(i)
        return indexs

    def put_column_full(self):
        number = self.board.number
        colunas = self.board.get_columns()
        index_colunas_cheias = self.find_index_full_column()
        index_colunas_2_vazios = self.find_index_2_empty_column()
        estado = 0;
        for i in index_colunas_2_vazios:
            for j in index_colunas_cheias:
                indexs = [[]]
                for index in range(number):
                    if colunas[i][index] != 2 and colunas[j][index] != 2 and colunas[i][index] != colunas[j][index]:
                        indexs = [[]]
                        estado = 0
                        return False
                    if colunas[i][index] == colunas[j][index] != 2 or (
                            colunas[i][index] == 2 and colunas[j][index] != 2) or (
                            colunas[i][index] != 2 and colunas[j][index] == 2):
                        estado = 1
                    if ((colunas[i][index] == 2 and colunas[j][index] != 2) or (
                            colunas[i][index] != 2 and colunas[j][index] == 2)) and estado == 1:
                        indexs.append(index)
                for ind in indexs:
                    self.place_num_state(ind, i)

    def put_line_full(self):
        number = self.board.number
        linhas = self.board.get_lines()
        index_linhas_cheias = self.find_index_full_line()
        index_linhas_2_vazios = self.find_index_2_empty_line()
        estado = 0;
        for i in index_linhas_2_vazios:
            for j in index_linhas_cheias:
                indexs = [[]]
                for index in range(number):
                    if linhas[i][index] != 2 and linhas[j][index] != 2 and linhas[i][index] != linhas[j][index]:
                        indexs = [[]]
                        estado = 0
                        return False
                    if linhas[i][index] == linhas[j][index] != 2 or (
                            linhas[i][index] == 2 and linhas[j][index] != 2) or (
                            linhas[i][index] != 2 and linhas[j][index] == 2):
                        estado = 1
                    if ((linhas[i][index] == 2 and linhas[j][index] != 2) or (
                            linhas[i][index] != 2 and linhas[j][index] == 2)) and estado == 1:
                        indexs.append(index)
                for ind in indexs:
                    self.place_num_state(ind, i)


    def num_restrict_simple(self, linha: int, coluna: int):
        board = self.board
        number = board.number
        linhas = board.get_lines()[linha]
        colunas = board.get_columns()[coluna]
        limit = number // 2 + number % 2
        if np.count_nonzero(linhas == 1) > limit or np.count_nonzero(linhas == 0) > limit:
            return False
        if np.count_nonzero(colunas == 1) > limit or np.count_nonzero(colunas == 0) > limit:
            return False
        return True

    def num_restrict(self):
        board = self.board
        number = board.number
        linhas = board.get_lines()
        colunas = board.get_columns()
        limit = number // 2 + number % 2
        for i in range(number):
            if np.count_nonzero(linhas[i] == 1) > limit or np.count_nonzero(linhas[i] == 0) > limit:
                return False
            if np.count_nonzero(colunas[i] == 1) > limit or np.count_nonzero(colunas[i] == 0) > limit:
                return False
        return True

    def fill_rest_line(self, linha: int):
        board = self.board
        number = board.number
        linhas = board.get_lines()
        empty = self.empty_positions
        line  = linhas[linha]
        if np.count_nonzero( line == 0) == number//2 + number%2:
            for pos in empty:
                if pos[0] == linha:
                    self.place_num_state(pos[0], pos[1], 1)
        if np.count_nonzero( line == 1) == number//2 + number % 2:
            for pos in empty:
                if pos[0] == linha:
                    self.place_num_state(pos[0],pos[1],0)

    def fill_rest_column(self, coluna: int):
        board = self.board
        number = board.number
        empty = self.empty_positions
        colunas = board.get_columns()
        col  = colunas[coluna]
        if np.count_nonzero( col == 0) == number // 2 + number % 2:
            for pos in empty:
                if pos[1] == coluna:
                    self.place_num_state(pos[0], pos[1], 1)
        if np.count_nonzero( col == 1) == number // 2 + number % 2:
            for pos in empty:
                if pos[1] == coluna:
                    self.place_num_state(pos[0], pos[1], 0)


    def verify_restrictions(self):
        if not self.board.three_follow_all_board():
            return False
        if not self.num_restrict():
            return False
        return True

    def pre_processing(self):
        number = self.board.number
        while self.placed:
            self.placed = False
            self.put_obv_three_all()
            if self.restriction_safe:
                for i in range(number):
                    self.fill_rest_line(i)
                for i in range(number):
                    self.fill_rest_column(i)


class Takuzu(Problem):

    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        empty = board.get_empty_positions()
        self.initial = TakuzuState(board, empty)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        if (type(state) != type(None)):
            empty = state.empty_positions
            if state.restriction_safe and len(empty) != 0:
                empty = state.empty_positions
                return [[empty[0][0], empty[0][1], 0], [empty[0][0], empty[0][1], 1]]
            else:
                return []
        else:
            raise NotImplementedError

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_board = Board(state.board.positions, state.board.number)
        new_state = TakuzuState(new_board, state.empty_positions)
        new_state.place_num_state(action[0],action[1],action[2])
        return new_state

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        if type(state) != type(None):
            state.placed = True
            state.pre_processing()
            if len(state.empty_positions) != 0:
                return False
            if not state.verify_restrictions():
                return False
            if len(state.empty_positions) == 0 and state.equal_lines() and state.equal_columns():
                return False
            return True
        return False

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A."""
        node.state.pre_processing()
        num2 = len(node.state.empty_positions)
        total = board.number *board.number
        if node.state.restriction_safe:
            value = total - num2
        else:
            value = 0
        return value
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler tabuleiro do ficheiro 'i1.txt' (Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)
    goal_node = depth_first_tree_search(problem)
    goal_node.state.board.write()

    # Obter o nó solução usando a procura em profundidade:

    pass