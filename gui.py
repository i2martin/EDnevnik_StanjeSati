import sys
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QInputDialog
)
from stanje_svih_sati import stanje_sati
from zakljucene_ocjene import provjeri_zakljucene_ocjene


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("e-Dnevnik")

        stanje_sati_button = QPushButton("Stanje sati")
        stanje_sati_button.clicked.connect(self.stanje_sati)

        zakljucene_ocjene_button = QPushButton("Zaključene ocjene?")
        zakljucene_ocjene_button.clicked.connect(self.prompt_additional_info)

        button_layout = QHBoxLayout()
        button_layout.addWidget(stanje_sati_button)
        button_layout.addWidget(zakljucene_ocjene_button)

        layout = QVBoxLayout()
        self.widgets = [
            QLabel("Korisničko ime: "),
            QLineEdit(),
            QLabel("Lozinka: "),
            QLineEdit(),
            QLabel("Broj tjedana (1-35): "),
            QLineEdit(),
        ]

        self.widgets[3].setEchoMode(QLineEdit.EchoMode.Password)

        for w in self.widgets:
            layout.addWidget(w)

        layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def get_username(self):
        if "@skole.hr" not in self.widgets[1].text():
            self.show_error_message("Neispravno korisničko ime")
            return None
        else:
            return self.widgets[1].text()

    def get_password(self):
        return self.widgets[3].text()

    def get_number_of_weeks(self):
        try:
            number_of_weeks = int(self.widgets[5].text())
            if 1 <= number_of_weeks <= 35:
                return number_of_weeks
            else:
                self.show_error_message("Broj tjedana mora biti između 1 i 35")
                return None
        except ValueError:
            self.show_error_message("Molimo unesite broj između 1 i 35")
            return None

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec()

    def show_info_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle("Info")
        msg.exec()

    def stanje_sati(self):
        username = self.get_username()
        if username is None:
            return

        password = self.get_password()
        number_of_weeks = self.get_number_of_weeks()
        if number_of_weeks is None:
            return

        stanje_sati(username, password, number_of_weeks)

    def prompt_additional_info(self):
        text, ok = QInputDialog.getText(self, 'Popis razreda', 'Navedite sve oznake razreda, odvojene zarezom, za koje želite provjeru zaključenih ocjena (npr. 1.ag,2.ag). Ako ostavite prazno, provjerit će se svi razredi (ovo može potrajati nekoliko minuta).')
        if ok:
            self.provjeri_zakljucene_ocjene(text)

    def provjeri_zakljucene_ocjene(self, classes):
        username = self.get_username()
        if username is None:
            return

        password = self.get_password()
        provjeri_zakljucene_ocjene(username, password, classes)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
