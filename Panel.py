import tkinter as tk

from Config import *
from Solver import *
from Game import Game

class Panel:
    '''
    Giao diện của solver
        root, left_frame, right_frame: các frame của giao diện
        display_field: tham chiếu tới các entities của field được hiển thị
    Lưu ý:
        Tuyệt đối không thực hiện những thay đổi trực tiếp trên field trong class này
    '''
    CELL_SIZE = 32   # Kích thước mỗi ô vuông (pixel)
    CELL_GAP = 2

    def __init__(self, game: Game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Procon 2025 solver by TheDeath")

        # Chia layout 2 phần
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(0, weight=1)

        # --- Bên trái ---
        self.left_frame = tk.Frame(self.root, bg="#e8e8e8", relief="groove")
        self.left_frame.grid(row = 0, column = 0, sticky="n", padx=10, pady=10)
        self.left_frame.grid_forget()

        # --- Bên phải ---
        self.right_frame = tk.Frame(self.root, padx=10, pady=10)
        self.right_frame.grid(row = 0, column = 1, sticky="ns")

        # Checkbox bật/tắt hiển thị lưới
        self.render_var = tk.BooleanVar(value = False)
        chk_render = tk.Checkbutton(
            self.right_frame,
            text="GUI",
            variable = self.render_var,
            font=("Arial", 11),
            command=self.update_field,
        )
        chk_render.pack(pady = 5)

        # Vùng input
        self.add_message_box("Question ID", "question_id")
        self.add_message_box("Field size (test)", "field_size")
        self.add_message_box("X (column)", "x")
        self.add_message_box("Y (row)", "y")
        self.add_message_box("N (size)", "n")
        self.add_message_box("Answer ID", "answer_id")

        # Vùng input để giao tiếp server
        tk.Button(self.right_frame, text = "Fetch problem", font=("Arial", 12), 
                  command = lambda: self.fetch_problem_btn(self.right_frame.nametowidget("question_id").get())).pack(side = 'top')
        
        tk.Button(self.right_frame, text = "Create problem", font=("Arial", 12), 
                  command = lambda: self.create_problem_btn(self.right_frame.nametowidget("field_size").get())).pack(side = 'top')
        
        tk.Button(self.right_frame, text = "New Attempt", font=("Arial", 12), 
                  command = self.make_new_attempt_btn).pack(side = 'top')
        
        tk.Button(self.right_frame, text = "Make a move", font=("Arial", 12), 
                  command = lambda: self.move_btn(
                      self.right_frame.nametowidget("x").get(),
                      self.right_frame.nametowidget("y").get(),
                      self.right_frame.nametowidget("n").get()
                  )).pack(side = 'top')

        # Vùng nút bấm sinh lời giải tự động
        tk.Label(self.right_frame, text='Solver', font=("Arial", 12, "bold")).pack(pady = 5)

        tk.Button(self.right_frame, text = "Basic solution", font=("Arial", 12), command = Solver.basic_solution).pack(side = 'top')

        # Vùng nút trả lời
        tk.Label(self.right_frame, text='Answer', font=("Arial", 12, "bold")).pack(pady = 5)

        tk.Button(self.right_frame, text = "Show answers", font=("Arial", 12), command = self.game.show_answers).pack(side = 'top')
        tk.Button(self.right_frame, text = "Send answer", font=("Arial", 12), 
                  command = lambda: self.send_answer_btn(
                      self.right_frame.nametowidget("question_id").get(),
                      self.right_frame.nametowidget("answer_id").get()
                  )).pack(side = 'top')

    def create_problem_btn(self, size):
        self.game.create_problem(size)
        self.update_field()

    def make_new_attempt_btn(self):
        self.game.make_new_attempt()
        self.update_field()

    def move_btn(self, x, y, n):
        self.game.move(x, y, n)
        self.update_field()

    def fetch_problem_btn(self, question_id):
        self.game.fetch_problem(question_id)
        self.update_field()

    def send_answer_btn(self, question_id, answer_id):
        self.game.send_answer(question_id, answer_id)
        
    def render_field(self):
        """Render field — tô xanh các ô có ô kề cùng giá trị, còn lại đỏ."""
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        n = len(self.display_field.field)
        field = self.display_field.field

        for r in range(n):
            for c in range(n):
                val = field[r][c]
                same_adjacent = False

                # Kiểm tra 4 hướng kề nhau
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n and field[nr][nc] == val:
                        same_adjacent = True
                        break

                color = "#00cc44" if same_adjacent else "#ff4444"  # xanh nếu có cặp

                lbl = tk.Label(
                    self.left_frame,
                    text=str(val),
                    relief="ridge",
                    borderwidth=1,
                    width=4, height=2,
                    font=("Arial", 12, "bold"),
                    bg=color
                )
                lbl.place(
                    x=c * (Panel.CELL_SIZE + Panel.CELL_GAP),
                    y=r * (Panel.CELL_SIZE + Panel.CELL_GAP),
                    width=Panel.CELL_SIZE,
                    height=Panel.CELL_SIZE
                )

        total_size = n * Panel.CELL_SIZE + (n - 1) * Panel.CELL_GAP
        self.left_frame.config(width=total_size, height=total_size)
        self.left_frame.pack_propagate(False)

    def update_field(self):
        """
        Update giá trị các ô trong lưới và render nếu gui bật (hoặc chỉ render)
        Nếu có field trong tham số thì gán cho display_field
        """
        if not self.render_var.get():
            if self.left_frame.winfo_ismapped():
                self.left_frame.grid_forget()
            return
        
        self.display_field = self.game.get_display_field()
        # Nếu checkbox bật, hiện lại phần lưới
        if not self.left_frame.winfo_ismapped():
            self.left_frame.grid(row = 0, column = 0, sticky="n", padx = 10, pady = 10)

        self.render_field()

    def add_message_box(self, label, box_name):
        '''Thêm 1 message box vào frame, truy cập để lấy giá trị bằng box_name'''
        tk.Label(self.right_frame, text = label, font=("Arial", 12, "bold")).pack(side = "top")
        entry = tk.Entry(self.right_frame, width = 15, font=("Arial", 12), name = box_name, justify = "center")
        entry.pack(side = "top", fill = "x")

    def run(self):
        self.root.mainloop()