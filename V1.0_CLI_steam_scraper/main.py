import pandas as pd
import steam_scraper as ss
from datetime import date

ss.welcome()
option = ss.options()

while not option.isnumeric():
    print("invalid input! ")
    option = ss.options()
    

if int(option) == 1:
    df, game = ss.get_game_data() 
else:
   print("See you next time!")
   raise SystemExit(0)



df.Date = pd.to_datetime(df.Date, format='%Y%m%d')

month = date.today().month



''' Then, groups the data by months '''

df["Month"] = df.Date.dt.month
next_sales = df.groupby(["Month", "Price"]).Date.min()

''' Gets the rows of the next months dates '''
df = df.loc[df["Date"].isin(next_sales)].sort_values(by="Month", ascending=True)

''' If The month is december, goes to the next year '''
if month == 12:
    month = 1
    
''' Only gets the records after todays month '''
df = df.loc[df["Date"].dt.month > month]

''' 
    Gets the amount that the game is off by
    then removes all the rows where game does not have sale 
'''

df["Sale"] = df["Regular Price"] - df["Price"]

df = df.drop(df[df["Sale"] == 0].index)


''' Groups the rows by month, then gets the cheapest price '''
cheapest_sales = df.groupby("Month").Price.min()


'''
    Prints all the dates where the games are on sale
'''

print("\nAll sales that will occur after {}".format(date.today()))

print("---------------------------------------------------------------")
df["Date"] = df["Date"].dt.strftime("%m-%d")
df = df.set_index("Date")
if not df.empty:
    print(df)
else:
    print("No records of sales for {}".format(game))
    
print("---------------------------------------------------------------")


'''
    Prints all the dates where the games are on sale, grouped by month
'''

print("\nMonths and lowest prices for sales that will occur after {}:".format(date.today()))

print("---------------------------------------------------------------")
if not cheapest_sales.empty:
    print(cheapest_sales)
else:
    print("No records of sales for {}".format(game))

print("---------------------------------------------------------------")
