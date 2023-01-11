from bs4 import BeautifulSoup
import requests
import pynput
import mouse
import english_words
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import io
import os
from PIL import Image
import time
import configparser

def webscraper():
# Zieht einzelne Daten aus der Webseite und zeigt diese an

    city_1 = 'Tokyo'
    city_2 = 'Ingolstadt'

    # f kennzeichnet formatierten string, nachträgliche Änderungen möglich
    url = f'https://www.numbeo.com/cost-of-living/compare_cities.jsp?country1=Japan&city1={city_1}&country2=Germany&city2={city_2}&displayCurrency=EUR'
    page= requests.get(url) #automatisch auf url zugreifen
    soup = BeautifulSoup(page.content, 'html.parser') # Zugriff auf Seite durch BeautifulSoup, Aufteilung in kleine html Teile
    table = soup.find('table', attrs={'class':'data_wide_table new_bar_table cost_comparison_table'}) # Suche in soup
    rows= table.find_all('tr') #

    cola_data = rows[7].text.split() # In rows Liste 7.Element aufrufen, nur Text herausgeben, als Liste herausgeben

    price_1 = cola_data[4] # 1.Preis an 4.Stelle
    price_2 = cola_data[7] # 2. Preis an '6. Stelle

    
    # data_wide_table new_bar_table cost_comparison_table

def downloadMultipleImg():
    # Downloadet mehrere Bilder einer Google Suche, werden danach wieder gelöscht
    
    PATH = "C:\\Users\\"+config['PATH']['User'] +"\\PycharmProjects\\DownloadImg\\chromedriver.exe"  # Path of webdriver

    wd = webdriver.Chrome(PATH)

    #image_url = "https://wallpaperaccess.com/full/7078582.jpg"  # URL of selected picture


    def get_images_from_google(wd, delay, max_images):
        def scroll_down(wd):
            wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')  # scrolls down in google search bar
            time.sleep(delay)

            # url of your google search
        url_pic = "https://www.google.com/search?q=python+animal+wallpaper&tbm=isch&ved=2ahUKEwi_o8XrtcP3AhUXkaQKHTZCBbcQ2-cCegQIABAA&oq=python+animal+wallpaper&gs_lcp=CgNpbWcQAzIECAAQEzoECAAQQzoFCAAQgAQ6BggAEAcQHjoICAAQCBAHEB46BggAEAgQHlCCBljdJ2CnK2gAcAB4AIABRogB8gOSAQE4mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=_CtxYr-1LZeikgW2hJW4Cw&bih=927&biw=929&rlz=1C1AVFC_enDE903DE907"
        wd.get(url_pic)  # load url

        image_urls = set()
        skips = 0

        while len(image_urls) + skips < max_images:  # downloads images as long amount is less than max_images
            scroll_down(wd)

            thumbnails = wd.find_elements(By.CLASS_NAME, "islir")  # every image from google searcgh has same class name -> finds all elemnts with this class name

            for img in thumbnails[len(image_urls) + skips:max_images]:  # additional img thumbnails after max_images added to image_urls (does not add same thumbnails multiple times)
                try:
                    img.click()
                    time.sleep(delay)
                except:
                    continue  # if click fails, go to next item in for loop

                images = wd.find_elements(By.CLASS_NAME, "Q4LuWd")  # returns image #rg_i
                for image in images:
                    if image.get_attribute("src") in image_urls:  # hinders clicking same image multiple times
                        max_images += 1
                        skips += 1
                        break

                    if image.get_attribute("src") and "http" in image.get_attribute("src"):  # if image has same class name, then check if it has a source, if yes -> Image_urls
                        image_urls.add(image.get_attribute("src"))
                       

        return image_urls


    def download_image(download_path, url2, file_name):  # path the image is downloaded to, url of image, file name of downloades image
        try:
            image_content = requests.get(url2).content
            image_file = io.BytesIO(image_content)  # store this as a binary data type in computer's memory
            image = Image.open(image_file)  # load image_file as an actual image
            file_path = download_path + file_name  # img stored in download path

            with open(file_path, "wb") as f:  # wb means writing an image
                image.save(f, "JPEG")  # img saved in a JPEG form

           
        except:
            pass

    #download_image("", image_url, "test.jpg")  # download_path blank means img stored, where py file located


    urls = get_images_from_google(wd, 1, 2)
    for i, url in enumerate(urls):
        download_image("", url, str(i) + ".jpg")  # loop through all urls, downloaded in folder where py file is, unique name for all images
    wd.quit()  # closes webdriver
    
    time.sleep(4)
 
    # Does the file exist? If it exists it gets removed
    for i in range(0, 100):
        if os.path.exists(str(i) + '.jpg'):
            os.remove(str(i) + '.jpg')
    # If file does not exist
        else:
            print("%s.jpg doesn't exist!" % str(i))
    

def clickButtons()  
# Sucht einen Begriff in der Suchleiste und klickt auf Links

    config = configparser.ConfigParser()
    config.read('ConfigPathDriver.txt')

    PATH = 'C:\\Users\\'+config['PATH']['User']+'\\chromedriver.exe'
    driver = webdriver.Chrome(PATH)

    driver.get("https://de.wikipedia.org/wiki/Wikipedia:Hauptseite")
    

    search = driver.find_element_by_id('searchInput')  # Name des Buttons in der Webseite
    search.send_keys("Python")  # Eingabe in Suchleiste
    search.send_keys(Keys.RETURN)  # Return Taste drücken um Suche zu starten
    time.sleep(1)
    click = driver.find_element_by_class_name('searchmatch')
    click.click()
    time.sleep(1)
    click2 = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/ul[1]/li[3]/a')
    click2.click()
    time.sleep(5)  # Delay, damit Browser nicht sofort schließt

    driver.quit()  # schließt browser
    
    time.sleep(5)
    
    # Does the file exist? If it exists it gets removed
    for i in range(0, 100):
        if os.path.exists(str(i) + '.jpg'):
            os.remove(str(i) + '.jpg')
    # If file does not exist
        else:
            pass
    # Downloaded images are deleted 
    
def googleSearch():
    # Zufällig ausgewählte englische Wörter werden über Bing gesucht
    
    PATH = 'C:\\Users\\' + config['PATH']['User'] + '\\chromedriver.exe'
    driver = webdriver.Chrome(PATH)
    
    driver.get("https://www.bing.com/?cc=de")
    driver.maximize_window()
    
    search = english_words.english_words_set.pop()
    bar = driver.find_element_by_class_name('sb_form_q')
    bar.send_keys(search + Keys.ENTER)
    sleep(2)
    driver.find_element_by_xpath('//button[normalize-space()="Akzeptieren"]').click()
    sleep(2)
    
    driver.quit()
    
def randomizer_Web():
    a = randint(1,3)
    if a == 1:
        webscraper()
        
    if a == 2:
        downloadMultipleImg()
        
    if a == 3:
        clickButtons()
          
    if a == 4:
        googleSearch()
        
