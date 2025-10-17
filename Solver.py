from Config import *
from Game import Game

class Solver:
    def basic_solution(game: Game):
        field = game.get_display_field().field
        size = len(field)

        def find_couple(r, c):
            for i in range(c+1, size):
                if field[r][c] == field[r][i]:
                    return r, i
            
            for i in range(r+1, size):
                for j in range(size):
                    if field[r][c] == field[i][j]:
                        return i, j 

        '''
        Cách giải chắc chắn 100% cặp đôi đúng cho mọi đề bài theo trình tự sau:
        + Xử lý từ hàng đầu tiên đến hàng n-2 bằng cách xếp từng cặp
        + Xử lý 2 hàng còn lại bằng cách xếp từng cặp theo cột
        + Xử lý 4 ô cuối
        '''
        print(LogHeader.OKCYAN + "Solving with basic solution...")

        ### Phase 1: Xử lý từ hàng đầu tiên đến hàng n-2 bằng cách xếp từng cặp
        for row in range(size - 2):
            for col in range(0, size, 2):
                # Nếu đã có sẵn cặp rồi thì next sang cặp khác
                if field[row][col] == field[row][col+1]:
                    continue
                # Tìm vị trí ô cặp đôi
                target_row, target_col = find_couple(row, col)
                
                # Đưa về cùng cột nếu trái/phải dưới
                ## TODO: thêm trường hợp đưa về cùng hàng
                if col != target_col and row != target_row:
                    # Trường hợp 1: trái dưới
                    if target_col < col:
                        # Kiểm tra ô cần tìm có sát rìa dưới, nếu có thì nhấc lên
                        if target_row == size - 1:
                            yield game.move(target_col, target_row - 1, 2)
                            target_row -= 1
                        # Xác định mảnh lớn nhất có thể dùng
                        max_distance = min(col - target_col + 1, size - target_row)
                        # Dùng mảnh lớn nhất có thể để đưa ô cần tìm sang phải
                        while (col - target_col + 1 >= max_distance):
                            yield game.move(target_col, target_row, max_distance)
                            target_col += max_distance - 1
                        # Nếu ô cần tìm vẫn chưa ở cùng cột với ô cặp đôi thì dùng mảnh nhỏ hơn đưa vào 
                        if col - target_col != 0:
                            yield game.move(target_col, target_row, col - target_col + 1)
                        target_col = col

                    # Trường hợp 2: phải dưới
                    else:
                        # Kiểm tra hàng 2 cặp là liên tiếp thì đưa ô cần tìm xuống dưới
                        if target_row - row == 1:
                            yield game.move(target_col - 1, target_row, 2)
                            target_row += 1
                        # Xác định mảnh lớn nhất có thể dùng
                        max_distance = min(target_col - col + 1, target_row - row)
                        # Dùng mảnh lớn nhất có thể để đưa ô cần tìm sang trái
                        while (target_col - col + 1 >= max_distance):
                            yield game.move(target_col - max_distance + 1, target_row - max_distance + 1, max_distance)
                            target_col = target_col - max_distance + 1
                        # Nếu ô cần tìm vẫn chưa ở cùng cột với ô cặp đôi thì dùng mảnh nhỏ hơn đưa vào 
                        if target_col - col != 0:
                            yield game.move(col, target_row - (target_col - col + 1) + 1, target_col - col + 1)
                            target_col = col
            
                ## Trường hợp 3: cùng hàng
                if target_row == row:
                    # Xác định mảnh lớn nhất có thể dùng
                    max_distance = min(target_col - col, size - row)
                    # Đưa ô cần tìm xuống phía dưới
                    yield game.move(target_col - max_distance + 1, row, max_distance)
                    # Cập nhật hàng
                    target_row += max_distance - 1 
                    # Dùng mảnh lớn nhất có thể để đưa ô cần tìm sang trái
                    while (target_col - col >= max_distance):
                        yield game.move(target_col - max_distance + 1, row, max_distance)
                        target_col = target_col - max_distance + 1
                    # Nếu ô cần tìm vẫn chưa ở ngay dưới vị trí đặt thì dùng mảnh nhỏ hơn đưa vào 
                    if target_col - col > 1:
                        yield game.move(col + 1, target_row - (target_col - col) + 1, target_col - col)
                    # Đưa ô cần tìm vào đúng vị trí
                    yield game.move(col + 1, row, max_distance)

                # Trường hợp 4: cùng cột
                else:
                    # Xác định mảnh lớn nhất có thể dùng
                    max_distance = min(size - col, target_row - row)
                    if max_distance == 1:
                        yield game.move(col, row, 2)
                        continue
                    # Đưa ô cần tìm lên trên, sát ô cặp đôi
                    while (target_row - row >= max_distance):
                        yield game.move(col, target_row - max_distance + 1, max_distance)
                        target_row = target_row - max_distance + 1
                    # Nếu ô cần tìm vẫn chưa ở ngay dưới ô cặp đôi thì dùng mảnh nhỏ hơn đưa vào 
                    if target_row - row > 1:
                        yield game.move(col, row + 1, target_row - row)
                    # Dùng mảnh 2x2 xếp cặp vào vị trí đúng
                    yield game.move(col, row, 2)

        print(LogHeader.OKGREEN + "Done!")

    def naive_solution(game: Game):
        '''
        Cách giải xét tất cả nước đi có thể:
        + Tìm nước đi cải thiện số lượng cặp liền kề nhiều nhất
        + Lặp đến khi không thể cải thiện nữa
        '''
        pass

    def physic_solution(game: Game):
        '''
        Cách giải áp dụng vật lý:
        + Tưởng tượng sân đấu là một bể nước
        + Tìm tất cả nước đi có thể rồi tính trọng tâm của vật được tạo bởi nước đi đó
        + Xoay sao cho không còn vật nào có trọng tâm "hướng lên trên"
        '''
        pass