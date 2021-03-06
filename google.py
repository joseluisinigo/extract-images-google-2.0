from selenium import webdriver
import time, requests
from selenium.webdriver.common.by import By
import csv

def search_google(search_query):
    browser = webdriver.Chrome()
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    images_url = []

    # open browser and begin search
    browser.get(search_url)
    elements = browser.find_elements_by_class_name('rg_i')

    count = 0
    for e in elements:
        # get images source url
        e.click()
        time.sleep(1)
        element = browser.find_elements_by_class_name('v4dQwb')

        # Google image web site logic
        if count == 0:
            big_img = element[0].find_element_by_class_name('n3VNCb')
        else:
           big_img = element[1].find_element_by_class_name('n3VNCb')

        images_url.append(big_img.get_attribute("src"))

        # write image to file
        reponse = requests.get(images_url[count])
        if reponse.status_code == 200:

            with open(f"{search_query}.jpg","wb") as file:
                file.write(reponse.content)

        count += 1

        # Stop get and save after 5
        if count == 1:
            break

    return images_url

file=csv.reader(open('andaluza.csv'), delimiter=',')
f = open('google.csv', 'w')
for line in file:
    items = search_google(line[0])
   
    f.write(line[0]+','+line[1]+','+items[0]+'\n')
f.close()
