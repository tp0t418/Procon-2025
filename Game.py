from copy import deepcopy

from Config import *
from Panel import *
from Field import *
from Connector import *

class Game:
    '''
    Bắt đầu một game:
        problem_field là đề bài, saved_fields lưu field cùng các lượt giải cho đề bài đó
        field được thao tác luôn là field cuối cùng trong saved_field (tức saved_field[-1])
    '''
    def __init__(self):
        self.problem_field = Field(size=8).generate_field()
        self.saved_fields = [deepcopy(self.problem_field)]

    def fetch_problem(self, question_id: str):
        self.problem_field = Field(field=Connector.fetch_problem(question_id))
        self.saved_fields.clear()
        self.make_new_attempt()
    
    def send_answer(self, question_id, answer_id: str):
        if answer_id == "":
            return
        answer_id = int(answer_id)
        Connector.send_answer(question_id, self.saved_fields[answer_id].get_solution())

    def create_problem(self, size) -> Field:
        self.problem_field = Field(size=int(size)).generate_field()
        self.saved_fields.clear()
        self.make_new_attempt()
        return self.problem_field
    
    def get_display_field(self) -> Field:
        return self.saved_fields[-1]

    def make_new_attempt(self):
        self.saved_fields.append(deepcopy(self.problem_field))

    def move(self, x, y, n):
        x = int(x)
        y = int(y)
        n = int(n)
        self.get_display_field().move(x, y, n)

    def show_answers(self):
        print(LogHeader.OKCYAN + "Avaiable answers:")
        for i in range(len(self.saved_fields)):
            print(f"{i}: {self.saved_fields[i].get_steps_amount()} steps & {self.saved_fields[i].count_couples()} couples")

if __name__ == '__main__':
    game = Game()
    panel = Panel(game)
    panel.update_field()
    panel.run()