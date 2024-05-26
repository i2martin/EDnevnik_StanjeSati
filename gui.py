import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from predmeti import find_weekly_hours
import time
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("e-Dnevnik stanje sati")

        button = QPushButton("Prijava")
        button.clicked.connect(self.e_dnevnik)

        layout = QVBoxLayout()
        self.widgets = [
            QLabel("Korisničko ime: "),
            QLineEdit(),
            QLabel("Lozinka: "),
            QLineEdit(),
            QLabel("Broj tjedana (1-35): "),
            QLineEdit(),
            button
        ]

        self.widgets[3].setEchoMode(QLineEdit.EchoMode.Password)

        for w in self.widgets:
            layout.addWidget(w)

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

    def e_dnevnik(self):
        username = self.get_username()
        if username is None:
            return

        password = self.get_password()
        number_of_weeks = self.get_number_of_weeks()
        if number_of_weeks is None:
            return

        list_to_file = []
        driver = webdriver.Chrome()
        driver.implicitly_wait(2)
        driver.get("https://e-dnevnik.skole.hr/")
        username_elem = driver.find_element(By.ID, "username")
        username_elem.send_keys(username)
        pass_key = driver.find_element(By.ID, "password")
        pass_key.send_keys(password)
        log_in = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input[4]")
        log_in.click()

        parent = driver.find_element(By.ID, "class-list")
        classes = [single_class.get_attribute('href') for single_class in parent.find_elements(By.TAG_NAME, 'a')]

        for single_class in classes:
            driver.get(single_class)
            driver.find_element(By.CLASS_NAME, "icon-dnevnik-rada").click()
            driver.find_element(By.XPATH, "/html/body/div[1]/ul/li[3]/div/a[5]").click()

            parent = driver.find_element(By.CLASS_NAME, 'cc-container')
            subjects = [subject.get_attribute('href') for subject in parent.find_elements(By.TAG_NAME, 'a')]

            for subject in subjects:
                driver.get(subject)
                no_of_hours = sum(
                    int(table.text) for i, table in enumerate(driver.find_elements(By.XPATH, '/html/body/div[5]/div/table[1]/tbody/tr/td[2]')) if i < 3
                )

                subject_name = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[2]/tbody/tr[1]/th')
                s_class, sub = map(str.strip, subject_name.text.split("-", maxsplit=1))
                expected_number_of_hours = find_weekly_hours(s_class, sub) * number_of_weeks
                missing_hours = no_of_hours - expected_number_of_hours
                line = f"{subject_name.text},{no_of_hours},{expected_number_of_hours},{missing_hours}\n"
                list_to_file.append(line)

        with open('stanje_sati.txt', 'a') as file:
            for line in list_to_file:
                file.write(line)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
