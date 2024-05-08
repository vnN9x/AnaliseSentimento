from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
import time

url = f'https://querobolsa.com.br/unip/avaliacao-dos-alunos'

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options) 
driver.get(url)

full_data = []

for z in range(401):
    author = driver.find_elements(By.XPATH, '//strong[@class="z-title student-evaluation__profile-name z-title--size-extra-small"]')
    rev = driver.find_elements(By.XPATH, '//p[@class="z-text student-evaluation__text z-text--size-medium z-text--left"]')
    rating_raw = driver.find_elements(By.XPATH, '//div[@class="rating-bubbles popover-ratings__ratings-bubbles"]')
    filtered_rating = []

    for k in range(len(rating_raw)):
        if rating_raw[k].text != '' and k != 0:
            filtered_rating.append(float(rating_raw[k].text))

    reviews = lista_de_listas = [list(par) for par in zip(rev[::2], rev[1::2])]

    for i in range(len(reviews)):

        if filtered_rating[i] >= 4:
            rating_value = 'Positivo'
        elif filtered_rating[i] < 3:
            rating_value = 'Negativo'
        else:
            rating_value = 'Neutro'

        full_data.append([author[i].text, reviews[i][0].text + ' ' + reviews[i][1].text, rating_value])
        #print(f'\nNome: {author[i].text}\npros: {reviews[i][0].text}\n\ncons: {reviews[i][1].text}\n===== <> ===== <> ===== <>')

    next_button = driver.find_elements(By.XPATH, '//button[@class="paginator__button paginator__arrow-button"]')
    next_button[1].click()
    time.sleep(3)

driver.quit()

df = pd.DataFrame(full_data, columns=['author', 'text', 'rating'])
df.head(10)
df.to_csv('./data/others/querobolsa.csv')

print(df)