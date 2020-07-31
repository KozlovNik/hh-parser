from bs4 import BeautifulSoup
import requests
import html
link = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&fromSearch=true&items_on_page=100'
def get_html(url):
    headers = {'User-Agent': 'PostmanRuntime/7.26.1'}
    r = requests.get(link,headers=headers).text
    return BeautifulSoup(r)


html = get_html(link)
#number of pages
last_page = html.find_all('a', attrs={'data-qa':'pager-page'})[-1].text

#metro branches from 1 to 12
for i in range(1,13):
    print(i)
# def get_data():
#     vacancies = []
#     for el in soup.find_all(attrs={"class": "vacancy-serp-item"}):
#         try:
#             salary = el.find('span', attrs={'data-qa':'vacancy-serp__vacancy-compensation'}).text.replace('\xa0','')
#         except:
#             salary = ''

#         vacancies.append({
#             "title": el.find('span', class_='g-user-content').text,
#             "company": el.find('span', class_='g-user-content').text,
#             "link": el.find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text,
#             "salary": salary
#         })



# for vacancy in vacancies:
#     print(vacancy)