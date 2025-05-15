from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QDialog, QLineEdit, QComboBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("МастерПол")
        self.setWindowIcon(QIcon("Мастер пол.png"))
        self.resize(500, 500)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        logo_label = QLabel()
        logo_pixmap = QPixmap("Мастер пол.png")
        logo_pixmap = logo_pixmap.scaled(50,50)
        logo_label.setPixmap(logo_pixmap)
        self.layout.addWidget(logo_label, alignment = Qt.AlignTop | Qt.AlignLeft)
        
        self.set_ui()
    
    def set_ui(self):
        self.nbtn = QPushButton("Перейти на основное окно")
        self.nbtn.clicked.connect(self.btnclc)
        self.nbtn.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.layout.addWidget(self.nbtn)
           
        
        
    def btnclc(self):
        self.addbtn = QPushButton("Добавить")
        self.addbtn.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.addbtn.clicked.connect(self.open_add_partner_dialog)
        self.layout.addWidget(self.addbtn)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["asd","asvd","ads"])
        self.layout.addWidget(self.table)
        self.nbtn.deleteLater()
        self.nbtn1 = QPushButton("Назад")
        self.nbtn1.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.nbtn1.clicked.connect(self.dele)
        self.layout.addWidget(self.nbtn1)
    
    def dele(self):
        self.nbtn1.deleteLater()
        self.addbtn.deleteLater()
        self.table.deleteLater()
        self.set_ui()
        
    
    def open_add_partner_dialog(self):
        dialog = AddWindow(self)
        dialog.exec()
         
        
        
class AddWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        
        main_layout = QVBoxLayout(self)
        
        self.setWindowTitle("Добавление")
        self.setFixedSize(500,400)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap("Мастер пол.png")
        logo_pixmap = logo_pixmap.scaled(50,50)
        logo_label.setPixmap(logo_pixmap)
        main_layout.addWidget(logo_label, alignment = Qt.AlignTop | Qt.AlignLeft)
        
        self.l1 = QLabel("Тип")
        self.c1 = QComboBox()
        
        self.l2 = QLabel("Наименонавние партнера")
        self.le2 = QLineEdit()
        
        self.l3 = QLabel("Директор")
        self.le3 = QLineEdit()
        
        self.l4 = QLabel("Номер")
        self.le4 = QLineEdit()
        
        self.l5 = QLabel("Рейтинг")
        self.le5 = QLineEdit()
        
        main_layout.addWidget(self.l1)
        main_layout.addWidget(self.c1)
        main_layout.addWidget(self.l2)
        main_layout.addWidget(self.le2)
        main_layout.addWidget(self.l3)
        main_layout.addWidget(self.le3)
        main_layout.addWidget(self.l4)
        main_layout.addWidget(self.le4)
        main_layout.addWidget(self.l5)
        main_layout.addWidget(self.le5)
        
        
        
        
        self.esc = QPushButton("Назад")
        self.esc.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.esc.clicked.connect(self.esp)
        main_layout.addWidget(self.esc)
        
        
    def esp(self):
        self.close()

        
        
        
            