import requests
from bs4 import BeautifulSoup

listings = []
counter = 0

def get_listings():
    return listings

def print_listings(listings):
    for item in listings:
        print(item)
        print()


def scrape_kijiji():
    print("Scraping Kijiji...")
    url = 'https://www.kijiji.ca/b-apartments-condos/kingston-on/c37l1700183?sort=dateDesc&radius=12.0&address=Kingston%2C+ON&ll=44.2334401%2C-76.49302949999999'
    # Old link with only 9 listings: "https://www.kijiji.ca/b-real-estate/kingston-on/c34l1700183?address=Kingston%2C%20ON&gpTopAds=y&ll=44.2334401%2C-76.49302949999999&radius=12.0&sort=dateDesc"
    response = requests.get(url)  # Retreive the html content
    soup = BeautifulSoup(response.content, "html.parser")  # Parse the raw data

    items = soup.select(
        'li[data-testid^="listing-card-list-item-"]'
    )  # Retrieve list of listings

    global counter
    for item in items:
        image = item.find('img').get('src')
        title = item.find("h3", attrs={"data-testid": "listing-title"}).text.strip()
        price = item.find("p", attrs={"data-testid": "listing-price"}).text.strip()
        if item.find("li", attrs={"aria-label": "Bedrooms"}) == None:
            beds = "N/A"
        else:
            beds = item.find("li", attrs={"aria-label": "Bedrooms"}).get_text()
        if item.find("li", attrs={"aria-label": "Bathrooms"}) == None:
            baths = "N/A"
        else:
            baths = item.find("li", attrs={"aria-label": "Bathrooms"}).get_text()
        link = (
            "kijiji.ca"
            + item.find("a", attrs={"data-testid": "listing-link"})["href"].strip()
        )
        counter += 1
        listing = {
            "count": counter,
            "image": image,
            "title": title,
            "price": price,
            "beds": beds,
            "baths": baths,
            "link": link,
        }
        listings.append(listing)


def scrape_frontenac():
    print("Scraping Frontenac...")
    url = (
        "https://www.frontenacproperty.com/properties/stud/?sort=availability&order=ASC"
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    items = soup.find_all("div", class_="col-sm-6 col-md-4")

    global counter
    for item in items:
        if item.find("div", class_="text").text.strip() == "RENTED":
            continue
        image = item.find('img').get('src')
        title = item.find("a")["title"].strip()
        price = (
            item.find("span", class_="property-price label label-primary pull-right")
            .find("b")
            .text.strip()
        )
        beds_baths = item.find_all("span", class_="bedrooms")
        
        beds_element = beds_baths[0].find("b")
        if beds_element is not None:
            beds = beds_baths[0].find("b").text.strip()
        else:
            beds = "N/A"
        
        baths = beds_baths[1].find("b").text.strip()
        link = item.find("a")["href"].strip()
        counter += 1
        listing = {
            "count": counter,
            "image": image,
            "title": title,
            "price": price,
            "beds": beds,
            "baths": baths,
            "link": link,
        }
        listings.append(listing)

scrape_kijiji()
scrape_frontenac()