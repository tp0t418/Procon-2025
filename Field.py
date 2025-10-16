import random

from Config import *

class Field:
    '''
    Sân đấu:
        size: độ lớn của cạnh
        field: mảng size x size chứa các entity
    '''
    EMPTY = -1
    def __init__(self, size = None, field = None):
        if size is not None:
            self.size = size
            self.field = self.generate_empty_field()
        else:
            self.field = field
            self.size = len(field)
        self.solution = []

    def __len__(self):
        return len(self.field)

    def generate_empty_field(self):
        self.field = [[Field.EMPTY] * self.size for i in range(self.size)]
    
    def generate_field(self):
        numbers = [i for i in range((self.size * self.size) // 2)] * 2
        random.shuffle(numbers)
        self.field = [numbers[i*self.size:(i+1)*self.size] for i in range(self.size)]
        print(LogHeader.OKCYAN + "New field generated!")
        self.print_field()
        return self

    def check_valid_move(self, x, y, n):
        if n < 2 or x < 0 or y < 0 or x + n > self.size or y + n > self.size: return False
        return True

    def move(self, x, y, n):
        '''
        Di chuyển nếu hợp lệ và add nước đi vào solution
        '''
        if not self.check_valid_move(x, y, n):
            print(LogHeader.FAIL + f"Invalid move ({x}, {y}, {n})")
            return -1

        sub = [row[x:x+n] for row in self.field[y:y+n]]

        # Xoay ma trận con 90 độ
        rotated = [list(row) for row in zip(*sub[::-1])]

        # Ghi đè trở lại vị trí cũ
        for i in range(n):
            for j in range(n):
                self.field[y + i][x + j] = rotated[i][j]

        self.solution.append({"x": x, "y": y, "n": n})
        # self.print_field()

    def count_couples(self):
        '''
        Đếm số cặp đôi trong field
        '''
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if j + 1 < self.size and self.field[i][j] == self.field[i][j + 1]:
                    count += 1
                if i + 1 < self.size and self.field[i][j] == self.field[i + 1][j]:
                    count += 1

        return count

    def get_solution(self):
        return self.solution

    def get_steps_amount(self):
        return len(self.solution)

    def print_field(self):
        print('-' * 100)
        for i in range(self.size):
            for j in range(self.size):
                print('%d\t' % self.field[i][j], end='')
            print()
        print('-' * 100)
