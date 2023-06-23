"""Currency Exchange Calculator
Author: Pedro
Last update: 29.03.2023

One of my self learning, small projects.
Still trying to improve. Any comments welcome :)
"""

#functions.py - all functions used in main()
from functions import *

#currencies.json - storing currencies used in calculator.
json_file = 'currency_exchange/currencies.json'

def main():
    """Calculator main body."""
    currency_dict = check_if_json_file_exists(json_file)

    welcome_message()

    for currency in currency_dict.keys():
        show_currencies(currency, currency_dict)

    if update_online_question(): 
        update_currencies(currency_dict)
        for currency in currency_dict.keys():
            show_currencies(currency, currency_dict)

    show_options(currency_dict)
    counter = 0

    while True:

        currency = input_currency()
        if currency in get_options(currency_dict):

            show_currencies(currency, currency_dict)
            change_currencies(currency, currency_dict)
            show_currencies(currency, currency_dict)

            next = True
            while (next):
                currnecy_exchange(currency, currency_dict)
                next = exchange_another_question(currency, currency_dict, next)

        elif currency == "q" or currency == "quit" or currency == "n" or currency == "no":
            print("Ok. Quit.\nSaving changes in currencies.json", end='.. ')
            save_currencies(json_file, currency_dict)
            print("OK")
            break

        else:
            print("\nWrong answer.")
            counter = counter + 1
            if counter == 3:
                print("")
                show_options(currency_dict)
                counter = 0

main()