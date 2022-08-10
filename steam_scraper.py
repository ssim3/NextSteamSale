"""
Created on Wed Aug 10 11:17:12 2022

@author: Tristan Sim
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


def welcome():
    print("================================================")
    print('''                                                       
     _____         _   _____               _____     _     
    |   | |___ _ _| |_|   __|___ _____ ___|   __|___| |___ 
    | | | | -_|_'_|  _|  |  | .'|     | -_|__   | .'| | -_|
    |_|___|___|_,_|_| |_____|__,|_|_|_|___|_____|__,|_|___|
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

        GetGameData() if option == 1 else print("Thank you for using...")
        
    except (ValueError, AssertionError):
        print("Invalid input!")
        options()
  
def GetGameData():
    
    print("\n============================")
    print("The program will visit steamDB and download a csv file into your current directory")
    print("When the website is loaded, a captcha will have to be manually completed (15 Seconds)...")
    print("============================")
    
    
    game = input("Enter the name of the game: ")
    

    'Gets the chrome webdrive that is installed on working directory'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)

    'Visits isthereanydeal.com to see price history, waits for 5 seconds for site to load'
    driver.get('https://isthereanydeal.com/')
    time.sleep(3)
    
    '''
    Searches up the users game of choice on the website
    '''
    search = driver.find_element(By.ID, "searchbox")
    search.send_keys(game)
    search.submit()

    game = driver.find_element(By.CLASS_NAME, "card__img").click()

    time.sleep(10)

   
        

def main():
    welcome()
    options()
    
main()
    
