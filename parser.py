from bs4 import BeautifulSoup
import requests
import time
import csv

link = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&items_on_page=100&search_period=1'


def save(vacancies, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ("Вакансия", "Компания", "Ссылка", "Зарплата", "Метро"))

        for vacancy in vacancies:
            try:
                writer.writerow((
                    vacancy['title'],
                    vacancy['company'],
                    vacancy['link'],
                    vacancy['salary'],
                    vacancy['metro-station'],
                ))
            except UnicodeEncodeError:
                print('exception')


def get_html(url):
    headers = {'User-Agent': 'PostmanRuntime/7.26.1'}
    r = requests.get(url, headers=headers).text
    return BeautifulSoup(r, features="html.parser")


def isValidVacancy(title):
    for exclusion in exclusion_list:
        if exclusion.lower() in title.lower():
            return False
    return True


def get_vacancies(soup):
    vacancies = []
    for el in soup.find_all(attrs={"class": "vacancy-serp-item"}):
        # try to parse salary
        try:
            salary = el.find('span', attrs={
                             'data-qa': 'vacancy-serp__vacancy-compensation'}).text.replace('\xa0', '')
        except:
            salary = ''

        try:
            company = el.find(
                'a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
        except:
            company = ''

        try:
            metro_station = el.find('span', class_="metro-station").text
        except:
            metro_station = ''

        title = el.find('span', class_='g-user-content').text

        if not isValidVacancy(title):
            continue
        print(title)

        vacancies.append({
            "title": title,
            "company": company,
            "link": el.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href'],
            "salary": salary,
            "metro-station": metro_station
        })
    return vacancies


# metro lines from 1 to 12 in search parameters
vacancies = []
for page in range(40):
    soup = get_html(f'{link}&page={page}')
    # print(soup)
    time.sleep(1)
    data = get_vacancies(soup)
    vacancies.extend(data)


save(vacancies, 'vacs.csv')
