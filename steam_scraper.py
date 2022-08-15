"""
Created on Wed Aug 10 11:17:12 2022

@author: Tristan Sim
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


def welcome():
    print("================================================")
    print('''
 _____         _   _____ _                 _____     _     
|   | |___ _ _| |_|   __| |_ ___ ___ _____|   __|___| |___ 
| | | | -_|_'_|  _|__   |  _| -_| .'|     |__   | .'| | -_|
|_|___|___|_,_|_| |_____|_| |___|__,|_|_|_|_____|__,|_|___|

          ''')                                                    
    print("================================================")
    
    print("\nFind out when your favorite steam game will go on sale next!")

def options():
    print("\n=======================")
    print("1. Get Next Sale")
    print("2. Quit")
    print("=======================")
    
    try:
        option = int(input("\nOption: "))
        assert 1 <= option <= 2

        return option
        
    except (ValueError, AssertionError):
        print("Invalid input!")
        options()
  
def get_game_data():
    
    print("\n============================")
    print("The program will visit isthereanydeal.com to gather data on your game's steam sales.")
    print("Please do not touch the website while the programming is running...")
    print("============================")
    
    
    game = input("Enter the name of the game: ")
    

    'Gets the chrome webdrive that is installed on working directory'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    'Visits isthereanydeal.com to see price history, waits for 5 seconds for site to load'
    driver.get('https://isthereanydeal.com/')
    time.sleep(2)
    
    '''
    Searches up the users game of choice on the website
    '''
    search = driver.find_element(By.ID, "searchbox")
    search.send_keys(game)
    search.submit()

    time.sleep(1)

    try:
        driver.find_element(By.CLASS_NAME, "card__img").click()
    except:
        print("Game not found! Please reload the program...")
        exit()

    time.sleep(1)

    ''' Moves to the History tab '''
    try:
        history = driver.find_elements(By.CLASS_NAME, "gameNav__link")
        history[1].click()
    except:
        error()

    ''' Filters the page to show only steam prices'''
    driver.get(driver.current_url + "/?shop%5B%5D=steam")


    ''' Scrolls down the page to logs'''
    driver.execute_script("window.scrollTo(0, 2000);")

    '''Saving all the logs as a list...Using pandas now :D'''
    
    print("Getting information on {}...".format(game))

    logs = driver.find_elements(By.CLASS_NAME, "lg2__content")
    
    dates = []
    prices = []
    percentages = []
    regulars = []

    ''' 
        Loops through every price log, append the date, price and percentage off
        as separate lists.
    '''
    for i in logs:
        try:
            date = i.find_element(By.CLASS_NAME,"lg2__time-rel")
            dates.append("".join(date.text[:10].split("-")))

            price = i.find_element(By.CLASS_NAME, "lg2__price.lg2__price--new")
            prices.append(price.text)
            
            regular = i.find_element(By.CLASS_NAME, "lg2__price")
            regulars.append(regular.text)
            
        except:
            error()
    
    ''' Gets rid of empty dates created for some reason '''
    dates = [x for x in dates if x != ""]
    prices = [float(y[1:]) for y in prices if y != ""]
    regulars = [float(z[1:]) for z in regulars if z != ""]

    
    return pd.DataFrame({"Date": dates, "Price": prices, "Regular Price": regulars}), game
    


def error():
    print("You might be in the wrong page. Please reload the program...")
    exit()

def main():
    welcome()
    return options()
    
    
