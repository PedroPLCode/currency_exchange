"""All functions used in currency_exchange.py
Author: Pedro
Last update: 29.03.2023
"""

import sys, requests, json

YOUR_API_KEY = 'XXX'

def check_if_json_file_exists(filename):
    """Checks if json file exists."""
    currency_dict = get_stored_currencies(filename)
    if currency_dict:
        print("\nFile currencies.json OK")
        return currency_dict
    else:
        print("\nCurrency Exchange Calculator.\n"
              "FATAL ERROR: File currencies.json NOT FOUND OR BROKEN.\n"
              "Check do you have good currencies.json file in currency_exchange directory.\n")
        sys.exit()
        

def get_stored_currencies(filename):
    """Get stored currencies from json file if available."""
    try:
        with open(filename) as f_obj:
            currency_dict = json.load(f_obj)
    except FileNotFoundError:
        return None
    except json.decoder.JSONDecodeError:
        print("\nCurrency Exchange Calculator.\n"
              "ERROR. currencies.json file looks broken.")
        return False
    else:
        return currency_dict


def save_currencies(filename, dict):
    """Save currencies in json file"""
    with open(filename, 'w') as f_obj:
        json.dump(dict, f_obj)
    return dict


def show_currencies(currency, dict):
    """"Shows actual currencies for currency, taken from currencies dictionary"""
    print("\nActual currencies:")
    for key, values in dict.items():
        for key_curr, val_curr in values.items():
            if currency == key:
                print(f"Currency {key.upper()} / {key_curr.upper()}: {round(val_curr, 2)}")


def update_online_question():
    """Asks user if he wants do update currencies online using API."""
    while True:    
        update = str(input("\nDo you want to get latest currencies from API?\nInternet connection required: y / n: "))
        update = update.strip().lower()

        if update == 'y' or update == 'yes':
            print("\nOk. Currencies will be updated.")
            return True
        elif update == 'n' or update == 'no':
            print("\nOk. Currencies not updated.")
            return False
        else:
            print("\nWrong answer. Try again.")
            continue


def update_currencies(dict):
    """Updates currencies using API"""
    for key, values in dict.items():

        print(f"Updating {key.upper()} currencies.. \nStarting request API", end='..')
        url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/latest"
        querystring = {"base": str(key.upper())}
        headers = {
	        "X-RapidAPI-Key": f"{YOUR_API_KEY}",
	        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
        }
        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            response_dict = {}
            response_dict = response.json()
            print("OK")

            for key_curr, val_curr in values.items():
                for curr_online in response_dict['rates'].keys():
                    if curr_online.lower().strip() == key_curr:

                        print(f"Updating {key.upper()} / {key_curr.upper()} currency", end='...')
                        new = response_dict['rates'][key_curr.upper()]
                        values[key_curr] = round(new, 2)
                        succes = True
                        print("OK")
        except requests.ConnectionError:
            print("ERROR. ConnectionError. Coundn't connect to API. Currencies not changed.")
            succes = False
        except KeyError:
            print(f"ERROR. Api KeyError. Couldn't find {key.upper()} in API 'rates'.")
            succes = False
    if succes:        
        print("\nCurrencies succesfully updated.")
    if not succes:
        print("\nERROR.\nCURRENCIES NOT UPDATED.")


def input_currency():
    """Gets currency input from user."""
    currency = str(input("\nEnter choosen currency or Q to Quit: "))
    currency = currency.lower().strip()
    return currency


def change_currencies(currency, dict):
    """Allows to change choosen currency in dictionary"""
    for key, values in dict.items():
        for key_curr, val_curr in values.items():
            if currency == key:
                change_single_currency(key, key_curr, values)


def change_single_currency(key, key_curr, values):
    """Single currency exchange mechanism."""
    while True:
        change = str(input(f"\nDo you want to change {key.upper()} / {key_curr.upper()} currency? "
                           "Answer y / n  "))
        change = change.lower().strip()

        if change == "y" or change == "yes":
            new = input(f"Enter new {key.upper()} / {key_curr.upper()} currency: ")
            new = replace_to_comma(new)

            if check_input_type(new):
                continue
            else:
                new = float(new)

            if new < 0:
                print(f"\nWrong. New {key.upper()} / {key_curr.upper()} currency can't be lower than 0"
                      "\nDidn't change.")
                continue

            if round(new, 2) == 0:
                print(f"\nWrong. New {key.upper()} / {key_curr.upper()} currency can't be 0"
                      "\nDidn't change.")
                continue

            values[key_curr] = round(new, 2)
            print(
                f"\nCurrency {key.upper()} / {key_curr.upper()} changed to {str(round(new, 2))}")
            break

        elif change == "n" or change == "no":
            print(f"\nCurrency {key.upper()} / {key_curr.upper()} not changed.")
            break

        else:
            print(
                f"\nWrong answer. Currency {key.upper()} / {key_curr.upper()} not changed.")


def amount_input(currency):
    """Get amount input from user."""
    while True:
        amount = input(f"\nEnter {(currency.upper())} amount to exchange: ")
        amount = replace_to_comma(amount)

        if check_input_type(amount):
            continue
        else:
            amount = float(amount)
            if amount < 0.1:
                print(f"Wrong. You Can't exchange less than 0.1 {currency.upper()}.")
                continue
            break
    return amount


def currnecy_exchange(currency, dict):
    """Exchanges currencies and shows results."""
    amount = amount_input(currency)
          
    print("\nExchange results:")
    for key, values in dict.items():
        for key_curr, val_curr in values.items():
            if currency == key:
                result = float(amount) * float(val_curr)
                if result < 0.01:
                    result = str("less than 0.01")
                else:
                    result = round(result, 2)

                print(
                    f"{str(round(amount, 2))} {(currency.upper())} "
                    f"equals: {str(result)} {key_curr.upper()}")


def get_options(dict):
    """Gets possible currency options from currencies dictionary and returns as list"""
    options = []
    for key in dict.keys():
        options.append(key)
    return options


def show_options(dict):
    """Shows possible currency options from currencies dictionary"""
    print("\nWhat currency will we exchange?\n\nOptions:")
    for key in dict.keys():
        print(key.upper())


def exchange_another_question(currency, dict, next):
    """Questions if user wants to cexchange another currency?"""
    while True:

        next = str(input(
            f"\nDo you want to exchange another {currency.upper()} amount? "
            "Answer y / n "))
        next = next.lower().strip()

        if next == "y" or next == "yes":
            print("Ok. Let's count again.")
            next = True
            return next

        elif next == "n" or next == 'no':
            print("\nOk. Do you want to count another currency?\n")
            show_options(dict)
            next = False
            return next

        else:
            print("\nWrong answer. Please answer y / n")


def check_input_type(input):
    try:
        input = float(input)
        return False
    except ValueError:
        try:
            input = int(input)
            return False
        except ValueError:
            print(f"\nInput {input} is not a correct number. Looks like string."
                   "\nPlease try again.")
            return True
    except TypeError:
        print("\nYour input is not a correct number."
                   "\nPlease try again.")
        return True


def replace_to_comma(input):
    """Converts entered decimals with ',' to floats with '.' if possible.
    Second version. Using this function instead of convert_input_to_float()."""
    converted = input.replace(',', '.')
    try:
        converted = float(converted) 
        return converted
    except ValueError:
        pass
    return input

def convert_input_to_float(input): # NOT IN USE.
    """Converts entered decimals with ',' to floats with '.' if possible.
    First version - working good but too complicated. Now using replace_to_comma() instead."""
    if ',' in input:
        splitted = input.split(',')

        if len(splitted) == 2:
            converted = (splitted[0]+'.'+splitted[1])
            try:
                converted = float(converted)
                return converted
            except ValueError:
                pass
                return input

    else:
        return input


def welcome_message():
    """Shows welcome message."""
    print("\n-----------------------------------------\n"
      "-----------Currency Exchange-------------\n"
      "---------------Calculator----------------\n"
      "---------------------------------pedro-v5")