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
    
    item_id = item_tree.xpath('//td[contains(text(), "Item ID")]/following-sibling::td/text()')[0]
    weight = item_tree.xpath('//td[contains(text(), "Weight")]/following-sibling::td/text()')[0]
    item_type = item_tree.xpath('//td[contains(text(), "Type")]/following-sibling::td/a/span/text()')[0]
    rarity = item_tree.xpath('//td[contains(text(), "Rarity")]/following-sibling::td/a/span/text()')[0]
    horizontal_slots = item_tree.xpath('//td[contains(text(), "Horizontal Slots")]/following-sibling::td/text()')[0]
    vertical_slots = item_tree.xpath('//td[contains(text(), "Vertical Slots")]/following-sibling::td/text()')[0]
    
    try:
        description = item_tree.xpath('//p/text()')[3]
        pass
    except Exception as e:
        description = None
        print(name + "BU EŞYANIN AÇIKLAMA KISMI YÜKLENMEDİ --------------------------------------------") 
    
    try:
        magazine = item_tree.xpath('//td[contains(text(), "Magazine")]/following-sibling::td/a/text()')[0]
        pass
    except Exception as e:
        magazine = None
        pass
    
    data.setdefault('item',[]).append({
        "name": name,
        "item_id": item_id,
        "weight": weight,
        "item_type": item_type,
        "rarity": rarity,
        "horizontal_slots": horizontal_slots,
        "vertical_slots": vertical_slots,
        "description": description,
        "magazine": magazine,
        "image_url": f"https://unturnedhub.com/img/item/200/{name}.png"})
    
    with open("items.json", "w") as f: # YOU CAN CHANGE LOCATION
        json.dump(data, f)
    print(name +" ataması yapıldı")





