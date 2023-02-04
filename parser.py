import time, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--v=99")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver


result = []
for i in range(0,100+1):
    driver = create_driver()
    url = 'https://music.yandex.ru/genre/музыка%20всех%20жанров/artists' + '?page=' + str(i)
    driver.get(url)
    time.sleep(10)
    try:
        promo = driver.find_element_by_class_name("js-close")
        promo.click()
    except: 
        pass
    time.sleep(2)
    artist__content = driver.find_elements_by_class_name('artist__content')
    
    for artist in artist__content:
        artist_names = artist.find_element_by_class_name('d-artists')
        link_artist = artist_names.find_element_by_class_name('d-link').get_attribute("href")
        id_artist = link_artist.split('/')[-1]
        try:
            artist_genres = artist.find_element_by_class_name('d-genres').text
            try:
                artist_cover = artist.find_element_by_class_name('artist-pics__pic').get_attribute("src")
            except:
                artist_cover = None
        except:
            artist_genres = None
            try:
                artist_cover = artist.find_element_by_class_name('artist-pics__pic').get_attribute("src")
            except:
                artist_cover = None

        #print(id_artist, artist_names.text, artist_genres, artist_cover)
        result.append({'id_artist': int(id_artist), 'artist_name': artist_names.text, 'artist_genre': artist_genres, 'artist_cover': artist_cover})
    time.sleep(2)
    print('quit')
    driver.quit()

with open('result.json', 'w', encoding='utf-8') as fp:
    json.dump(result, fp, sort_keys=True, indent=4, ensure_ascii=False)