from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
def crawling_lyrics(audio_names:dict) -> str:
    lyrics_list = []
    for k, v in audio_names.items():
        try:   
            driver = webdriver.Chrome(options=chrome_options)
            # driver = webdriver.Chrome()
            driver.get('https://www.melon.com/index.htm')
            search_sentense = f"{v['artist']},{v['title']}"
            search = driver.find_element(By.XPATH, '//*[@id="top_search"]') 
            search.send_keys('{}\n'.format(search_sentense))             
            driver.find_element(By.XPATH, '//*[@id="divCollection"]/ul/li[6]/a').click()    
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            num = soup.select('#conts > div.section_lyric > div.wrap_serch_title > h3 > strong > em')   
            if int(num[0].getText()) > 0:  
                driver.implicitly_wait(3)
                driver.find_element(By.XPATH, '//*[@id="pageList"]/div/ul/li/dl/dd[1]/a').click()   
                driver.find_element(By.XPATH, '//*[@id="lyricArea"]/button') 
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                lyrics = soup.select('#d_video_summary')
                if lyrics: 
                    lyrics = lyrics[0].getText().replace('\n', '') 
                    lyrics = lyrics.replace('\t', '')              
                    lyrics_list.append(lyrics)
            else:
                pass
        except:
            pass
    return lyrics_list