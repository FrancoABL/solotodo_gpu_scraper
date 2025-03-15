from time import sleep
import json 
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Configurar las opciones del navegador
options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


url ='https://www.solotodo.cl/monitors?refresh_rate_start=110648'
#url = 'https://www.solotodo.cl/video_cards?gpu_families=106058&gpu_lines=887442&gpu_lines=819952&gpu_lines=1240913&gpu_lines=1651050&gpu_lines=2014763&page=1'
driver.get(url)

def scrapeo():
    for x, y in zip(nombres, precios):
        dic_gpu[x.text] = y.text  # Agrega los nombres

    with open('dic_gpu.json', 'w') as json_file:
        json.dump(dic_gpu, json_file)

boton = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/main/div/div/div[3]/div[3]/div/div/div[3]/button[3]")

#scrapeo
dic_gpu = {}
for i in range(10):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    nombres = soup.find_all(class_="MuiTypography-h5")
    precios = soup.find_all(class_="MuiTypography-h2")
    link = soup.find_all("a", {"class": "href-link"})
    scrapeo()
    print(dic_gpu)
    print(link)
    sleep(3)
    try:
        boton = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/main/div/div/div[3]/div[3]/div/div/div[3]/button[3]")
        boton.click()
    except:
        break

sleep(3)

#para verificar la ultima pagina
soup = BeautifulSoup(driver.page_source, 'html.parser')
nombres = soup.find_all(class_="MuiTypography-h5")
precios = soup.find_all(class_="MuiTypography-h2")
scrapeo()
print(dic_gpu)

driver.quit()

with open('dic_gpu.json', 'r') as json_file:
    data = json.load(json_file)

df = pd.DataFrame(list(data.items()), columns=['Nombre', 'Precio'])
print(df)