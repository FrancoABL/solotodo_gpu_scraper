from time import sleep
import json 
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

#url ='https://www.solotodo.cl/monitors?refresh_rate_start=110648'
url = 'https://www.solotodo.cl/video_cards?gpu_families=106058&gpu_lines=887442&gpu_lines=819952&gpu_lines=1240913&gpu_lines=1651050&gpu_lines=2014763&page=1'
driver.get(url)

def scrapeo():
    for x, y, z in zip(nombres, precios, links):  
        dic_gpu[x.text] = {'Precio': y.text, 'Link': z} 

    with open('dic_gpu.json', 'w') as json_file:
        json.dump(dic_gpu, json_file)

    df = pd.DataFrame.from_dict(dic_gpu, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['Nombre', 'Precio', 'Link']
    df.to_csv('dic_gpu.csv', index=False)

boton = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/main/div/div/div[3]/div[3]/div/div/div[3]/button[3]")


dic_gpu = {}
for i in range(10):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    nombres = soup.find_all(class_="MuiTypography-h5")
    precios = soup.find_all(class_="MuiTypography-h2")
    product_divs = soup.find_all("div", class_="css-1g4yje1")
    
    links = [None]  # Agrega un enlace vacío en la posición 0
    for div in product_divs:
        a_tags = div.find_all("a", href=True)
        for a_tag in a_tags:
            full_url = "https://www.solotodo.cl" + a_tag["href"]
            links.append(full_url)
    
    scrapeo()
    print(dic_gpu)
    print(links)
    sleep(3)
    try:
        boton = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/main/div/div/div[3]/div[3]/div/div/div[3]/button[3]")
        boton.click()
    except:
        break

sleep(3)


soup = BeautifulSoup(driver.page_source, 'html.parser')
nombres = soup.find_all(class_="MuiTypography-h5")
precios = soup.find_all(class_="MuiTypography-h2")
product_divs = soup.find_all("div", class_="css-1g4yje1")

links = ["https://www.solotodo.cl"]  
for div in product_divs:
    a_tags = div.find_all("a", href=True)
    for a_tag in a_tags:
        full_url = "https://www.solotodo.cl" + a_tag["href"]
        links.append(full_url)

scrapeo()
print(dic_gpu)

driver.quit()

with open('dic_gpu.json', 'r') as json_file:
    data = json.load(json_file)

df = pd.DataFrame(list(data.items()), columns=['Nombre', 'Precio'])
print(df)