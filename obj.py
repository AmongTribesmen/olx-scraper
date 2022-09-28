''' scraper object script:

scrapes data from any OLX website and stores the data
in a csv file matching the query name.


'''
import requests
from bs4 import BeautifulSoup
import logging
from time import sleep
import csv
from geopy.geocoders import Nominatim




geo = Nominatim(user_agent="<<city finder>>")

logging.basicConfig(level=logging.DEBUG,
format=' %(asctime)s - %(levelname)s - %(message)s')

class Scraper:

    def __init__(self, query, static_url):
        self.query = query
        self.links=[]
        self.static=static_url
        global url
        url = self.static+ '/en/ads/q-'+ query+'/'
        logging.debug(url)
        try:
            self.response = requests.get(url, timeout=10)
            self.content=self.response.content
            self.soup=BeautifulSoup(self.content, 'html.parser')
            logging.debug(self.response.status_code)
            if self.response.status_code != 200:
                print('%s returned status code %s, terminating.'%(url, self.response.status_code))
        except Exception as ex:
            print(str(ex))

    def write_csv(self, csvfile, Title, Description, Price, Location, long, lat, Username, User_join_date, Link):
        header = ['Title', 'Description', 'Price', 'City',
        'longitude', 'latitude', 'Username', 'User_join_date', 'Link']


        with open(csvfile, 'r+', encoding='UTF8') as f:
            writer = csv.writer(f)
            if ','.join(header) not in f.read():
                writer.writerow(header)
            writer.writerow([Title, Description, Price, Location, long, lat, Username, User_join_date, Link])


    def parse(self):

        a, b, domain_extention = self.static.partition('olx')
        csv_filename = domain_extention +' | ' +self.query + '.csv'

        with open(csv_filename, 'w') as tempvar:
            pass


        for I in range(len(self.links)):
            with open('links.txt', 'r+') as links_file:
                link = links_file.readlines()[I]

                sleep(2)
                try:
                    link_response=requests.get(link, timeout=10)
                    link_content=link_response.content
                    self.link_soup=BeautifulSoup(link_content, 'html.parser')
                    if link_response.status_code != 200:
                        print('%s returned status code %s, terminating.' %(link, link_response.status_code))
                except Exception as ex:
                    print(str(ex))

                #find the listing title:
                Title = self.link_soup.find('h1', {'class':"a38b8112"})
                logging.debug(Title)

                #find the item's description
                Description = self.link_soup.find('div', {'class': "_0f86855a"})
                logging.debug(Description.text)


                #find the item's price
                Price_unformatted = self.link_soup.find('div', {'class': "b44ca0b3"})
                x, y, Price = Price_unformatted.text.partition('Price')
                logging.debug(Price)


                #find the listing's location
                Location = self.link_soup.find('span', {'class':'_8918c0a8 fccf2e37'})
                x,y,Location = Location.text.partition(',')
                logging.debug(Location)

                geo_location = geo.geocode(Location)
                if geo_location != None:
                    location_long, location_lat = geo_location.longitude, geo_location.latitude
                else:
                    location_long, Location_lat = 'N/A', 'N/A'


                #find the OLX username and join date
                Username_and_date = self.link_soup.find('div', {'class':'_1075545d _6caa7349 _42f36e3b d059c029'})
                logging.debug(Username_and_date)
                logging.debug(type(Username_and_date))
                Username, x, Join_date = Username_and_date.text.partition("Member since")
                logging.debug(Username)
                logging.debug(Join_date)

                self.write_csv(csv_filename, Title.text, Description.text, Price, Location,
                location_long, location_lat, Username, Join_date, link)



    def get_links(self):
        pages = self.soup.find('div', {'class':"_2a1c1a09"})
        logging.debug('PAGES:' + pages.text)

        for item in self.soup.find_all('article'):
            a = item.find('a', {'href':True})
            self.links.append(self.static + a['href'] + '/')

        for I in range(1, len(pages.text)):
            page_url = url + '?page=' + str(I + 1)
            r = requests.get(page_url, timeout=10)
            c = r.content
            page_soup = BeautifulSoup(c, 'html.parser')

            for item in page_soup.find_all('article'):
                b = item.find('a', {'href':True})
                self.links.append(self.static + b['href'] + '/')



        with open('links.txt', 'w') as links_file:
            links_file.write('\n'.join(self.links))
