import requests
from lxml import html
import json

url = "https://unturnedhub.com/items"
response = requests.get(url)
tree = html.fromstring(response.text)
rows = tree.xpath('//tbody/tr')


item_names = []
for row in rows:
    name = row.xpath('.//td[@class="ts"]/a/text()')[0]
    item_names.append(name)

fixed_item_names = [name.lower().replace(" ", "-") for name in item_names]
items_dict = {}

with open("D:\jsonfile\items.json", "r") as f:
    data = json.load(f)

for name in fixed_item_names:
    item_url = f"https://unturnedhub.com/item/{name}"
    item_response = requests.get(item_url)
    item_tree = html.fromstring(item_response.text)

    try:
        item_id = item_tree.xpath('//td[contains(text(), "Item ID")]/following-sibling::td/text()')[0]
        pass
    except Exception as e:
        item_id = None
        print(e) 
        pass
    try:
        rarity = item_tree.xpath('//td[contains(text(), "Rarity")]/following-sibling::td/a/span/text()')[0]
        pass
    except Exception as e:
        rarity = None
        print(e)
        pass
    

    

    IDrarity = 0    
    match rarity:
        case "Common":
            IDrarity = 1
        case "Uncommon":
            IDrarity = 2
        case "Rare":
            IDrarity = 3
        case "Epic":
            IDrarity = 4
        case "Legendary":
            IDrarity = 5
        case "Mythical":
            IDrarity = 6
            

    data[item_id] = []
    data[item_id].append({
        "name": name,
        "photo": f"https://unturnedhub.com/img/item/500/{name}.png",
        "chance": IDrarity,
        "rarity": IDrarity})
    
    with open("D:\jsonfile\items.json", "w") as f: # YOU CAN CHANG LOCATION
        json.dump(dict(data), f)
    print(name +" ataması yapıldı")





