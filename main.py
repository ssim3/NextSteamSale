import steam_scraper as ss

option = ss.main()

df = ss.get_game_data() if option == 1 else exit()

print(df.head(20))