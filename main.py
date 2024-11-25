from arena import get_arena
from get_date import date_list
import pandas as pd
from scraper import scraper


columns_title = ['Game Date', 'Home_team', 'Away_Team', 'Home_KP', 'Away_KP',
                 'Home_KP_Rank', 'Away_KP_Rank', 'Predicted_W%_team', 'Predicted_W%', 'Home_Score',
                 'Away_Score', 'Possessions', 'Arena', 'City_State', 'Is Neutral']

def main():
    initial_year = input("Input season starting year: ")
    final_year = int(initial_year) + 1
    date_range = date_list(initial_date=int(initial_year), final_date=final_year)
    arena_dict = get_arena(int(initial_year))
    for i in date_range:
        final_data_to_save = scraper(date=i, arena_dictionary=arena_dict)
        df_available = pd.DataFrame(final_data_to_save, columns=columns_title)
        # Save dataframe into Excel file
        excel_file_path = f'season{initial_year}-{final_year}.xlsx'
        df_available.to_excel(excel_file_path, index=False)
        print(f'The result has been saved into: {excel_file_path}')


if __name__ == "__main__":
    main()
