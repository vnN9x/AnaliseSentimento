from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from keys import *

def obter_tweets(num_tweets=50):
    url = f'https://twitter.com/login'

    # Configurar o navegador
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)  # Você precisa ter o ChromeDriver instalado e no PATH
    driver.get(url)

    time.sleep(3)
    elemento_input = driver.find_element(By.XPATH,"//input[@name='text']")
    elemento_input.send_keys(TWITTER_LOGIN)

    next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Avançar')]")
    next_button.click()

    time.sleep(3)

    password = driver.find_element(By.XPATH,"//input[@name='password']")
    password.send_keys(TWITTER_PASS)

    log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Entrar')]")
    log_in.click()

    time.sleep(2)

    url_top = 'https://twitter.com/search?q=lang%3Apt%20Unip&src=typed_query&f=top'
    driver.get(url_top)
    time.sleep(2)

    top_tweets_list = []
    latest_tweets_list = []

    for _ in range(num_tweets // 10):
        
        UserTag = driver.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
        TimeStamp = driver.find_element(By.XPATH, ".//time").get_attribute('datetime')
        Tweet = driver.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text

        top_tweets_list.append([UserTag, Tweet, TimeStamp])

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    # Obter o conteúdo da página
    page_content_top = driver.page_source

    url_latest = 'https://twitter.com/search?q=lang%3Apt%20Unip&src=typed_query&f=live'
    driver.get(url_latest)
    time.sleep(2)

    for _ in range(num_tweets // 10):  # 10 tweets são carregados a cada rolagem
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Aguardar um breve período após cada rolagem

    #page_content_latest = driver.page_source
    #driver.quit()

    # Analisar a página com BeautifulSoup
    top_page = BeautifulSoup(page_content_top, 'html.parser')
    latest_page = BeautifulSoup(page_content_latest, 'html.parser')

    top_tweets = top_page.find_all("//article[@data-testid='tweet']")

    latest_tweets = latest_page.find_all("//article[@data-testid='tweet']")

    for tweet in top_tweets:
        usuario = tweet.find('span', {'class': 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'}).text
        conteudo = tweet.find('div', {'class': 'css-901oao r-1re7ezh r-1qd0xha r-n6v787 r-16dba41 r-1sf4r6n r-bcqeeo r-qvutc0'}).text
        data = tweet.find('time')['datetime']

        top_tweets_list.append([usuario, conteudo, data])

    for tweet in latest_tweets:
        usuario = tweet.find('span', {'class': 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'}).text
        conteudo = tweet.find('div', {'class': 'css-901oao r-1re7ezh r-1qd0xha r-n6v787 r-16dba41 r-1sf4r6n r-bcqeeo r-qvutc0'}).text
        data = tweet.find('time')['datetime']

        latest_tweets_list.append([usuario, conteudo, data])

    df = pd.DataFrame(top_tweets_list, columns=['author', 'text', 'data'])
    df.head(10)
    df.to_csv('./data/twitter/top_tweets.csv')

    df = pd.DataFrame(latest_tweets_list, columns=['author', 'text', 'data'])
    df.head(10)
    df.to_csv('./data/twitter/latest_tweets.csv')

# Substituir 'python' pelo termo de pesquisa desejado
obter_tweets(num_tweets=50)
