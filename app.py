from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QDialog, QScrollArea, QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QIcon
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from reportlab.lib.pagesizes import A4
from sqlalchemy import func
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import sys


# Определение базы данных через SQLAlchemy
Base = declarative_base()

class Partner(Base):
    __tablename__ = 'partners'
    partners_id = Column(Integer, primary_key=True, autoincrement=True)
    type_partner = Column(String)
    company_name = Column(String)
    director_name = Column(String)
    phone = Column(String)
    rating = Column(Integer)
    partnerproducts = relationship("PartnerProduct", back_populates="partner_relation")
    

class PartnerProduct(Base):
    __tablename__ = 'partnerproduct'
    pp_id = Column(Integer, primary_key=True)
    id_partner = Column(Integer, ForeignKey('partners.partners_id'))
    id_product = Column(Integer)
    count_product = Column(Integer)
    partner_relation = relationship("Partner", back_populates="partnerproducts")


class PartnerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("МастерПол")
        self.resize(800, 600)
        
        self.setWindowIcon(QIcon('icons.ico')) 

        # Создание подключения к базе данных через SQLAlchemy для PostgreSQL
        self.engine = create_engine('postgresql://postgres:1234@localhost:5432/postgres')  
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Основной виджет и макет
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)  # Основной макет для размещения боковой панели и содержимого
        main_widget.setStyleSheet("background-color: white;")
        
        # Боковая панель
        side_panel = QWidget()
        side_layout = QVBoxLayout(side_panel)
        side_panel.setStyleSheet("background-color: #F4E8D3; padding: 10px;")
        
        title_label = QLabel("Мастер пол")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: black;")
        

        # Логотип
        logo_label = QLabel()
        logo_pixmap = QPixmap('logotype.png')
        logo_pixmap = logo_pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        side_layout.addWidget(logo_label)
        side_layout.addWidget(title_label)
        # Кнопка "Партнеры"
        self.partners_button = QPushButton("Партнеры")
        self.partners_button.setStyleSheet("background-color: #67BA80; color: white; padding: 10px;")
        self.partners_button.clicked.connect(self.load_partners)
        side_layout.addWidget(self.partners_button)

        # Кнопка "Добавление Редактирование"
        self.add_edit_button = QPushButton("Добавление")
        self.add_edit_button.setStyleSheet("background-color: #67BA80; color: white; padding: 10px;")
        self.add_edit_button.clicked.connect(self.open_add_partner_dialog)
        side_layout.addWidget(self.add_edit_button)

        # Кнопка "История"
        self.history_button = QPushButton("История")
        self.history_button.setStyleSheet("background-color: #67BA80; color: white; padding: 10px;")
        self.history_button.clicked.connect(self.show_history)
        side_layout.addWidget(self.history_button)
        
        side_layout.addStretch()  # Добавляет отступ снизу

        # Прокручиваемая область для списка партнеров (основное содержимое)
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.partner_list_layout = QVBoxLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)
        content_layout.addWidget(scroll_area)

        # Добавляем боковую панель и основное содержимое в главный макет
        main_layout.addWidget(side_panel, 1)
        main_layout.addWidget(content_widget, 4)

        self.setCentralWidget(main_widget)

        # Загрузка данных
        self.load_partners()

    def show_history(self):
        history_dialog = QDialog(self)
        history_dialog.setWindowTitle("История реализации продукции")
        history_dialog.resize(600, 400)

        layout = QVBoxLayout()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["ID Продукта", "ID Партнера", "Количество"])

        try:
            partner_products = self.session.query(
                PartnerProduct.id_product,
                PartnerProduct.id_partner,
                PartnerProduct.count_product
            ).all()

            self.history_table.setRowCount(len(partner_products))

            for row, partner_product in enumerate(partner_products):
                self.history_table.setItem(row, 0, QTableWidgetItem(str(partner_product.id_product)))
                self.history_table.setItem(row, 1, QTableWidgetItem(str(partner_product.id_partner)))
                self.history_table.setItem(row, 2, QTableWidgetItem(str(partner_product.count_product)))

            layout.addWidget(self.history_table)
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            self.session.rollback()

                # Кнопка "Отчет"
        self.report_button = QPushButton("Отчет")
        self.report_button.setStyleSheet("background-color: #67BA80; color: white; padding: 10px;")
        self.report_button.clicked.connect(self.generate_report)
        layout.addWidget(self.report_button)


        history_dialog.setLayout(layout)
        history_dialog.exec()

    def open_add_partner_dialog(self):
        dialog = PartnerDialog(self)
        dialog.exec()
        self.load_partners()
        
        
    def generate_report(self):
        c = canvas.Canvas("report.pdf", pagesize=A4)
        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))  # Используем шрифт с поддержкой кириллицы
        c.setFont("DejaVuSans", 14)

        c.drawString(200, 800, "Отчет по продажам")
        y = 750
        c.setFont("DejaVuSans", 9)
        i = 1

        for row in range(self.history_table.rowCount()):
            # Получаем данные из строки, проверяя наличие элемента в каждой ячейке
            row_data = [
                self.history_table.item(row, col).text() if self.history_table.item(row, col) is not None else ""
                for col in range(5)
            ]
            
            # Рисуем строку в PDF
            c.drawString(10, y, f"{i})")
            c.drawString(20, y, " | ".join(row_data))
            y -= 20
            i += 1

        c.save()


    def calculate_discount(self, total_sales):
        if total_sales >= 300000:
            return "15%"
        elif total_sales >= 50000:
            return "10%"
        elif total_sales >= 10000:
            return "5%"
        else:
            return "0%"

    def load_partners(self):
        while self.partner_list_layout.count():
            child = self.partner_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Используем SQLAlchemy для загрузки данных из таблицы Partners
        partners = self.session.query(Partner).all()
        for partner in partners:
            partner_id = partner.partners_id
            partner_type = partner.type_partner
            partner_name = partner.company_name
            director_name = partner.director_name
            phone = partner.phone
            rating = partner.rating

            # Здесь можно выполнить дополнительные запросы для расчета скидок и других данных
            sales_query = self.session.execute(
                select(func.sum(PartnerProduct.count_product)).where(PartnerProduct.id_partner == partner_id)
                )           
            total_sales = sales_query.scalar() or 0
            discount = self.calculate_discount(total_sales)

            partner_card = QFrame()
            partner_card.setStyleSheet(""" 
                background-color: #FFFFFF; 
                border: 1px solid black; 
                padding: 1px;
            """)
            partner_card_layout = QHBoxLayout()
            partner_card.mousePressEvent = lambda event, pid=partner_id, pt=partner_type, pn=partner_name, dn=director_name, ph=phone, rt=rating: self.open_edit_partner_dialog(event, pid, pt, pn, dn, ph, rt)

            left_layout = QVBoxLayout()
            name_label = QLabel(f"{partner_type} | {partner_name}")
            name_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
            name_label.setStyleSheet("color: black;border: 0px;")

            director_label = QLabel(f"Директор: {director_name}")
            phone_label = QLabel(f"Телефон: {phone}")
            rating_label = QLabel(f"Рейтинг: {rating}")
            for label in (director_label, phone_label, rating_label):
                label.setFont(QFont("Segoe UI", 10))
                label.setStyleSheet("color: black;border: 0px;")

            left_layout.addWidget(name_label)
            left_layout.addWidget(director_label)
            left_layout.addWidget(phone_label)
            left_layout.addWidget(rating_label)

            right_layout = QVBoxLayout()
            sales_label = QLabel(f"Продажи: {total_sales}")
            sales_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            sales_label.setStyleSheet("color: black;border: 0px;")
            discount_label = QLabel(f"Скидка: {discount}")
            discount_label.setFont(QFont("Segoe UI", 10))
            discount_label.setStyleSheet("color: black;border: 0px;")
            
            right_layout.addWidget(sales_label)
            right_layout.addWidget(discount_label)

            partner_card_layout.addLayout(left_layout)
            partner_card_layout.addLayout(right_layout)
            partner_card.setLayout(partner_card_layout)
            self.partner_list_layout.addWidget(partner_card)

    def open_edit_partner_dialog(self, event, partner_id, partner_type, partner_name, director_name, phone, rating):
        """
        Открывает окно редактирования партнера.
        """
        print(f"Редактирование партнера: {partner_id}, {partner_name}")
        edit_dialog = PartnerDialog(self, partner_id)  # Передаем partner_id в диалог
        edit_dialog.name_input.setText(partner_name)
        edit_dialog.type_input.setText(partner_type)
        edit_dialog.director_input.setText(director_name)
        edit_dialog.phone_input.setText(phone)
        edit_dialog.rating_input.setText(str(rating))
        edit_dialog.exec()
        self.load_partners()

class PartnerDialog(QDialog):
    def __init__(self, parent=None, partner_id=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление партнера")
        self.setFixedSize(400, 300)

        self.partner_id = partner_id  # Сохраняем partner_id в объекте диалога

        layout = QVBoxLayout(self)

        self.name_input = QLineEdit(self)
        self.type_input = QLineEdit(self)
        self.director_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        self.rating_input = QLineEdit(self)

        layout.addWidget(QLabel("Название компании"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Тип партнера"))
        layout.addWidget(self.type_input)
        layout.addWidget(QLabel("Директор"))
        layout.addWidget(self.director_input)
        layout.addWidget(QLabel("Телефон"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("Рейтинг"))
        layout.addWidget(self.rating_input)

        self.save_button = QPushButton("Сохранить", self)
        layout.addWidget(self.save_button)

        self.save_button.clicked.connect(self.save_partner)

        if self.partner_id:
            self.setWindowTitle("Редактирование партнера")
            # Если partner_id передан, заполняем поля существующими данными
            partner = self.parent().session.query(Partner).get(self.partner_id)
            if partner:
                self.name_input.setText(partner.company_name)
                self.type_input.setText(partner.type_partner)
                self.director_input.setText(partner.director_name)
                self.phone_input.setText(partner.phone)
                self.rating_input.setText(str(partner.rating))
                
            # Кнопка удаления (отображается только при редактировании)
        if self.partner_id is not None:
            self.delete_button = QPushButton("Удалить")
            self.delete_button.setFixedHeight(30)
            self.delete_button.setFont(QFont("Segoe UI", 10))
            self.delete_button.setStyleSheet("""
                background-color: #FF6B6B;
                color: black;  /* Черный текст на кнопке */
                border-radius: 5px;
                padding: 5px;
            """)
            self.delete_button.clicked.connect(self.delete_partner)
            layout.addWidget(self.delete_button)

    def save_partner(self):
        # Получаем данные из полей ввода
        name = self.name_input.text()
        partner_type = self.type_input.text()
        director = self.director_input.text()
        phone = self.phone_input.text()
        rating = self.rating_input.text()

        if self.partner_id:  # Если это редактирование
            # Обновляем данные в базе
            partner = self.parent().session.query(Partner).get(self.partner_id)
            if partner:
                partner.company_name = name
                partner.type_partner = partner_type
                partner.director_name = director
                partner.phone = phone
                partner.rating = rating
        else:  # Если это создание нового партнера
            # Создаем новый объект Partner и добавляем в сессию
            new_partner = Partner(
                company_name=name,
                type_partner=partner_type,
                director_name=director,
                phone=phone,
                rating=rating
            )
            self.parent().session.add(new_partner)

        self.parent().session.commit()  # Сохраняем изменения в базе данных
        self.accept()  # Закрываем диалог
        
        
        
    def delete_partner(self):
        if self.partner_id is not None:
            try:
                # Получаем сессию из родительского окна
                session = self.parent().session
                
                # Выполняем запрос на получение партнера по ID
                partner_to_delete = session.query(Partner).filter_by(partners_id=self.partner_id).first()
                
                if partner_to_delete:
                    # Удаляем партнера из базы данных
                    session.delete(partner_to_delete)
                    session.commit()  # Подтверждаем изменения в базе данных
                    self.accept()  # Закрываем диалог после успешного удаления
                else:
                    print("Партнер не найден.")
            except Exception as e:
                session.rollback()  # Откатываем изменения в случае ошибки
                print(f"Ошибка при удалении партнера: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PartnerApp()
    window.show()
    sys.exit(app.exec())
