import requests
from bs4 import BeautifulSoup

links = [] #Концы ссылок, которые ведут к разным объявлениям
Links = [] #Полные ссылки

name_product = [] #yes
date = []
price_for_ton = [] #yes
region = [] #yes
city = [] #yes
seller = [] #yes
phone = [] # yes
website = [] # yes

number = 0
date_num = 0

url = 'https://zernocentr.ru/ad/cat/1'
headers = {'User-Agent': 'Mozilla/5'}
links_ = set() #Множество, при помощи которого будет происходить фильтрация ссылок
               #(Во множество попадает только уникаьное значение, которое и запишем в список)
response = requests.get(url, headers=headers)
print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')

if response.status_code == 200:
    num = 0 #Счётчик для списка ссылок
    anchor_elements = soup.find_all('a')
    for element in anchor_elements:
        len1 = len(links_)
        href = element.get('href')
        if href is not None and href.startswith("/ad/node/"):
            links_.add(href)
            len2 = len(links_)
            if (len2 > len1):
                links.append(href) 
            num += 1           
    print(links)

    date_elements = soup.find_all('span', class_ = 'date-display-single')
    for element in date_elements:
        date.insert(date_num, element.text)
        date_num += 1
    print(' ')

    for link in links:
        print("Объявление " + str(number+1))
        mini_url = link
        url2 = 'https://zernocentr.ru' + mini_url
        response2 = requests.get(url2, headers=headers) 
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        if response2.status_code == 200:
            Links.append(url2)
            if soup2.find('h1', class_='page-header'):
                name_product.insert(number, (soup2.find('h1', class_='page-header').get_text(strip=True)))
                print(name_product[number])  

            print("Дата выставления: " + date[number])            
            print("Ссылка: " + Links[number])

            strong_tag = soup2.find('strong', class_ = 'text-danger')
            if strong_tag:
                price_text = strong_tag.get_text(strip=True)
                price_for_ton.insert(number, (price_text))
                try:
                    soup2.find('div', class_ = 'double-field-second').get_text
                except AttributeError:
                    att = "Договорная"
                    print("Цена: " + att)
                else:
                    if soup2.find('div', class_ = 'double-field-second').text == "тонну":
                        print("Цена: " + (price_for_ton[number] + " за тонну"))  
                    if soup2.find('div', class_ = 'double-field-second').text == "килограмм": 
                        print("Цена: " + str(float(price_for_ton[number])*1000) + " за тонну")

            if soup2.find('div', class_="panel-pane pane-entity-field pane-node-field-ads-grain-region prop-dotted") is None:
                print("Регион не указан")
            else:
                region.insert(number, (soup2.find('div', class_="panel-pane pane-entity-field pane-node-field-ads-grain-region prop-dotted").text))
                print("Регион: " + region[number].replace("Регион купли/продажи/услуги: " , "").strip())  

            if soup2.find('div', class_="panel-pane pane-entity-field pane-node-field-ads-grain-town prop-dotted") is None:
                print("Город не указан")
            else:    
                city.insert(number, (soup2.find('div', class_="panel-pane pane-entity-field pane-node-field-ads-grain-town prop-dotted").text))  
                print("Нас.пункт: " + city[number].replace("Нас. пункт купли/продажи/услуги: ", "").strip())

            if soup2.find('p', title = 'Контактное лицо') is None:
                print("Продавец не указан")
            else:
                seller.insert(number, (soup2.find('p', title = 'Контактное лицо' ).text))
                print("Продавец: " + seller[number])  
            
            if soup2.find('p', title = 'Телефон') is None:
                print("Телефон не указан")
            else:
                 phone.insert(number, (soup2.find('p', title = 'Телефон').text))
                 print("Телефон: " + phone[number])     

            if soup2.find('a', targer = '_blank') is None:
                print("Сайт не указан")
            else:
                website.insert(number, (soup2.find('a', targer = '_blank').text))
                print("Сайт: " + website[number])
              
            print(' ')
            number += 1 #Счётчик объявлений и индекса в списках
else:
    print("Ошибка соединения с сайтом")




