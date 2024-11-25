import json
import os
from time import sleep

from availability_test import similarity_test, similiarity_test_json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


final_data = []

def scraper(date, arena_dictionary):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        page = browser.new_page(user_agent=ua)
        is_logged_in = False
        while not is_logged_in:
            try:
                print("log in for scraper...")
                page.goto("https://kenpom.com/index.php")
                page.get_by_placeholder('E-mail').fill('danielmmaggin@gmail.com')
                page.get_by_placeholder('Password').fill('12345678')
                page.get_by_text('Login!').click()
                is_logged_in = True
            except:
                print('Retry login for scraper...')
                is_logged_in = False

        # Get teams arena dictionary
        teams_arena = arena_dictionary
        file_path = os.path.abspath('arena.json')
        with open(file_path, 'r') as file:
            arena_json = json.load(file)
        # go to the main page
        url = f'https://kenpom.com/fanmatch.php?d={date}'
        is_page_opened = False
        while not is_page_opened:
            try:
                page.goto(url)
                year = url.split("=")[1].split("-")[0]
                month = url.split("=")[1].split("-")[1]
                day = url.split("=")[1].split("-")[2]
                game_date = month + "/" + day + "/" + year
                is_page_opened = True
            except:
                print('Retry log in for scraper...')
                page.goto("https://kenpom.com/index.php")
                page.get_by_placeholder('E-mail').fill('danielmmaggin@gmail.com')
                page.get_by_placeholder('Password').fill('12345678')
                page.get_by_text('Login!').click()

        try:
            print(f"{date} start...")

            sleep(1)
            page_source = page.content()
            soup = BeautifulSoup(page_source, 'html.parser')
            table = soup.find('table', id='fanmatch-table').find('tbody')
            rows = table.find_all('tr')
        except AttributeError:
            print('Sorry, no games today. :(')
            rows = []

        for row in rows:
            try:
                data = []
                columns = row.find_all('td')
                game_column = columns[0]
                prediction_column = columns[1]
                location_column = columns[3]

                # Get team's name
                team_name = game_column.find_all('a')
                team1_name = team_name[0].text.strip()
                team2_name = team_name[1].text.strip()
                # Get team's prediction
                team1_kp = prediction_column.text.split("-")[0].split(" ")[-1].strip()
                team2_kp = prediction_column.text.split("-")[1].split(' ')[0].strip()
                # Get team's kp rank
                rank_temp = game_column.find_all('span', class_='seed-gray')
                team1_kp_rank = rank_temp[0].text.strip()
                team2_kp_rank = rank_temp[1].text.strip()
                # Get team in that will win
                prediction_column_text = prediction_column.text.strip()
                if team1_name in prediction_column_text:
                    winning_team = team1_name
                else:
                    winning_team = team2_name
                # Get predicted win
                predicted_win = prediction_column.text.split("(")[-1].replace("%", "").replace(")", "").strip()
                # Get team's score
                team1_score = game_column.text.strip().split(',')[0].split(" ")[-1].strip()
                team2_score = game_column.text.strip().split(',')[1].split(team2_name)[1].strip().split(' ')[0].strip()
                # Get possession
                possessions = game_column.text.split("[")[-1].split(']')[0].strip()
                # Get arena
                arena = location_column.find('a').text.strip()
                # Get city state
                location_column.find('a').decompose()
                city = location_column.text.strip()


                # Get Home or Away
                # Create a dictionary where team's name is the key and the arena are the value
                # later we will decide which one is the home or neutral

                team1_arena_dict = {team1_name: arena}
                team2_arena_dict = {team2_name: arena}
                team1_arena_dict_json = {team1_name: [arena, city]}
                team2_arena_dict_json = {team2_name: [arena, city]}
                team1_arena_similarity = similarity_test(arena_dict=teams_arena, team_arena_dict=team1_arena_dict)
                team2_arena_similarity = similarity_test(arena_dict=teams_arena, team_arena_dict=team2_arena_dict)
                team1_arena_similarity_json = similiarity_test_json(arena_json=arena_json, team_city_arena=team1_arena_dict_json)
                team2_arena_similarity_json = similiarity_test_json(arena_json=arena_json, team_city_arena=team2_arena_dict_json)

                if team1_arena_similarity > 0.68 or team1_arena_similarity_json > 0.68:
                    home_team_name = team1_name
                    away_team_name = team2_name
                    home_kp = team1_kp
                    away_kp = team2_kp
                    home_kp_rank = team1_kp_rank
                    away_kp_rank = team2_kp_rank
                    home_score = team1_score
                    away_score = team2_score
                    neutral = ''
                elif team2_arena_similarity > 0.68 or team2_arena_similarity_json > 0.68:
                    home_team_name = team2_name
                    away_team_name = team1_name
                    home_kp = team2_kp
                    away_kp = team1_kp
                    home_kp_rank = team2_kp_rank
                    away_kp_rank = team1_kp_rank
                    home_score = team2_score
                    away_score = team1_score
                    neutral = ''
                # if there is no team name in arena dictionary
                else:
                    home_team_name = team1_name
                    away_team_name = team2_name
                    home_kp = team1_kp
                    away_kp = team2_kp
                    home_kp_rank = team1_kp_rank
                    away_kp_rank = team2_kp_rank
                    home_score = team1_score
                    away_score = team2_score
                    neutral = '1'
                data.append(game_date)
                data.append(home_team_name)
                data.append(away_team_name)
                data.append(home_kp)
                data.append(away_kp)
                data.append(home_kp_rank)
                data.append(away_kp_rank)
                data.append(winning_team)
                data.append(predicted_win)
                data.append(home_score)
                data.append(away_score)
                data.append(possessions)
                data.append(arena)
                data.append(city)
                data.append(neutral)
                final_data.append(data)
            except:
                pass
        browser.close()
    return final_data


