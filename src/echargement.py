#!/usr/bin/env python

import json
import os


class Echargement():

    def __init__(self,
                 fullname: str,
                 badge: str,
                 url: str,
                 json_path: str
                 ):

        self.fullname = fullname
        self.badge = badge
        self.json_path = json_path
        self.url = url

    def get_account_page(self):
        import mechanize
        """
        Get account page
        """
        browser = mechanize.Browser()
        browser.open(self.url)
        browser.select_form(nr=0)
        browser.form['badge_number'] = self.badge
        browser.form['badge_nom'] = self.fullname
        browser.submit()

        return browser.response().read()

    def find_account_balance(self, html):
        from bs4 import BeautifulSoup
        import re
        """
        Parse amount
        """
        soup = BeautifulSoup(html, features="html5lib")
        str_to_search = "Solde disponible sur votre compte"

        for row in soup.findAll('tr'):
            aux = row.findAll('td')
            if str_to_search in aux[0].text:
                balance = re.sub('[^0-9,]', "", aux[1].text)
                break
        return float(balance.replace(',', '.'))

    def get_account_balance(self):
        """
        Get account amount
        """
        html = self.get_account_page()
        return self.find_account_balance(html)

    def save_account_balance(self, balance):
        import datetime

        yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")
        balance_history = self.get_account_balance_history()
        balance_history[yesterday] = balance

        with open(self.json_path, "w") as jsonFile:
            json.dump(balance_history, jsonFile,  ensure_ascii=False, indent=4)

    def get_account_balance_history(self):

        with open(self.json_path, "r") as jsonFile:
            data = json.load(jsonFile)

        return data


def script_args():
    import argparse
    args = argparse.ArgumentParser(
        description="Get your balance and save it to json"
        )
    args.add_argument(
        "--badge",
        help="Your badge number",
        required=True
        )
    args.add_argument(
        "--fullname",
        help="Your fullname (DOE John)",
        required=True
        )
    args.add_argument(
        "--url",
        help="Url of your echargement (specific for each company)",
        required=True
        )
    args.add_argument(
        "--save-path",
        help="Json file path",
        default="balance.json"
        )

    return args.parse_args()


def main():
    args = script_args()

    # If save_path file doesn't exist, create it
    if not os.path.exists(args.save_path):
        with open(args.save_path, 'w+') as file:
            file.write('{}')

    echargement = Echargement(
        args.fullname,
        args.badge,
        args.url,
        args.save_path
        )

    balance = echargement.get_account_balance()
    echargement.save_account_balance(balance)


if __name__ == "__main__":
    main()
