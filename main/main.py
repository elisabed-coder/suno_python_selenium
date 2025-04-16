import time
import sqlite3
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


options = webdriver.ChromeOptions()

# Use your actual profile path
options.add_argument("user-data-dir=C:\\Users\\barat\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("profile-directory=Profile 1")

# Add anti-detection flags BEFORE launching driver
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Optional: Make it a little more stealthy
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://suno.com")
create_button = WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[3]/a[2]/span')))
create_button.click()
custom_button = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located(
        (By.XPATH, '//*[@id="main-container"]/div[1]/div/div[1]/div/div[2]/div/div[1]/div/div/div[1]/button[2]')))
if "bg-white" not in custom_button.get_attribute("class"):
    custom_button.click()
    print("Clicked on the custom button (was not selected).")
else:
    print("Custom button is already selected.")
auto_button = WebDriverWait(driver, 40).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="main-container"]/div[1]/div/div[1]/div/div[2]/div/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/button[1]')))
auto_button.click()
lyrics_input = WebDriverWait(driver, 10).until(
    ec.presence_of_element_located((
        By.XPATH,'//*[@id="main-container"]/div[1]/div/div[1]/div/div[2]/div/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div/textarea'))
)
lyrics_input.send_keys("lets generate new ai song")
create_song_button = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="main-container"]/div[1]/div/div[1]/div/div[3]/div[2]/button')))
create_song_button.click()
time.sleep(10)
song_links = WebDriverWait(driver, 60).until(
    ec.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/song/")]'))
)

WebDriverWait(driver, 20).until(
    ec.invisibility_of_element_located((By.XPATH, '//div[@style and contains(@style, "opacity: 0.05")]'))
)

# Now safely click the last link
song_links[-1].click()
get_title = WebDriverWait(driver, 50).until(ec.presence_of_element_located((By.XPATH, '//*[@id="main-container"]/div[1]/div[1]/div[2]/div[1]/input')))


share_link = WebDriverWait(driver, 20).until(
    ec.presence_of_element_located((By.CSS_SELECTOR, '#main-container > div.bg-background-primary.w-full.h-full.flex.flex-col.items-stretch.overflow-y-scroll.md\:px-4 > div.\@container.flex.flex-row.items-start.justify-stretch.gap-4.md\:pt-8.pb-8.max-md\:flex-col > div.relative.flex-1.flex.flex-col.gap-2.self-stretch.max-md\:px-4 > div.focus-within\:\[\&\>input\]\:border-primary.w-full.font-serif.font-light.text-foreground-primary.text-\[40px\]\/\[56px\] > input'))
)
prompt_text = WebDriverWait(driver, 20).until(ec.presence_of_element_located((By.CSS_SELECTOR,'#main-container > div.bg-background-primary.w-full.h-full.flex.flex-col.items-stretch.overflow-y-scroll.md\:px-4 > div.px-6.md\:px-0.w-full.flex-1.pb-48.flex.flex-col > div:nth-child(2) > div:nth-child(1) > section > div.font-sans.text-primary > p')))

title = get_title.text
prompt = prompt_text.text
url = ''
print(title, url, prompt)

# Insert into SQLite
# conn = sqlite3.connect('suno_db.db')
# c = conn.cursor()
# c.execute("INSERT INTO songs (title, prompt, url) VALUES (?, ?, ?)", (title, prompt, url))
# conn.commit()
# conn.close()
# print(f"Logged to database: {title}, {url}")



time.sleep(50)