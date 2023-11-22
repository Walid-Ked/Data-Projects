import requests
import json
import database

data = []
items = []
connection = database.connect_to_database()
database.create_table(connection)

for i in range(0,2):
    url = f"https://www.accommodationforstudents.com/search?limit=1000&skip={i*1000}&random=false&mode=text&numberOfBedrooms=0&occupancy=min&countryCode=gb"
    payload = {}
    headers = {
    'authority': 'www.accommodationforstudents.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'afsExId=f0bc5a5e-e4e2-46dd-bf03-73b62d6474d0',
    'if-none-match': 'W/"48283a-s696yaKc0XxprHwZOFB94l84aQM"',
    'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data.extend(json.loads(response.text)["properties"])
    
    print(f"Scraped {len(data)} items !")

print(f"Inserting data into database ....")

for n,i in enumerate(data):
    try:
        available_rooms =i["occupancy"]["available"]
        total_rooms = i["occupancy"]["total"]
    except:
        available_rooms = None
        total_rooms = None

    available_rooms = available_rooms
    total_rooms = total_rooms
    id =  i["id"]
    type =  i["propertyType"]
    address1 = i["address"]["address1"]
    address2 = i["address"]["address2"]
    city = i["address"]["city"]
    area = i["address"]["area"]
    postcode = i["address"]["postcode"]
    rentPpw = i["terms"]["rentPpw"]["value"]
    deposit = i["terms"]["deposit"]["value"]
    lat = i["coordinates"]["lat"]
    lon = i["coordinates"]["lon"]
    url = i["url"]
    thumb = i["thumbnails"][0]
    special_offer = i["hasSpecialOffers"]

    database.insert_house(connection,id,type,address1,address2,
                          city,area,postcode,rentPpw,deposit,
                          lat,lon,url,thumb,special_offer,
                          available_rooms)
