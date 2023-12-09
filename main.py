from selenium import webdriver
from selenium.webdriver.common.by import By
from predmeti import find_weekly_hours
from selenium.webdriver.common.keys import Keys
import time

#broj tjedana - za sad potrebno ručno upisati
number_of_weeks = 14
expected_number_of_hours = 0
list_to_file = []
driver = webdriver.Chrome('./chromedriver')
driver.get("https://e-dnevnik.skole.hr/")
username = driver.find_element(By.ID, "username")
username.send_keys("ivan.martinovic17@skole.hr")
pass_key = driver.find_element(By.ID, "password")
pass_key.send_keys("1234269556")
log_in = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input[4]")
log_in.click()


# dohvati sve razrede
parent = driver.find_element(By.ID, "class-list")
classes = []

#dohvati poveznice na sve razredne knjige
for single_class in parent.find_elements(By.TAG_NAME, 'a'):
    classes.append(single_class.get_attribute('href'))

for single_class in classes:
    driver.get(single_class)
    time.sleep(0.1)
    # za svaki razred otvori dnevnik rada --> radni sati po predmetu
    driver.find_element(By.CLASS_NAME, "icon-dnevnik-rada").click()
    driver.find_element(By.XPATH, "/html/body/div[1]/ul/li[3]/div/a[4]").click()

    # prikupi sve linkove na predmete
    parent = driver.find_element(By.CLASS_NAME, 'cc-container')
    subjects = []
    for subject in parent.find_elements(By.TAG_NAME, 'a'):
        subjects.append(subject.get_attribute('href'))

    # prođi kroz sve predmete
    for subject in subjects:
        driver.get(subject)
        no_of_hours = 0
        time.sleep(0.1)
        # dohvati podatke o trenutnom broju sati
        hour_tables = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[1]/tbody/tr[3]')
        for table in hour_tables.find_elements(By.TAG_NAME, 'td'):
            no_of_hours = no_of_hours + int(table.get_attribute("innerHTML"))
        subject_name = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[2]/tbody/tr[1]/th')
        s_class, sub = subject_name.text.split("-", maxsplit=1)
        s_class = s_class.strip()
        sub = sub.strip()
        #odredi planirani broj sati
        expected_number_of_hours = find_weekly_hours(s_class, sub)

        # zapiši razred, predmet i broj održanih sati
        expected_number_of_hours = expected_number_of_hours * number_of_weeks
        missing_hours = no_of_hours - expected_number_of_hours
        line = subject_name.text + "," + str(no_of_hours) + "," + str(expected_number_of_hours) + "," + str(
            missing_hours) + "\n"
        list_to_file.append(line)

for line in list_to_file:
    with open('stanje_sati.txt', 'a') as file:
        file.write(line)