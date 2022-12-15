from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#broj tjedana - za sad potrebno ručno upisati
number_of_weeks = 15
expected_number_of_hours = 0
driver = webdriver.Chrome('./chromedriver')
driver.get("https://e-dnevnik.skole.hr/")

username = driver.find_element(By.ID, "username")
username.send_keys("")
pass_key = driver.find_element(By.ID, "password")
pass_key.send_keys("")
log_in = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input[4]")
log_in.click()


# dohvati sve razrede
parent = driver.find_element(By.ID, "class-list")
classes = []
for single_class in parent.find_elements(By.TAG_NAME, 'a'):
    classes.append(single_class.get_attribute('href'))

for single_class in classes:
    driver.get(single_class)

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
        # dohvati podatke o trenutnom broju sati
        no_of_hours = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[1]/tbody/tr[3]/td')
        subject_name = driver.find_element(By.XPATH, '/html/body/div[5]/div/table[2]/tbody/tr[1]/th')

        #odredi planirani broj sati
        #TODO: Izraditi bazu predmeta s brojem sati
        if "Matematika" in subject_name.text:
            if "1.g" in subject_name.text or "2.g" in subject_name.text or "3.g" in subject_name.text or "4.g" in subject_name.text or "1.tr" in subject_name.text or "2.tr" in subject_name.text:
                expected_number_of_hours = 4
            elif "3.tr" in subject_name.text or "4.tr" in subject_name.text:
                expected_number_of_hours = 3
            elif "1.vv" in subject_name.text or "2.vv" in subject_name.text or "3.vv" in subject_name.text:
                expected_number_of_hours = 1
            else:
                expected_number_of_hours = 2
        elif "Hrvatski jezik" in subject_name.text:
            if "1.g" in subject_name.text or "2.g" in subject_name.text or "3.g" in subject_name.text or "4.g" in subject_name.text:
                expected_number_of_hours = 4
            else:
                expected_number_of_hours = 3
        elif "Engleski jezik" in subject_name.text:
            if "1.g" in subject_name.text or "2.g" in subject_name.text or "3.g" in subject_name.text or "4.g" in subject_name.text or "3.tr" in subject_name.text or "4.tr" in subject_name.text:
                expected_number_of_hours = 3
            else:
                expected_number_of_hours = 2
        elif "Praktična nastava" in subject_name.text:
            expected_number_of_hours = 7
        elif "Sat razrednika" in subject_name.text:
            expected_number_of_hours = 1
        else:
            expected_number_of_hours = 2
        # zapiši razred, predmet i broj održanih sati
        expected_number_of_hours = expected_number_of_hours * number_of_weeks
        missing_hours = int(no_of_hours.text) - expected_number_of_hours
        with open('stanje_sati.txt', 'a') as file:
            line = subject_name.text + "," + no_of_hours.text + "," + str(expected_number_of_hours) + "," + str(missing_hours) + "\n"
            file.write(line)
