from selenium import webdriver
from selenium.webdriver.common.by import By
from predmeti import find_weekly_hours
import locators

def stanje_sati(username, password, number_of_weeks):
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

    parent = driver.find_elements(By.CSS_SELECTOR, locators.classes_links)
    classes = [single_class.get_attribute('href') for single_class in parent]

    for single_class in classes:
        driver.get(single_class)
        driver.find_element(By.CLASS_NAME, "icon-dnevnik-rada").click()
        driver.find_element(By.XPATH, "/html/body/div[1]/ul/li[3]/div/a[5]").click()

        parent = driver.find_element(By.CLASS_NAME, 'cc-container')
        subjects = [subject.get_attribute('href') for subject in parent.find_elements(By.TAG_NAME, 'a')]
        try:
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
        except:
            #skip all the empty classes for now
            pass

    with open('stanje_sati.txt', 'a') as file:
        for line in list_to_file:
            file.write(line)

    driver.quit()
