import json
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


path_chrome = ChromeDriverManager().install()
options = ChromeOptions()
# options.add_argument('--headless')
browser_service = Service(executable_path=path_chrome)
browser = Chrome(service=browser_service, options=options)
browser.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')


articles_tag = browser.find_elements(By.CLASS_NAME, 'vacancy-serp-item__layout')

key_words = ["Django", "Flask"]
parsed_data = []

for article_tag in articles_tag:
    a_tag = article_tag.find_element(by=By.TAG_NAME, value='a')
    link_absolute = a_tag.get_attribute('href')

    try:
        vacancy = article_tag.find_element(by=By.CLASS_NAME, value='bloko-header-section-2')
        salary_text = vacancy.text
    except:
        salary_text = 'зарплата не указана'
    parsed_data.append({
        'link': link_absolute,
        'salary': salary_text.replace('\u202f', ' '),
        'name_company': '',
        'location': ''
    })


new_parsed_data = []
for parsed_article in parsed_data:
    browser.get(parsed_article['link'])

    try:
        article_tag = browser.find_element(by=By.CLASS_NAME, value='g-user-content')
        articles_text = article_tag.text
    except:
        articles_text = 'описание не указано'

    if key_words[0] in articles_text and key_words[1] in articles_text:

        try:
            company_location_tag = browser.find_element(by=By.CLASS_NAME, value='vacancy-creation-time-redesigned')
            company_location_text = company_location_tag.text.split()[-1]
        except:
            company_location_text = 'локация не указана'

        try:
            name_tag = browser.find_element(by=By.CLASS_NAME, value='vacancy-company-name')
            company_name_text = name_tag.text.strip()
        except:
            company_name_text = 'компания не указана'

        parsed_article['name_company'] = company_name_text
        parsed_article['location'] = company_location_text

        new_parsed_data.append(parsed_article)
parsed_data = new_parsed_data


with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, indent=4, ensure_ascii=False)

print('Данные добавлены в файл')
