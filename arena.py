from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from time import sleep


def get_arena(year):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        page = browser.new_page(user_agent=ua)
        # login
        is_logged_in = False
        while not is_logged_in:
            try:
                print('Log in to retrieve list of arena...')
                page.goto("https://kenpom.com/index.php")
                page.get_by_placeholder('E-mail').fill('danielmmaggin@gmail.com')
                page.get_by_placeholder('Password').fill('12345678')
                page.get_by_text('Login!').click()
                is_logged_in = True
            except:
                print('Retry log in for arena...')
                is_logged_in = False
        # scrape arena
        is_page_opened = False
        while not is_page_opened:
            try:
                page.goto(f'https://kenpom.com/arenas.php?y={year}')
                sleep(1)
                page_source = page.content()
                soup = BeautifulSoup(page_source, 'html.parser')
                table = soup.find('table', id='ratings-table').find('tbody')
                rows = table.find_all('tr')
                is_page_opened = True
            except:
                page.goto("https://kenpom.com/index.php")
                page.get_by_placeholder('E-mail').fill('danielmmaggin@gmail.com')
                page.get_by_placeholder('Password').fill('12345678')
                page.get_by_text('Login!').click()

        team_list = []
        arena_list = []

        for row in rows:
            temp = []
            team_name = row.find_all('td')[1].text
            arena = row.find_all('td')[3].text.split("(")[0].strip()
            alt_arena = row.find_all('td')[4].text.split("(")[0].strip()
            temp.append(arena)
            temp.append(alt_arena)
            arena_list.append(temp)
            team_list.append(team_name)

        teams_arena = dict(zip(team_list, arena_list))
    return teams_arena
