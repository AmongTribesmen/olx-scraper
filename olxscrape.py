from obj.py import *


url_options = ['https://www.olx.com.bh',
'https://www.olx.com.eg',
'https://olx.jo',
'https://olx.com.kw',
'https://www.olx.com.om',
'https://www.olx.com.pk',
'https://olx.qa',
'https://www.olx.sa.com',
'https://www.olx.com.lb']


def pick_url(o):
    global url_options

    try:
            return url_options[o]
    except Exception as ex:
        print(ex)


link_choice = int(input('''

1: https://www.olx.com.bh/
2: https://www.olx.com.eg/
3: https://olx.jo/
4: https://olx.com.kw/
5: https://www.olx.com.om/
6: https://www.olx.com.pk/
7: https://olx.qa/
8: https://www.olx.sa.com/
9: https://www.olx.com.lb/

Enter the number of the website you would like to scrape from:
 ''')) - 1


if link_choice in range(len(url_options)):
    link_choice = pick_url(link_choice)
else:
    print('what you entered is not in the list, terminating.')
    quit()

print(link_choice)
query_choice=input('\nEnter your search query: ').lower()


scraper=Scraper(query_choice,link_choice)

print(scraper.get_links())
print(scraper.parse())
