from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QDialog, QLineEdit, QComboBox, QMessageBox, QTableWidgetItem
from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtCore import Qt
from user_class import Partner, Connect, PartnerProduct
from sqlalchemy import func

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("МастерПол")
        self.setWindowIcon(QIcon("logotype.png"))
        self.resize(500, 500)
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        logo_label = QLabel()
        logo_pixmap = QPixmap("logotype.png")
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
        hb1 = QHBoxLayout()
        
        self.addbtn = QPushButton("Добавить")
        self.addbtn.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.addbtn.clicked.connect(self.open_add_partner_dialog)
        
        self.editbtn = QPushButton("Редактировать")
        self.editbtn.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.editbtn.clicked.connect(self.oped_edit_partner_dialog)
        
        hb1.addWidget(self.addbtn)
        hb1.addWidget(self.editbtn)
        self.layout.addLayout(hb1)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Тип","Наименование","Директор", "Телефон", "Рейтинг", "Скидка", "ID"])
        self.table.setColumnHidden(6, True)
        self.layout.addWidget(self.table)
        self.nbtn.deleteLater()
        self.nbtn1 = QPushButton("Назад")
        self.nbtn1.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.nbtn1.clicked.connect(self.dele)
        self.layout.addWidget(self.nbtn1)
        self.tableo()
        
    def tableo(self):
        session = Connect.create_connection()
        if session is None:
            QMessageBox.critical(self, "Ошибка", "Не удалось подключиться к базе данных.")
            return
        part = session.query(Partner).all()
        self.tabless(part, session)
        session.close()
        
    def tabless(self, part, session):
        self.table.setRowCount(len(part))
        for row, par in enumerate(part):
            total_count = session.query(func.sum(PartnerProduct.count_product)).filter(PartnerProduct.id_partner == par.partners_id).scalar() or 0
            
            if total_count < 10000:
                discount = "0%"
            elif 10000 <= total_count <= 50000:
                discount = "5%"
            elif 50000 < total_count <= 300000:
                discount = "10%"
            else:
                discount = "15%"
            self.table.setItem(row, 0, QTableWidgetItem(par.type_partner))
            self.table.setItem(row, 1, QTableWidgetItem(par.company_name))
            self.table.setItem(row, 2, QTableWidgetItem(par.director_name))
            self.table.setItem(row, 3, QTableWidgetItem(par.phone))
            self.table.setItem(row, 4, QTableWidgetItem(str(par.rating)))
            self.table.setItem(row, 5, QTableWidgetItem(discount))
            self.table.setItem(row, 6, QTableWidgetItem(str(par.partners_id)))
        self.table.resizeColumnsToContents()
        
    def dele(self):
        self.nbtn1.deleteLater()
        self.addbtn.deleteLater()
        self.editbtn.deleteLater()
        self.table.deleteLater()
        self.set_ui()
        
    def open_add_partner_dialog(self):
        dialog = AddWindow(self)
        dialog.exec()
        
    def oped_edit_partner_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите строку для редактирования.")
            return
        
        partner_id = int(self.table.item(selected_row, 6).text())
        dialog = AddWindow(self, partner_id=partner_id)
        dialog.exec()

class AddWindow(QDialog):
    def __init__(self, parent=None, partner_id=None):
        super().__init__(parent)
        self.partner_id = partner_id
        
        main_layout = QVBoxLayout(self)
        
        self.setWindowTitle("Редактирование" if partner_id else "Добавление")
        self.setFixedSize(500,400)
        
        logo_label = QLabel()
        logo_pixmap = QPixmap("logotype.png")
        logo_pixmap = logo_pixmap.scaled(50,50)
        logo_label.setPixmap(logo_pixmap)
        main_layout.addWidget(logo_label, alignment = Qt.AlignTop | Qt.AlignLeft)
        
        self.l1 = QLabel("Тип")
        self.l1.setFont(QFont("Arial", 16))
        self.c1 = QComboBox()
        self.c1.addItems(["ООО", "ОАО", "ИП"])
        
        self.l2 = QLabel("Наименование партнера")
        self.l2.setFont(QFont("Segoe UI", 10))
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
        
        self.sav = QPushButton("Сохранить")
        self.sav.setStyleSheet("""QPushButton {background-color: #F4E8D3} """)
        self.sav.clicked.connect(self.save)
        
        hb = QHBoxLayout()
        hb.addWidget(self.esc)
        hb.addWidget(self.sav)
        
        main_layout.addLayout(hb)
        
        if partner_id:
            session = Connect.create_connection()
            partner = session.query(Partner).filter(Partner.partners_id == partner_id).first()
            if partner:
                self.c1.setCurrentText(partner.type_partner)
                self.le2.setText(partner.company_name)
                self.le3.setText(partner.director_name)
                self.le4.setText(partner.phone)
                self.le5.setText(str(partner.rating))
            session.close()
        
    def save(self):
        type_partner = self.c1.currentText()
        company_name = self.le2.text()
        director_name = self.le3.text()
        phone = self.le4.text()
        rating_text = self.le5.text()
        
        if not all([type_partner, company_name, director_name, phone, rating_text]):
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
            return
        
        try:
            rating = int(rating_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Рейтинг должен быть целым числом.")
            return
        
        session = Connect.create_connection()
        
        if self.partner_id:
            # Режим редактирования
            partner = session.query(Partner).filter(Partner.partners_id == self.partner_id).first()
            if partner:
                partner.type_partner = type_partner
                partner.company_name = company_name
                partner.director_name = director_name
                partner.phone = phone
                partner.rating = rating
                reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите изменить данные партнера?", QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    session.commit()
                    QMessageBox.information(self, "Успех", "Данные партнера успешно обновлены.")
                else: return
        else:
            # Режим добавления
            new_partner = Partner(type_partner=type_partner, company_name=company_name, director_name=director_name, phone=phone, rating=rating)
            session.add(new_partner)
            reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите изменить данные партнера?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                session.commit()
                QMessageBox.information(self, "Успех", "Партнер успешно добавлен.")
            else: return
        
        self.parent().tableo()
        session.close()
        self.close()
        
    def esp(self):
        self.close()
        
        
    #     def del_emp(self):
    #     selected_row = self.table.currentRow()
    #     if selected_row < 0:
    #         QMessageBox.warning(self, 'Ошибка', 'Выберите строку')
    #         return
        
    #     employee_id = int(self.table.item(selected_row, 5).text())
        
    #     reply = QMessageBox.question(self, 'Подтверждение','Удалить сотрудника?', QMessageBox.Yes | QMessageBox.No)
        
    #     if reply == QMessageBox.Yes:
    #         session = Connect.create_connection()
    #         employee = session.query(Employee).filter(Employee.id == employee_id).first()
    #         session.delete(employee)
    #         session.commit()
    #         self.up_table()
    #         session.close()
    #         QMessageBox.information(self, 'Успех','Пользователь добавлен')
            
    # def search(self):
    #     session = Connect.create_connection()
    #     lnc = self.le5.text()
    #     if lnc:
    #         employees = session.query(Employee).filter(Employee.last_name.ilike(f"%{lnc}%")).all()
    #     else:
    #         employees = session.query(Employee).all()
    #     self.upd_table(employees)
    #     session.close()