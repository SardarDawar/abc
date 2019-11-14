from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options

#options = Options()
#options.add_argument("--headless")
#driver= webdriver.Firefox(options=options)
driver= webdriver.Chrome()

driver.get('https://detail.tmall.com/item.htm?id=595846333546&spm=a220o.1000855.1998099587.3.3bad54fadPsY4l')


time.sleep(5)

images = driver.find_elements_by_id('J_ImgBooth')
for images in images:
    print(images.get_attribute('src'))


title = driver.find_elements_by_tag_name('h1')
print(title[1].text)
     


offer = driver.find_elements_by_class_name('newp')
for offer in offer:
    print(offer.text)

rating = driver.find_elements_by_id('J_StrPriceModBox')
for rating in rating:
    print(rating.text)

    


details = driver.find_elements_by_class_name('attributes')
for details in details:
    print(details.text)

print('RATINGS')

driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]').click()
time.sleep(5)
at=driver.find_elements_by_xpath('//*[@id="J_Reviews"]/div/div[1]')
for at in at:
    print(at.text)











