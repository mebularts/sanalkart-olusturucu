import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt
from faker import Faker
import traceback
import openpyxl
import openpyxl.utils.exceptions


class CardWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(400, 250)

        self.card_number = "XXXX XXXX XXXX XXXX"
        self.expiration_date = "MM/YY"
        self.cvv = "CVV"

        self.setStyleSheet("padding: 20px;")

    def update_card_info(self, card_number, expiration_date, cvv):
        formatted_card_number = " ".join([card_number[i:i + 4] for i in range(0, len(card_number), 4)])
        self.card_number = formatted_card_number
        self.expiration_date = expiration_date
        self.cvv = cvv

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Kredi kartı şeklinde çerçeve çizimi
        card_width = self.width() - 40
        card_height = self.height() - 40

        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(QBrush(Qt.transparent))
        painter.drawRoundedRect(20, 20, card_width, card_height, 10, 10)

        # Kredi kartı bilgileri yazısı
        painter.setPen(QPen(Qt.black, 1))
        painter.setFont(QFont("Arial", 22, QFont.Bold))
        painter.drawText(40, 70, card_width - 32, 30, Qt.AlignCenter, self.card_number)

        painter.setFont(QFont("Arial", 16, QFont.Bold))
        painter.drawText(-30, 170, card_width - 80, 20, Qt.AlignCenter, self.expiration_date)
        painter.drawText(140, 170, card_width - 80, 20, Qt.AlignCenter, self.cvv)

        # Developer bilgisi
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        painter.setPen(QPen(Qt.white))
        painter.drawText(-40, self.height() - 17, self.width(), 20, Qt.AlignCenter, "Developed by")

        painter.setPen(QPen(Qt.white, 2))
        painter.drawText(35, self.height() - 17, self.width(), 20, Qt.AlignCenter, "@mebularts")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sanal Kart Oluşturucu")

        # Temayı ayarla
        self.set_theme()

        self.card_widget = CardWidget()

        copy_button = QPushButton("Kopyala")
        copy_button.clicked.connect(self.copy_card_info)
        copy_button.setFixedHeight(40)  # Düğme yüksekliğini ayarla

        create_button = QPushButton("Kart Oluştur")
        create_button.clicked.connect(self.create_virtual_card)
        create_button.setFixedHeight(40)  # Düğme yüksekliğini ayarla

        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Kart sayısı")
        self.number_input.setFixedHeight(40)
        self.number_input.setFixedWidth(200)

        bulk_create_button = QPushButton("Toplu Oluştur")
        bulk_create_button.clicked.connect(self.bulk_create_cards)
        bulk_create_button.setFixedHeight(40)
        bulk_create_button.setFixedWidth(100)

        self.card_list_label = QLabel("Oluşturulan Kartlar:")
        self.card_list_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.card_list_label.setFixedHeight(30)
        self.card_list_label.hide()

        self.card_list = QLabel()
        self.card_list.setWordWrap(True)
        self.card_list.hide()

        copy_all_button = QPushButton("Hepsini Kopyala")
        copy_all_button.clicked.connect(self.copy_all_cards)
        copy_all_button.setFixedHeight(40)


        button_layout = QHBoxLayout()
        button_layout.addWidget(copy_button)
        button_layout.addWidget(create_button)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.number_input)
        input_layout.addWidget(bulk_create_button)
        input_layout.addWidget(copy_all_button)

        layout = QVBoxLayout()
        layout.addWidget(self.card_widget)
        layout.addLayout(button_layout)
        layout.addLayout(input_layout)
        layout.addWidget(self.card_list_label)
        layout.addWidget(self.card_list)

        self.setLayout(layout)

    def set_theme(self):
        # Fusion temasını ayarla
        app.setStyle("Fusion")

        # Renk paletini oluştur
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        # Uygulama paletini ayarla
        app.setPalette(palette)

    def create_virtual_card(self):
        fake = Faker()

        # Kart numarası
        visa_prefix = "4"
        card_number_length = 16
        card_number = visa_prefix + ''.join(str(fake.random_digit()) for _ in range(card_number_length - 1))

        # Son kullanma tarihi (ay ve yıl)
        expiration_month = str(fake.random_int(min=1, max=12)).zfill(2)
        expiration_year = str(fake.random_int(min=24, max=29))

        # Güvenlik kodu (CVV/CVC)
        cvv = ''.join(str(fake.random_digit()) for _ in range(3))

        self.card_widget.update_card_info(card_number, expiration_month + "/" + expiration_year, cvv)

    def copy_card_info(self):
        clipboard = QApplication.clipboard()
        card_info = f"Kart No: {self.card_widget.card_number} SKT: {self.card_widget.expiration_date} CVV: {self.card_widget.cvv}"
        clipboard.setText(card_info)
        QMessageBox.information(self, "Kopyalandı", "Kart bilgileri kopyalandı!")

    def bulk_create_cards(self):
        try:
            num_cards = int(self.number_input.text())
            if num_cards <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Hatalı Giriş", "Lütfen geçerli bir kart sayısı girin (pozitif tam sayı)!")
            return

        fake = Faker()
        cards = []

        for _ in range(num_cards):
            visa_prefix = "4"
            card_number_length = 16
            card_number = visa_prefix + ''.join(str(fake.random_digit()) for _ in range(card_number_length - 1))

            expiration_month = str(fake.random_int(min=1, max=12)).zfill(2)
            expiration_year = str(fake.random_int(min=24, max=29))

            cvv = ''.join(str(fake.random_digit()) for _ in range(3))

            cards.append((card_number, expiration_month + "/" + expiration_year, cvv))

        self.display_card_list(cards)

    def display_card_list(self, cards):
        card_text = "<ul>"
        for card in cards:
            card_text += f"<li>Kart No: {card[0]} SKT: {card[1]} CVV: {card[2]}</li>"
        card_text += "</ul>"

        self.card_list.setText(card_text)
        self.card_list_label.show()
        self.card_list.show()

    def copy_all_cards(self):
        clipboard = QApplication.clipboard()
        card_text = self.card_list.text()
        clipboard.setText(card_text)
        QMessageBox.information(self, "Kopyalandı", "Tüm kart bilgileri kopyalandı!")
    


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
