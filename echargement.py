

class Echargement():

    def __init__(self,
                 badge_name,
                 badge_number):

        self.badge_name = badge_name
        self.badge_number = badge_number
        self.site_url = "https://www.e-chargement.com/api/libertis/"
        self.json_database = "balance.json"

    def get_account_page(self):
        import mechanize
        """
        Get account page
        """
        browser = mechanize.Browser()
        browser.open(self.site_url)
        browser.select_form(nr=0)
        browser.form['badge_number'] = self.badge_number
        browser.form['badge_nom'] = self.badge_name
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
                return re.sub('[^0-9,]', "", aux[1].text)

    def get_account_balance(self):
        """
        Get account amount
        """
        html = self.get_account_page()
        return self.find_account_balance(html)

    def save_account_balance(self, balance):
        import json
        import datetime

        date = datetime.datetime.now().strftime("%Y-%m-%d")

        with open(self.json_database, "r") as jsonFile:
            data = json.load(jsonFile)

        data[date] = balance

        with open(self.json_database, "w") as jsonFile:
            json.dump(data, jsonFile,  ensure_ascii=False, indent=4)

    def get_account_balance_history(self):
        import json
        with open(self.json_database, "r") as jsonFile:
            data = json.load(jsonFile)

        return data


