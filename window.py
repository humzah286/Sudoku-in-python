from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QStackedWidget, QVBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtCore import QTimer, QSize
import sys
import sudoku
from os.path import exists
import time

solution = [ [0 for c in range(0,9)] for r in range(0, 9) ]
puzzle = []

assigned = [ [False for c in range(0,9)] for r in range(0, 9) ]
saved_answer = [0]
saved_row = [-1]
saved_col = [-1]

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.pause_time = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_timer)
        self.setWindowTitle("sudoku")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedHeight(700)
        self.setFixedWidth(550)
        self.setContentsMargins(0,0,0,0)
        self.stackedWidget =  QStackedWidget()        
        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.firstPageWidget =  QWidget()
        self.secondPageWidget =  QWidget()
        self.stackedWidget.addWidget(self.firstPageWidget)
        self.stackedWidget.addWidget(self.secondPageWidget)
        self.setStyleSheet("background-color: white")
        image = QImage('title.PNG')
        label_logo = QLabel(self.firstPageWidget)
        label_logo.setGeometry(60, 100, 400, 150)
        label_logo.setPixmap(QPixmap(image).scaledToWidth(400))
        label_logo.show()
        btn = QPushButton("Start", self.firstPageWidget)
        btn.setGeometry(210, 500, 100, 50)
        btn.clicked.connect(self.clicked_btn)
        btn.setStyleSheet('''width: 100px;
            height: 50px;
            border-radius: 15px;
            border: 3px solid black;
            font-family: sans-serif;
            font-size: 20px;
            font-weight: bold;
            background-color: lightblue; ''')
        btn.show()
        self.label_best_score =  QLabel(self.firstPageWidget)
        self.label_best_score.setGeometry(170, 300, 220, 50)
        self.label_best_score.setStyleSheet("font-family: sans-serif; font-size: 25px;")
        self.label_games_won =  QLabel(self.firstPageWidget)
        self.label_games_won.setGeometry(170, 380, 220, 50)
        self.label_games_won.setStyleSheet("font-family: sans-serif; font-size: 25px;")
        if not exists("record.txt"): 
            f = open("record.txt", "w")
            f.write("0\n0")
            f.close()
            
        f = open("record.txt", "r")
        self.bestScore = int(f.readline())
        self.gamesWon = int(f.readline())
        f.close()
        self.set_records()
        # first page finished
        
        # time label placement
        self.show_time = QLabel(self.secondPageWidget)
        self.show_time.setGeometry(400, 15, 100, 50)
        self.setStyleSheet("color: black; background-color: white; font-size: 25px;")
        
        # border_lines are lines for enclosing entire grid
        
        border_lines = [QWidget(self.secondPageWidget) for i in range(0,4)]
        
        border_lines[0].setGeometry(50,100,424,3)   # top side
        border_lines[1].setGeometry(50,100,3,424)   # left side
        border_lines[2].setGeometry(470,100,3,424)  # right side
        border_lines[3].setGeometry(50, 520, 424, 3) # bottom side
        
        for i in range(0, 4):  border_lines[i].setStyleSheet("background-color: black")
        
        # horizontal lines for separation in between main lines
        
        main_vertical_lines = [QWidget(self.secondPageWidget) for i in range(0,2)]
        
        main_vertical_lines[0].setGeometry(190, 100, 3, 422) 
        main_vertical_lines[1].setGeometry(330, 100, 3, 422) 
               
        for i in range(0, 2):  main_vertical_lines[i].setStyleSheet("background-color: black")
        
        # horizontal lines for separation in between main lines
        
        main_horizontal_lines = [QWidget(self.secondPageWidget) for i in range(0,2)]
        
        main_horizontal_lines[0].setGeometry(50, 240, 422,3)
        main_horizontal_lines[1].setGeometry(50, 380, 422,3)
        
        for i in range(0, 2):  main_horizontal_lines[i].setStyleSheet("background-color: black")
        
        # internal_vertical_lines are for lines in between main lines
        internal_vertical_lines = [QWidget(self.secondPageWidget) for i in range(0,6)]
        
        row_gap = 98
        for i in range(0, 6): 
            if i>0 and i%2 == 0: row_gap += 48
            internal_vertical_lines[i].setGeometry(row_gap, 100, 1, 422)
            internal_vertical_lines[i].setStyleSheet("background-color: black")
            row_gap += 45 + 1
        
        # internal_horizontal_lines are for lines in between main lines
        internal_horizontal_lines = [QWidget(self.secondPageWidget) for i in range(0,6)]
        
        col_gap = 148
        for i in range(0, 6): 
            if i>0 and i%2 == 0: col_gap += 48
            internal_horizontal_lines[i].setGeometry(50, col_gap, 422, 1)
            internal_horizontal_lines[i].setStyleSheet("background-color: black")
            col_gap += 45 + 1
        
        # code for buttons
        self.puzzle_buttons = [[QPushButton("9", self.secondPageWidget) for i in range(0,9)] for j in range(0,9)]
        
        gap_col = 0
        for j in range(0, 9): 
            gap_row = 0
            if j%3 == 0: gap_col += 2
            for i in range(0, 9): 
                if i%3 == 0: gap_row += 2
                self.puzzle_buttons[j][i].setGeometry( 51 + i*45 + gap_row, 101 + j*45 + gap_col, 45 , 45)
                self.puzzle_buttons[j][i].setStyleSheet("background-color: white; font-family: sans-serif; font-size: 25px; border: 1px solid black;")
                # self.puzzle_buttons[j][i].clicked.connect(lambda: self.puzzle_button_clicked(j, i))
                gap_row += 1
            gap_col += 1
        
        self.puzzle_buttons[0][0].clicked.connect(lambda: self.puzzle_button_clicked(0, 0))
        
        # answer button placement
        self.answer = [QPushButton("9", self.secondPageWidget) for i in range(0,9)]
        
        answer_gap = 42
        for i in range(0, 9): 
            self.answer[i].setText(str(i+1))
            self.answer[i].setGeometry(answer_gap, 575, 40, 40)
            self.answer[i].setStyleSheet("background-color: white; border: 4px solid black; font-family: sans-serif; font-size: 22px;")
            answer_gap += 50
        
        self.set_connections()
        
        # pause_btn 
        self.pause_btn = QPushButton("", self.secondPageWidget)
        self.pause_btn.setGeometry(50, 15, 60, 60)
        self.pause_btn.setIcon(QIcon("pause.png"))
        self.pause_btn.setIconSize(QSize(60, 60))
        self.pause_btn.clicked.connect(self.pause_game)
        self.pause_btn.show()
        self.pause_btn.setStyleSheet("background-color: white;font-family: sans-serif; font-size: 30px;")

        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
        self.stackedWidget.setCurrentIndex(0)
        self.secondPageWidget.setStyleSheet('margin: 0; padding: 0px; background-color: white; ')
        self.firstPageWidget.setStyleSheet('margin: 0; padding: 0px; background-color: white; ')
        
        # pause screen
        self.pause_screen = QLabel(self.secondPageWidget)
        self.pause_screen.setGeometry(0, 99, 550, 600)
        self.pause_screen.setStyleSheet("background-color: white;")
        self.pause_screen.hide()
        
        # resume button
        self.resume_btn = QPushButton(self.secondPageWidget)
        self.resume_btn.setIcon(QIcon("resume.jpg"))
        self.resume_btn.setGeometry(235,320,60, 60)
        self.resume_btn.setIconSize(QSize(60, 60))
        self.resume_btn.clicked.connect(self.resume_game)
        self.resume_btn.hide()
        
        # mistakes label
        self.mistakes_label = QLabel(self.secondPageWidget)
        self.mistakes_label.setGeometry(180, 15, 200, 50)
        self.mistakes_label.setText("Mistakes : 0/5")
        self.mistakes_label.setStyleSheet("background-color: white;font-family: sans-serif; font-size: 25px;")

    def clicked_btn(self): 
        self.stackedWidget.setCurrentIndex(1)
        sudoku.fillGrid(solution)
        temp = [ [0 for c in range(0,9)] for r in range(0, 9) ]

        for i in range(0,9): 
            for j in range(0, 9): temp[i][j] = solution[i][j]
            
        puzzle = sudoku.generate_puzzle(temp, 1)
        for j in range(0,9): 
            for i in range(0, 9): 
                if puzzle[j][i] != 0:
                    self.puzzle_buttons[j][i].setText(str(puzzle[j][i]))
                    assigned[j][i] = True
                else: 
                    self.puzzle_buttons[j][i].setText("")
        
        for j in range(0, 9): self.answer[j].show()
        
        self.start_time = time.time()
        self.pause_time = 0           
        self.timer.start(1000)
        self.mistakes = 0
        self.mistakes = 0
        self.mistakes_label.setText("Mistakes : 0/5")
    
    def reset_button_color(self): 
        for i in range(0, 9): 
            for j in range(0, 9): 
                self.puzzle_buttons[i][j].setStyleSheet("background-color: white; font-family: sans-serif; font-size: 25px; border: 1px solid black;")
                
    def color_button(self, j, i): 
        for x in range(0 ,9): 
            self.puzzle_buttons[j][x].setStyleSheet("background-color: rgb(215, 215, 215); font-family: sans-serif; font-size: 25px; border: 1px solid black;")
            self.puzzle_buttons[x][i].setStyleSheet("background-color: rgb(215, 215, 215); font-family: sans-serif; font-size: 25px; border: 1px solid black;")
        
        box_row = (j//3)*3
        box_col = (i//3)*3
        
        for x in range(box_col, box_col+3): 
            for y in range(box_row, box_row+3):
                self.puzzle_buttons[y][x].setStyleSheet("background-color: rgb(215, 215, 215); font-family: sans-serif; font-size: 25px; border: 1px solid black;")
                
        self.puzzle_buttons[j][i].setStyleSheet("background-color: rgb(182, 211, 241); font-family: sans-serif; font-size: 25px; border: 1px solid black;")
        
        for x in range(0, 9): 
            for y in range(0, 9): 
                if self.puzzle_buttons[x][y].text() != "" and self.puzzle_buttons[j][i].text() == self.puzzle_buttons[x][y].text(): 
                    self.puzzle_buttons[x][y].setStyleSheet("background-color: rgb(182, 211, 241); font-family: sans-serif; font-size: 25px; border: 1px solid black;")
                            
    def puzzle_button_clicked(self, j, i):
        self.reset_button_color() 
        self.color_button(j,i)
        
        saved_row[0] = j
        saved_col[0] = i
        
    def set_connections(self): 
        self.puzzle_buttons[0][0].clicked.connect(lambda: self.puzzle_button_clicked(0, 0))
        self.puzzle_buttons[0][1].clicked.connect(lambda: self.puzzle_button_clicked(0, 1))
        self.puzzle_buttons[0][2].clicked.connect(lambda: self.puzzle_button_clicked(0, 2))
        self.puzzle_buttons[0][3].clicked.connect(lambda: self.puzzle_button_clicked(0, 3))
        self.puzzle_buttons[0][4].clicked.connect(lambda: self.puzzle_button_clicked(0, 4))
        self.puzzle_buttons[0][5].clicked.connect(lambda: self.puzzle_button_clicked(0, 5))
        self.puzzle_buttons[0][6].clicked.connect(lambda: self.puzzle_button_clicked(0, 6))
        self.puzzle_buttons[0][7].clicked.connect(lambda: self.puzzle_button_clicked(0, 7))
        self.puzzle_buttons[0][8].clicked.connect(lambda: self.puzzle_button_clicked(0, 8))
        self.puzzle_buttons[1][0].clicked.connect(lambda: self.puzzle_button_clicked(1, 0))
        self.puzzle_buttons[1][1].clicked.connect(lambda: self.puzzle_button_clicked(1, 1))
        self.puzzle_buttons[1][2].clicked.connect(lambda: self.puzzle_button_clicked(1, 2))
        self.puzzle_buttons[1][3].clicked.connect(lambda: self.puzzle_button_clicked(1, 3))
        self.puzzle_buttons[1][4].clicked.connect(lambda: self.puzzle_button_clicked(1, 4))
        self.puzzle_buttons[1][5].clicked.connect(lambda: self.puzzle_button_clicked(1, 5))
        self.puzzle_buttons[1][6].clicked.connect(lambda: self.puzzle_button_clicked(1, 6))
        self.puzzle_buttons[1][7].clicked.connect(lambda: self.puzzle_button_clicked(1, 7))
        self.puzzle_buttons[1][8].clicked.connect(lambda: self.puzzle_button_clicked(1, 8))
        self.puzzle_buttons[2][0].clicked.connect(lambda: self.puzzle_button_clicked(2, 0))
        self.puzzle_buttons[2][1].clicked.connect(lambda: self.puzzle_button_clicked(2, 1))
        self.puzzle_buttons[2][2].clicked.connect(lambda: self.puzzle_button_clicked(2, 2))
        self.puzzle_buttons[2][3].clicked.connect(lambda: self.puzzle_button_clicked(2, 3))
        self.puzzle_buttons[2][4].clicked.connect(lambda: self.puzzle_button_clicked(2, 4))
        self.puzzle_buttons[2][5].clicked.connect(lambda: self.puzzle_button_clicked(2, 5))
        self.puzzle_buttons[2][6].clicked.connect(lambda: self.puzzle_button_clicked(2, 6))
        self.puzzle_buttons[2][7].clicked.connect(lambda: self.puzzle_button_clicked(2, 7))
        self.puzzle_buttons[2][8].clicked.connect(lambda: self.puzzle_button_clicked(2, 8))
        self.puzzle_buttons[3][0].clicked.connect(lambda: self.puzzle_button_clicked(3, 0))
        self.puzzle_buttons[3][1].clicked.connect(lambda: self.puzzle_button_clicked(3, 1))
        self.puzzle_buttons[3][2].clicked.connect(lambda: self.puzzle_button_clicked(3, 2))
        self.puzzle_buttons[3][3].clicked.connect(lambda: self.puzzle_button_clicked(3, 3))
        self.puzzle_buttons[3][4].clicked.connect(lambda: self.puzzle_button_clicked(3, 4))
        self.puzzle_buttons[3][5].clicked.connect(lambda: self.puzzle_button_clicked(3, 5))
        self.puzzle_buttons[3][6].clicked.connect(lambda: self.puzzle_button_clicked(3, 6))
        self.puzzle_buttons[3][7].clicked.connect(lambda: self.puzzle_button_clicked(3, 7))
        self.puzzle_buttons[3][8].clicked.connect(lambda: self.puzzle_button_clicked(3, 8))
        self.puzzle_buttons[4][0].clicked.connect(lambda: self.puzzle_button_clicked(4, 0))
        self.puzzle_buttons[4][1].clicked.connect(lambda: self.puzzle_button_clicked(4, 1))
        self.puzzle_buttons[4][2].clicked.connect(lambda: self.puzzle_button_clicked(4, 2))
        self.puzzle_buttons[4][3].clicked.connect(lambda: self.puzzle_button_clicked(4, 3))
        self.puzzle_buttons[4][4].clicked.connect(lambda: self.puzzle_button_clicked(4, 4))
        self.puzzle_buttons[4][5].clicked.connect(lambda: self.puzzle_button_clicked(4, 5))
        self.puzzle_buttons[4][6].clicked.connect(lambda: self.puzzle_button_clicked(4, 6))
        self.puzzle_buttons[4][7].clicked.connect(lambda: self.puzzle_button_clicked(4, 7))
        self.puzzle_buttons[4][8].clicked.connect(lambda: self.puzzle_button_clicked(4, 8))
        self.puzzle_buttons[5][0].clicked.connect(lambda: self.puzzle_button_clicked(5, 0))
        self.puzzle_buttons[5][1].clicked.connect(lambda: self.puzzle_button_clicked(5, 1))
        self.puzzle_buttons[5][2].clicked.connect(lambda: self.puzzle_button_clicked(5, 2))
        self.puzzle_buttons[5][3].clicked.connect(lambda: self.puzzle_button_clicked(5, 3))
        self.puzzle_buttons[5][4].clicked.connect(lambda: self.puzzle_button_clicked(5, 4))
        self.puzzle_buttons[5][5].clicked.connect(lambda: self.puzzle_button_clicked(5, 5))
        self.puzzle_buttons[5][6].clicked.connect(lambda: self.puzzle_button_clicked(5, 6))
        self.puzzle_buttons[5][7].clicked.connect(lambda: self.puzzle_button_clicked(5, 7))
        self.puzzle_buttons[5][8].clicked.connect(lambda: self.puzzle_button_clicked(5, 8))
        self.puzzle_buttons[6][0].clicked.connect(lambda: self.puzzle_button_clicked(6, 0))
        self.puzzle_buttons[6][1].clicked.connect(lambda: self.puzzle_button_clicked(6, 1))
        self.puzzle_buttons[6][2].clicked.connect(lambda: self.puzzle_button_clicked(6, 2))
        self.puzzle_buttons[6][3].clicked.connect(lambda: self.puzzle_button_clicked(6, 3))
        self.puzzle_buttons[6][4].clicked.connect(lambda: self.puzzle_button_clicked(6, 4))
        self.puzzle_buttons[6][5].clicked.connect(lambda: self.puzzle_button_clicked(6, 5))
        self.puzzle_buttons[6][6].clicked.connect(lambda: self.puzzle_button_clicked(6, 6))
        self.puzzle_buttons[6][7].clicked.connect(lambda: self.puzzle_button_clicked(6, 7))
        self.puzzle_buttons[6][8].clicked.connect(lambda: self.puzzle_button_clicked(6, 8))
        self.puzzle_buttons[7][0].clicked.connect(lambda: self.puzzle_button_clicked(7, 0))
        self.puzzle_buttons[7][1].clicked.connect(lambda: self.puzzle_button_clicked(7, 1))
        self.puzzle_buttons[7][2].clicked.connect(lambda: self.puzzle_button_clicked(7, 2))
        self.puzzle_buttons[7][3].clicked.connect(lambda: self.puzzle_button_clicked(7, 3))
        self.puzzle_buttons[7][4].clicked.connect(lambda: self.puzzle_button_clicked(7, 4))
        self.puzzle_buttons[7][5].clicked.connect(lambda: self.puzzle_button_clicked(7, 5))
        self.puzzle_buttons[7][6].clicked.connect(lambda: self.puzzle_button_clicked(7, 6))
        self.puzzle_buttons[7][7].clicked.connect(lambda: self.puzzle_button_clicked(7, 7))
        self.puzzle_buttons[7][8].clicked.connect(lambda: self.puzzle_button_clicked(7, 8))
        self.puzzle_buttons[8][0].clicked.connect(lambda: self.puzzle_button_clicked(8, 0))
        self.puzzle_buttons[8][1].clicked.connect(lambda: self.puzzle_button_clicked(8, 1))
        self.puzzle_buttons[8][2].clicked.connect(lambda: self.puzzle_button_clicked(8, 2))
        self.puzzle_buttons[8][3].clicked.connect(lambda: self.puzzle_button_clicked(8, 3))
        self.puzzle_buttons[8][4].clicked.connect(lambda: self.puzzle_button_clicked(8, 4))
        self.puzzle_buttons[8][5].clicked.connect(lambda: self.puzzle_button_clicked(8, 5))
        self.puzzle_buttons[8][6].clicked.connect(lambda: self.puzzle_button_clicked(8, 6))
        self.puzzle_buttons[8][7].clicked.connect(lambda: self.puzzle_button_clicked(8, 7))
        self.puzzle_buttons[8][8].clicked.connect(lambda: self.puzzle_button_clicked(8, 8))
        
        self.answer[0].clicked.connect(lambda: self.answer_button_clicked(0))
        self.answer[1].clicked.connect(lambda: self.answer_button_clicked(1))
        self.answer[2].clicked.connect(lambda: self.answer_button_clicked(2))
        self.answer[3].clicked.connect(lambda: self.answer_button_clicked(3))
        self.answer[4].clicked.connect(lambda: self.answer_button_clicked(4))
        self.answer[5].clicked.connect(lambda: self.answer_button_clicked(5))
        self.answer[6].clicked.connect(lambda: self.answer_button_clicked(6))
        self.answer[7].clicked.connect(lambda: self.answer_button_clicked(7))
        self.answer[8].clicked.connect(lambda: self.answer_button_clicked(8))
        
    def answer_button_clicked(self, i): 
        for x in range(0, 9): 
            self.answer[x].setStyleSheet("background-color: white; border: 4px solid black; font-family: sans-serif; font-size: 22px;")
        self.answer[i].setStyleSheet("background-color: white; border: 4px solid #60bcff; font-family: sans-serif; font-size: 22px;")
        saved_answer[0] = i + 1
        self.check_answer()
        
    def check_answer(self): 
        if saved_row[0] == -1 or saved_col[0] == -1:
            msgBox = QMessageBox()
            msgBox.setText("No element selected from the grid!")
            msgBox.setWindowTitle("Error!")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            x = msgBox.exec()
            return
            
        if assigned[saved_row[0]][saved_col[0]]: 
            msgBox = QMessageBox()
            # msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("The element has already a number assigned!")
            msgBox.setWindowTitle("Error!")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.exec()
            return
        
        if saved_answer[0] == solution[saved_row[0]][saved_col[0]]:
            assigned[saved_row[0]][saved_col[0]] = True
            self.puzzle_buttons[saved_row[0]][saved_col[0]].setText(str(saved_answer[0]))
            self.reset_button_color()
            count_entries = []
            complete = True
            for i in range(0, 9): 
                for j in range(0,9): 
                    if not assigned[i][j]: complete = False
                    if self.puzzle_buttons[i][j].text() == str(saved_answer[0]): count_entries.append(saved_answer[0])
            if len(count_entries) == 9: 
                self.answer[saved_answer[0]-1].hide()
            if complete: 
                self.if_finished()
            saved_row[0] = -1
            saved_col[0] = -1
        else: 
            self.mistakes += 1
            self.mistakes_label.setText("Mistakes : " + str(self.mistakes) + "/5")
            if (self.mistakes == 5): 
                self.timer.stop()
                msgBox = QMessageBox()
                msgBox.setText("Game Over! You have made 5 mistakes")
                msgBox.setWindowTitle("You Lost!")
                msgBox.setIcon(QMessageBox.Icon.Critical)
                msgBox.exec()
                self.stackedWidget.setCurrentIndex(0)  
                return
                
            msgBox = QMessageBox()
            msgBox.setText("Wrong element selected!")
            msgBox.setWindowTitle("Error!")
            msgBox.setIcon(QMessageBox.Icon.Critical)
            msgBox.exec()
            return
            
    def pause_game(self): 
        self.pause_start = time.time()
        self.pause_screen.show()
        self.resume_btn.show()
        self.pause_btn.hide()
        self.timer.stop()
        
    def resume_game(self):
        self.pause_end = time.time()
        self.pause_time += int(self.pause_end - self.pause_start)
        self.timer.start(1000)
        self.pause_screen.hide()
        self.resume_btn.hide()
        self.pause_btn.show()
        
    def if_finished(self): 
        self.timer.stop()
        msgBox = QMessageBox()
        msgBox.setText("You have completed the puzzle!")
        msgBox.setWindowTitle("Congratulations!")
        msgBox.setIcon(QMessageBox.Icon.NoIcon)
        msgBox.exec()
        self.stackedWidget.setCurrentIndex(0)  
        if self.diff < self.bestScore: 
            self.bestScore = self.diff
        self.gamesWon += 1
        f = open("record.txt", "w")
        f.write(str(self.bestScore) + "\n" + str(self.gamesWon))
        f.close()
        self.set_records()
             
    def start_timer(self): 
        self.end_time = time.time()
        self.diff = int(self.end_time - self.start_time)
        self.diff -= self.pause_time
        self.show_time.setText(time_int_to_string((self.diff)))

    def set_records(self): 
        if self.bestScore == 0: 
            self.label_best_score.setText("Best Score = None")
        else: 
            self.label_best_score.setText("Best Score : " + time_int_to_string(self.bestScore))
            
        self.label_games_won.setText("Games won : " + str(self.gamesWon))
        

def time_int_to_string(i): 
    str1 = ""
    if i >= 3600: 
        str1 += "0" + str(i//3600) + ":"
        
    if not ((i//60)%60 >= 10): 
        str1 += "0" + str((i//60)%60) + ":"
    else: 
        str1 += str((i//60)%60) + ":"
        
    if not (i%60 >= 10):
        str1 += "0" + str(i%60)
    else: 
        str1 += str(i%60)
        
    return str1
    
    
app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())


