from selenium import webdriver
from selenium.webdriver.common.by import By
import locators


def provjeri_zakljucene_ocjene(username, password, classes):
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    driver.get("https://e-dnevnik.skole.hr/")
    username_elem = driver.find_element(By.ID, "username")
    username_elem.send_keys(username)
    pass_key = driver.find_element(By.ID, "password")
    pass_key.send_keys(password)
    log_in = driver.find_element(By.XPATH, "/html/body/div[1]/div/form/input[4]")
    log_in.click()
    all_classes_names = [element.text.strip() for element in
                         driver.find_elements(By.CSS_SELECTOR, locators.classes_names)]
    all_classes = [element.get_attribute('href') for element in
                   driver.find_elements(By.CSS_SELECTOR, locators.classes_links)]
    for i in range(0, len(all_classes)):
        if classes != "":
            if all_classes_names[i] in classes:
                driver.get(all_classes[i])
                check(driver)
        else:
            driver.get(all_classes[i])
            check(driver)
    driver.quit()


def check(driver):
    unconcluded_grades = []
    # otvori imenik
    driver.find_element(By.CSS_SELECTOR, locators.grade_book).click()

    # skupi sve linkove na učenike
    base_url = driver.current_url
    all_students = [element.get_attribute('href') for element in
                    driver.find_elements(By.CSS_SELECTOR, locators.all_students_links)]

    # za svakog učenika provjeri je li zaključena ocjena
    for student in all_students:
        driver.get(student)
        # skupi sve predmete
        all_subjects_names = [element.text.split("\n")[0] for element in
                              driver.find_elements(By.CSS_SELECTOR, locators.all_subjects)]
        all_subjects_links = [element.get_attribute('href') for element in
                              driver.find_elements(By.CSS_SELECTOR, locators.all_subjects)]
        # za svaki predmet provjeri je li zaključena ocjena
        for i in range(0, len(all_subjects_names)):
            if all_subjects_names[i].strip() != "Sat razrednika":
                driver.get(all_subjects_links[i])
                final_grade = driver.find_element(By.CSS_SELECTOR, locators.final_grade).text
                if final_grade == "":
                    student_name = driver.find_element(By.CLASS_NAME, locators.student_name).text
                    class_name = driver.find_element(By.XPATH, locators.class_name).text
                    temp = class_name + " " + student_name + " nema zaključenu ocjenu iz predmeta " + \
                           all_subjects_names[i]
                    unconcluded_grades.append(temp)
            driver.back()
        driver.get(base_url)

    # zapiši sve učenike s nezaključenom ocjenom u datoteku
    with open('nezakljucene_ocjene.txt', 'a') as file:
        for line in unconcluded_grades:
            file.write(line + "\n")
