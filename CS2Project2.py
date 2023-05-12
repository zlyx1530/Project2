#this program requires requests, bs4/BeautifulSoup, csv, and os.path/exists
import requests
from bs4 import BeautifulSoup
import csv
from os.path import exists
from datetime import date

def main() -> None:
    '''
    This is the main function that does all tasks. First asking for user input then webscraping
    weather.com for values. Printing those values in readable format and adding them to 'projoutput.csv'
    for a file/weather history.
    :return: -> None
    '''
    # Ask the user for a ZIP code some zip codes are weird, so I left it as open input
    #while len(zip_code) != 5:
    zip_code = input("Please enter your ZIP code: ")
    boo = True
    # Create the URL for the weather page using the ZIP code
    url = f"https://weather.com/weather/today/l/{zip_code}:4:US"

    # Send a GET request to the URL and get the response
    response = requests.get(url)
    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the current temperature
    temp_elem = soup.find('span', {'class': 'CurrentConditions--tempValue--MHmYY'})
    temp = temp_elem.text if temp_elem else "N/A"

    # Find the current weather description
    cond_elem = soup.find('div', {'class': 'CurrentConditions--phraseValue--mZC_p'})
    condition = cond_elem.text.strip() if cond_elem else "N/A"

    # Find the location
    loc_elem = soup.find('h1', {'class': 'CurrentConditions--location--1YWj_'})
    location = loc_elem.text if loc_elem else "N/A"

    # Find the time
    time_elem = soup.find('span', {'class': 'CurrentConditions--timestamp--1ybTk'})
    time = time_elem.text.strip() if time_elem else 'N/A'

    #def lists and date
    today = str(date.today()) + ' '+ time
    Fieldnames = ['Date', 'Location', 'Temperature', 'Condition']
    fields = [today, location, temp, condition]

    # Print the current weather informat1234ion
    if temp != "N/A":
        print(f"{date.today()} Current weather in {location} {time}: {temp} and {condition}")
    else:
        boo = False
        print("Sorry, could not get the weather information for that location.")
    if boo:
        if exists('weather.csv'):
            with open('weather.csv', 'a') as output:
                writer = csv.writer(output, delimiter=',', lineterminator='\n')
                writer.writerow(fields)
        else:
            with open('weather.csv', 'w') as output:
                writer = csv.writer(output, delimiter=',', lineterminator='\n')
                writer.writerow(Fieldnames)
                writer.writerow(fields)

if __name__ == '__main__':
    main()