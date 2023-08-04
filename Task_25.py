import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver
    driver.quit()




def test_show_all_pets(driver):
    mailInput = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    # Вводим email
    mailInput.send_keys('milana9604@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('manutd')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Нажимаем на мои питомцы
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Проверяем, что мы оказались на странице с питомцами пользователя
    assert driver.find_element(By.TAG_NAME, 'h2').text == "Милана"


    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')
    names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')
    age = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    breed = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    petsInfo = list(map(int, re.findall('\d+', driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]').text)))[0]

    # проверяем что У всех питомцев есть имя, возраст и порода.
    for i in range(len(names)):
       assert names[i].text != ''
       assert age[i].text != ''
       assert breed[i].text != ''

    # проверяем что присутствуют все питомцы
    assert len(all_my_pets) == petsInfo

    # проверяем, что хотя бы у половины питомцев есть фото.
    pets_images = []
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            pets_images.append(images[i].get_attribute("src"))
    assert petsInfo/2 <= len(pets_images)


    # проверяем, что у всех питомцев разные имена
    pets_names = []
    for i in range(len(names)):
        pet_name = names[i].text
        pets_names.append(pet_name)
    pets_names1 = list(set(pets_names))
    assert len(pets_names1) == petsInfo

    # проверяем, что В списке нет повторяющихся питомцев.
    # Повторяющиеся питомцы — это питомцы, у которых одинаковое имя, порода и возраст.
    pets = []
    for i in range(len(names)):
        pet = [names[i].text, age[i].text, breed[i].text]
        if pet not in pets:
            pets.append(pet)
    pets_amount = len(pets)
    assert pets_amount == petsInfo



