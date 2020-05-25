import requests
import re
import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def get_searchpage(keyword):
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    url0 = 'https://v.qq.com/x/search/?q='
    url1 = '&stag=3&cur='
    pattern=re.compile('<h2 class="result_title"><a href="(.*?)"') 
    items = []
    for i in range(1,22):
        url = url0+keyword+url1+str(i) #get search pages' urls
        response = requests.get(url,headers=headers)
        html = response.text 
        found_items = re.findall(pattern,html) #get all urls of video pages
        items += found_items
    return items


def get_element(video_pages):
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path='/Users/linyutian/Desktop/chromedriver', options=options) #initialize browser
    for video_page in video_pages:
        start = time.time()
        browser.set_page_load_timeout(10)
        try:
            browser.get(video_page)
        except TimeoutException:
            pass
        video_class = browser.find_element_by_tag_name('video')
        video_src = video_class.get_attribute('src') #get videos' srcs
        if (video_src[0:4] == "blob"):
            print('Video_src is locked') #judging blob
            continue
        elif (video_src == []):
            print('Cannot get the video_src')
            continue #judging failed getting
        else:
            try:
                response = requests.get(video_src)
            except Exception:
                print("Download failed")
                continue #reduce the influence of some small errors
            content = response.content
            filename = video_page[-15:-5]
            # prevent the repeated video
            if (filename + '.mp4' in os.listdir()):
                continue
            else: 
                # Download videos
                with open(filename + '.mp4', 'wb') as f:
                    f.write (content)
                end =time.time()
                lasting_time = end-start
                print("Download successfully." + "Running time:"+ str(lasting_time))
    browser.close()
    
        
def main():
    keywords = input("Please input what you want: ").split(' ')  #Users put in keyword
    for keyword in keywords:
        video_pages = get_searchpage(keyword) #get video page
        get_element(video_pages) #download videos
    
main()
    
