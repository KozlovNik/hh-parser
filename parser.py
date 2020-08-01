from bs4 import BeautifulSoup
import requests
import time
import csv

link = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&items_on_page=100&search_period=1'


def save(vacancies, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("Вакансия", "Компания", "Ссылка", "Зарплата"))

        for vacancy in vacancies:
            try:
                writer.writerow((
                    vacancy['title'],
                    vacancy['company'],
                    vacancy['link'],
                    vacancy['salary']
                ))
            except UnicodeEncodeError:
                continue


def get_html(url):
    headers = {'User-Agent': 'PostmanRuntime/7.26.1'}
    r = requests.get(url, headers=headers).text
    return BeautifulSoup(r)


def get_vacancies(soup):
    vacancies = []
    for el in soup.find_all(attrs={"class": "vacancy-serp-item"}):
        # try to parse salary
        try:
            salary = el.find('span', attrs={
                             'data-qa': 'vacancy-serp__vacancy-compensation'}).text.replace('\xa0', '')
        except:
            salary = ''
        vacancies.append({
            "title": el.find('span', class_='g-user-content').text,
            "company": el.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text,
            "link": el.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href'],
            "salary": salary
        })
    return vacancies


# metro lines from 1 to 12 in search parameters
vacancies = []
for line in range(1, 13):
    soup = get_html(f'{link}&metro={line}')
    # Finds number of pages or sets the number as one
    try:
        number_of_pages = int(soup.find_all(
            'a', attrs={'data-qa': 'pager-page'})[-1].text)
    except IndexError:
        number_of_pages = 1
    for page in range(number_of_pages):
        soup = get_html(f'{link}&metro={line}&page={page}')
        time.sleep(1)
        data = get_vacancies(soup)
        vacancies.extend(data)


save(vacancies, 'vacs.csv')
