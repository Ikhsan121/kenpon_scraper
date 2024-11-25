from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from time import sleep

def date_list(initial_date, final_date):
     with sync_playwright() as p:
        date_range_is = []
        initial_url_date = f'https://kenpom.com/fanmatch.php?d={initial_date}-11-01'
        final_url_date = f'https://kenpom.com/fanmatch.php?d={final_date}-04-29'
        browser = p.chromium.launch(headless=True)
        ua = 'Mozilla/5.0 (Linux; U; Android 9; es-us; Redmi Note 7 Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/12.1.7-g'
        page = browser.new_page(user_agent=ua)
        # login
        is_logged_in = False
        while not is_logged_in:
            try:
                print('Log in to get list of game\'s date...')
                page.goto("https://kenpom.com/index.php")
                page.get_by_placeholder('E-mail').fill('danielmmaggin@gmail.com')
                page.get_by_placeholder('Password').fill('12345678')
                page.get_by_text('Login!').click()
                is_logged_in = True
            except:
                is_logged_in = False

        # Go to page to get game start date
        is_page_opened = False
        while not is_page_opened:
            try:
                page.goto(initial_url_date)
                page_content = page.content()
                soup = BeautifulSoup(page_content, 'html.parser')
                header = soup.find('div', id='content-header')
                temp_day = list(header.find_all('a')[-1].text.split('/')[-1])
                if temp_day[0] == '0':
                    b = int(temp_day[1]) - 1
                    day_i = '0' + str(b)
                else:
                    b = int(temp_day[0] + temp_day[1]) - 1
                    if b < 10:
                        day_i = '0' + str(b)
                    else:
                        day_i = str(b)
                month_i = header.find_all('a')[-1].text.split('/')[0]
                year_i = initial_url_date.split("=")[-1].split("-")[0]
                is_page_opened = True
            except:
                print('Retry login for date...')
                page.goto("https://kenpom.com/index.php")
                page.get_by_placeholder('E-mail').fill('danielmmaggin@gmail.com')
                page.get_by_placeholder('Password').fill('12345678')
                page.get_by_text('Login!').click()

        # Go to page to get the game ends date
        page.goto(final_url_date)
        sleep(1)
        page_content = page.content()
        soup = BeautifulSoup(page_content, 'html.parser')
        header = soup.find('div', id='content-header')
        temp_day = list(header.find_all('a')[-1].text.split('/')[-1])
        if temp_day[0] == '0':
            b = int(temp_day[1]) + 1
            if b >= 10:
                day_f = str(b)
            else:
                day_f = '0' + str(b)
        else:
            b = int(temp_day[0] + temp_day[1]) + 1
            day_f = str(b)

        month_f = header.find_all('a')[-1].text.split('/')[0]
        year_f = final_url_date.split("=")[-1].split("-")[0]
        date_range_is.append(year_i + "-" + month_i + "-" + day_i)
        date_range_is.append(year_f + "-" + month_f + "-" + day_f)
        # Create list of date between those two dates
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(date_range_is[0], date_format)
        end_date = datetime.strptime(date_range_is[1], date_format)

        date_lists = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        date_list_str = [date.strftime(date_format) for date in date_lists]
        browser.close()
     return date_list_str






