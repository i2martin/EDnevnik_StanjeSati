import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome('./chromedriver')

driver.get("https://e-dnevnik.skole.hr/")
time.sleep(1)
username = driver.find_element(By.ID, "username")
username.send_keys("")
pass_key = driver.find_element(By.ID, "password")
pass_key.send_keys("")
log_in = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input[4]")
log_in.click()

time.sleep(0.3)

# dohvati sve razrede
parent = driver.find_element(By.ID, "class-list")
classes = []
for single_class in parent.find_elements(By.TAG_NAME, 'a'):
    classes.append(single_class.get_attribute('href'))

for single_class in classes:
    driver.get(single_class)
    time.sleep(0.3)

    # za svaki razred otvori dnevnik rada --> radni sati po predmetu
    driver.find_element(By.CLASS_NAME, "icon-dnevnik-rada").click()
    time.sleep(0.3)
    driver.find_element(By.XPATH, "/html/body/div[1]/ul/li[3]/div/a[4]").click()
    time.sleep(0.3)

    # prikupi sve linkove na predmete
    parent = driver.find_element(By.CLASS_NAME, 'cc-container')
    subjects = []
    for subject in parent.find_elements(By.TAG_NAME, 'a'):
        subjects.append(subject.get_attribute('href'))

    # prođi kroz sve predmete
    for subject in subjects:
        driver.get(subject)
        # dohvati podatke o trenutnom broju sati
        no_of_hours = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[1]/tbody/tr[3]/td')
        subject_name = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[2]/tbody/tr[1]/th')

        # zapiši razred, predmet i broj održanih sati
        with open('stanje_sati.txt', 'a') as file:
            line = subject_name.text + "," + no_of_hours.text + "\n"
            file.write(line)
