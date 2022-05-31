from bs4 import BeautifulSoup
import requests
import csv
import time


def get_watch_links_from_page(page_number):
    links = []
    watchesPageURL = "<URL_REMOVED>/watches"
    headers = {
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Accept': '*/*',
    'Origin': '<URL_REMOVED>',
    'X-Requested-With': 'XMLHttpRequest',
    'Request-Id': '|sL5uR.IsBCm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': '<URL_REMOVED>/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,si;q=0.8',
    }
    response = requests.post(watchesPageURL, params=(('orderby', 'BestMatch'), ('pageno', page_number)), headers=headers)
    
    page = BeautifulSoup(response.content, 'html.parser')
    for node in page.find_all("a", {"class": "prods_name redirect"}):
        links.append("<URL_REMOVED>{0}".format(node['href']))
    return links

def get_watch_details(watch_url):
    headers = {
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Accept': '*/*',
    'Origin': '<URL_REMOVED>',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': '<URL_REMOVED>/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,si;q=0.8',
    }
    response = requests.get(watch_url, headers=headers)
    page = BeautifulSoup(response.content, 'html.parser')
    
    details =  {}

    try:
        details ['Brand'] = page.find("span", {"class": "prod_brand ellipsis"}).text
    except:
        pass
    try:
        details ['Series'] = page.find("span", {"class": "prod_series ellipsis"}).text
    except:
        pass
    try:
        details['Model'] = page.find("span", {"class": "prod_model ellipsis"}).text
    except:
        pass
    try:
        details['Price'] = page.find("div", {"class": "prod_price notranslate"}).find("span", {"class":""}).text
    except:
        pass
    try:
        details['Retail Price'] = page.find("div", {"class": "prod_price-info"}).text.split(":")[1].strip()
    except:
        pass

    for node in page.find("table", {"class": "table prod_info-table"}).find_all("tr"):
        try:
            if node['class'][0] == "prod_info-collapse":
                continue
        except KeyError:
            pass
        td = node.find_all("td")
        try:
            if td[0].text == "Location":
                continue
            details[td[0].text.replace("\n","")] = td[1].text.replace("\n", "")
        except IndexError:
            pass
    
    return details

if __name__ == "__main__":
    pageNumber = 1
    fields = []
    watch_data = []
    print("Scraper Started...")
    while True:
        if pageNumber == 11:
            break
        try:
            watch_links = get_watch_links_from_page(pageNumber)
            print("Scraping Page Number - {0}".format(pageNumber))
        except:
            break
        for link in watch_links:
            print(get_watch_details(link))
            watch_data.append(get_watch_details(link))
            fields += list(get_watch_details(link).keys())
            
        time.sleep(5)
        pageNumber +=1


    print("Scraper Finished...")
    print("Adding Data into CSV File...")
    
    fields = list(set(fields))
    
    with open("watch_details.csv", "w", newline='') as csv_file:
        csv_file_writer = csv.DictWriter(csv_file, fieldnames=fields, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_file_writer.writeheader()
        for data in watch_data:
            csv_file_writer.writerow(data)
    print("Added {0} Data into CSV File...".format(len(watch_data)))
    

