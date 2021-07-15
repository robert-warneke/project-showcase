# This program parses data from an XML file containing
# data about plants. The data for each plant is displayed.
# After the data for each plant has been displayed, the
# program also displays the number of plants and their
# average price.
#
# References:
#   https://en.wikiversity.org/wiki/Python_Programming/Internet_Data


import urllib.request
import xml.etree.ElementTree
import sys


def general_error(text):
    print("Error reading file. " + text)
    exit()


def url_check(url):
    if url != "https://www.w3schools.com/xml/plant_catalog.xml":
        text = "Incorrect URL."
        general_error(text)


def read_file(url):
    try:
        page = urllib.request.urlopen(url).read()
        page = page.decode("UTF-8")
    except Exception as exception:
        print(str(exception) + " reading " + url)
        exit(1)

    root = xml.etree.ElementTree.fromstring(page)
    tree = xml.etree.ElementTree.ElementTree(root)

    for element in tree.iter():
        if element.text == '':
            text = "Missing text."
            general_error(text)

    return tree


def count_items(tree):
    item_count = 0
    for element in tree.iter():
        if element.tag == "PLANT":
            item_count += 1

    return item_count


def get_plants(item_count, tree):
    common = []
    botanical = []
    zone = []
    light = []
    price = []
    availability = []
    plants = []
    plant_arrays = [common, botanical, zone, light, price, availability]
    plant_tags = ["COMMON", "BOTANICAL", "ZONE",
                  "LIGHT", "PRICE", "AVAILABILITY"]

    for element in tree.iter():
        for i in range(len(plant_tags)):
            if element.tag == plant_tags[i]:
                plant_arrays[i].append(element.text)

    for m in range(len(plant_tags)):
        if len(plant_arrays[m]) != item_count:
            text = "Missing Data."
            general_error(text)

    for j in range(item_count):
        plant = common[j] + ' (' + botanical[j] + ') - ' + zone[j] + ' - '\
                + light[j] + ' - ' + price[j]

        plants.append(plant)

    return plants


def get_average_price(tree, item_count):
    price = 0
    for element in tree.iter():
        if element.tag == "PRICE":
            item_price = element.text.replace('$', '')
            if item_price.isalpha() is True:
                text = "Invalid Data."
                general_error(text)

            item_price = float(item_price)
            price += item_price

    average_price = price / item_count
    average_price = f"${average_price:.2f} average price"

    return average_price


def plants_out(plants):
    for k in range(len(plants)):
        print(plants[k])


def count_avrg_out(item_count, average_price):
    count_avrg = str(item_count) + " items - " + average_price
    print(count_avrg)


def main():
    url = "https://www.w3schools.com/xml/plant_catalog.xml"
    url_check(url)
    tree = read_file(url)

    # Use the following for testing
    # plant = tree.getroot().find("PLANT")
    # plant.remove(plant.find("LIGHT"))
    # plant.find("PRICE").text = "x"

    item_count = count_items(tree)

    plants = get_plants(item_count, tree)
    average_price = get_average_price(tree, item_count)

    plants_out(plants)
    count_avrg_out(item_count, average_price)


main()
