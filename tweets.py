from selenium import webdriver
from bs4 import BeautifulSoup
import time

def obter_tweets(termo_pesquisa, num_tweets=10):
    url = f'https://twitter.com/search?q={termo_pesquisa}&src=typed_query&f=live'

    # Configurar o navegador
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)  # Você precisa ter o ChromeDriver instalado e no PATH
    driver.get(url)

    # Rolar a página para baixo para carregar mais tweets
    for _ in range(num_tweets // 10):  # 10 tweets são carregados a cada rolagem
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Aguardar um breve período após cada rolagem

    # Obter o conteúdo da página
    page_content = driver.page_source
    driver.quit()

    # Analisar a página com BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    tweets = soup.find_all('div', {'data-testid': 'tweet'})

    for tweet in tweets:
        usuario = tweet.find('span', {'class': 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0'}).text
        conteudo = tweet.find('div', {'class': 'css-901oao r-1re7ezh r-1qd0xha r-n6v787 r-16dba41 r-1sf4r6n r-bcqeeo r-qvutc0'}).text
        data = tweet.find('time')['datetime']

        print(f'Usuário: {usuario}\nConteúdo: {conteudo}\nData: {data}\n{"="*50}')

# Substituir 'python' pelo termo de pesquisa desejado
obter_tweets('python', num_tweets=10)
