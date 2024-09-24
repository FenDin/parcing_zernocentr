import requests
from bs4 import BeautifulSoup

name_product = []
date = []
price_for_ton = []
region = []
city = []
seller = []
phone = []
website = []

url = 'https://zernocentr.ru/ad/cat/1'
headers = {'User-Agent': 'Mozilla/5'}
links = set()
response = requests.get(url, headers=headers)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')

if response.status_code == 200:
    anchor_elements = soup.find_all('a')
    for element in anchor_elements:
        href = element.get('href')
        if href is not None and href.startswith("/ad/node/"):
            links.add(href)
    print(links)

    while links:
        mini_url = links.pop()
        url2 = 'https://zernocentr.ru' + mini_url
        response2 = requests.get(url2, headers=headers) 
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        if response2.status_code == 200:
            if soup2.find('h1', class_='page_header'):
                name_product.append(soup2.find('h1', class_='page_header').get_text(strip=True))
                print(name_product[-1])  # Печатаем последний добавленный элемент

            strong_tag = soup2.find('strong', class_='text-danger')
            if strong_tag:
                price_text = strong_tag.get_text(strip=True).replace('₽', '').replace(' ', '')  # Удаляем символы
                if price_text.isdigit():  # Проверяем, что строка состоит только из цифр
                    price_value = int(price_text) * (1000 if soup2.find('div', class_='double-field-second').get_text(strip=True) == 'тонну' else 1)
                    price_for_ton.append(price_value)  
                else:
                    print(f"Не удалось преобразовать '{price_text}' в число.")

            print(price_for_ton[-1] if price_for_ton else "Цена не найдена.")  # Печатаем последнюю добавленную цену

            region.append(soup2.find('a').get('datatype'))  
            print(region[-1])  # Печатаем последний добавленный элемент

            city.append(soup2.find('div', class_='field-item even').get_text(strip=True))  
            print(city[-1])  # Печатаем последний добавленный элемент

            seller.append(soup2.find('span', class_='glyphicon mini-icon glyphicon-user').get_text(strip=True))  
            print(seller[-1])  # Печатаем последний добавленный элемент

            phone.append(soup2.find('span', class_='glyphicon mini-icon glyphicon-phone-alt').get_text(strip=True))  
            print(phone[-1])  # Печатаем последний добавленный элемент

            website.append(soup2.find('a', href=True).get('href'))  
            print(website[-1])  # Печатаем последний добавленный элемент

            print(' ')
else:
    print("Ошибка")




