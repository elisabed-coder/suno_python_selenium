import random
import time
import sqlite3
import pyperclip
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# from hcaptcha_solver import hcaptcha_solver
import undetected_chromedriver as uc
from seleniumbase import SB, Driver

def setup_driver():
    driver = Driver(uc=True, undetected=True)
    # options.add_argument(r"--user-data-dir=C:\Users\barat\AppData\Local\Google\Chrome for Testing\User Data")
    # options.add_argument("--profile-directory=Eli")
    driver.maximize_window()
    driver.get("https://suno.com")

    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("useAutomationExtension", False)

    driver.uc_open_with_reconnect("https://suno.com", reconnect_time=6)

    return driver

def wait_for_clickable(driver, xpath, timeout=15):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

def wait_for_presence(driver, xpath, timeout=30):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

def login_to_account(driver):
    driver.get("https://suno.com")
    sign_in_button = wait_for_clickable(driver, '/html/body/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div[2]/button[1]')
    time.sleep(random.uniform(2, 4))
    sign_in_button.click()

    # Wait for and click "Continue with Google" button
    google_button = wait_for_clickable(driver, '/html/body/div[6]/div[1]/div/div/div/div[1]/div[2]/div[1]/div/button[3]')
    time.sleep(random.uniform(2, 4))
    google_button.click()
    email_input = wait_for_presence(driver, '//*[@id="identifierId"]')
    time.sleep(random.uniform(2, 4))
    email_input.send_keys('elitesting001@gmail.com')


    # Click "Next" button
    next_button = wait_for_clickable(
        driver, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button')
    time.sleep(random.uniform(2, 4))
    next_button.click()

    password_input = wait_for_presence(driver, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
    time.sleep(random.uniform(2, 4))
    password_input.send_keys('EliTesting01!')
    login_button = wait_for_clickable(driver, '//*[@id="passwordNext"]/div/button')
    time.sleep(random.uniform(2, 4))
    login_button.click()

def click_create_song(driver):
    create_button = wait_for_clickable(driver, '/html/body/div[1]/div[1]/div[1]/div[3]/a[2]')
    time.sleep(random.uniform(2, 5))
    create_button.click()

def select_auto_or_custom_button(driver):
    auto_button_xpath = '//*[@id="main-container"]/div[1]/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div/button[1]'
    custom_button_xpath = '//*[@id="main-container"]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div/div[1]/button[2]'

    try:
        # Try auto_button first
        auto_button = wait_for_clickable(driver, auto_button_xpath)
        time.sleep(random.uniform(1, 3))
        auto_button.click()
    except TimeoutException:
        print("Auto button not found, clicking custom button first...")

        # Click custom_button
        custom_button = wait_for_clickable(driver, custom_button_xpath)
        time.sleep(random.uniform(2, 4))
        custom_button.click()

        # Try auto_button again
        auto_button = wait_for_clickable(driver, auto_button_xpath)
        time.sleep(random.uniform(1, 2))
        auto_button.click()


def handle_cloudflare_turnstile(driver, max_wait=90):
    try:
        # Step 1: Wait for iframe (if captcha appears)
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@title, 'captcha')]"))
        )
        print("🛡 hCaptcha iframe found. Waiting for solve...")

        # Step 2: Wait inside iframe until captcha is solved
        WebDriverWait(driver, max_wait).until_not(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'prompt-text')]"))
        )
        print("✅ Captcha solved!")

        # Step 3: Switch back to main content
        driver.switch_to.default_content()

    except TimeoutException:
        print("✅ No captcha detected or solved already. Continuing...")



def enter_prompt_and_create(driver, prompt_text):
    textarea_xpath = '//*[@id="main-container"]/div[1]/div/div[1]/div/div[3]/div/div/div/div/div[3]/div/div[2]/div[1]/div[2]/div/textarea'
    button_xpath = '//*[@id="main-container"]/div[1]/div/div[1]/div/div[4]/div[2]/button'
    textarea = wait_for_clickable(driver, textarea_xpath)
    time.sleep(random.uniform(2, 5))
    textarea.send_keys(prompt_text)

    button = wait_for_clickable(driver, button_xpath)
    time.sleep(random.uniform(2, 5))
    button.click()
    handle_cloudflare_turnstile(driver)


def go_to_library_and_open_song(driver):
    library_xpath = '/html/body/div[1]/div[1]/div[1]/div[3]/a[3]'
    songs_container_xpath = '//div[contains(@id, "tabpanel-songs")]'
    target_a_xpath = songs_container_xpath + '//a'

    # Step 1: Click Library button
    library_button = wait_for_clickable(driver, library_xpath)
    time.sleep(random.uniform(45, 75))
    library_button.click()

    time.sleep(random.uniform(2, 5))  # wait for page update

    # Step 2: Wait for container to be present
    wait_for_presence(driver, songs_container_xpath, timeout=30)

    # Step 3: Find all <a> tags deeply inside container
    all_links = driver.find_elements(By.XPATH, target_a_xpath)

    if all_links:
        first_a = all_links[0]

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", first_a)
        time.sleep(random.uniform(1, 2))

        # Try to click safely
        try:
            first_a.click()
        except Exception:
            driver.execute_script("arguments[0].click();", first_a)
    else:
        print("No <a> tags found inside container!")




def get_song_info(driver):
    title_xpath = '//*[@id="main-container"]/div[1]/div[1]/div[2]/div[1]/input'
    prompt_xpath = '//*[@id="main-container"]/div[1]/div[2]/div[1]/div[1]/section/div[1]/p'
    share_button_xpath = '//*[@id="main-container"]/div[1]/div[1]/div[2]/div[5]/div[2]/button[2]'

    title_input = wait_for_presence(driver, title_xpath, timeout=30)
    time.sleep(random.uniform(4, 8))
    title = title_input.get_attribute("value")

    share_button = wait_for_clickable(driver, share_button_xpath)
    share_button.click()
    time.sleep(random.uniform(2, 4))
    url = pyperclip.paste()

    prompt_element = wait_for_presence(driver, prompt_xpath)
    prompt = prompt_element.text

    return title, prompt, url

def save_to_db(title, prompt, url):
    conn = sqlite3.connect('suno_db.db')
    c = conn.cursor()
    c.execute("INSERT INTO songs (title, prompt, url) VALUES (?, ?, ?)", (title, prompt, url))
    conn.commit()
    conn.close()
    print(f"Saved to DB: {title}, {url}, {prompt}")



# MAIN RUN
try:
    driver = setup_driver()
    login_to_account(driver)
    click_create_song(driver)
    select_auto_or_custom_button(driver)
    enter_prompt_and_create(driver, "I was sitting in the room alone, it was dark, suddenly I see leaning on the stick mother coming through the wall.")
    go_to_library_and_open_song(driver)
    title, prompt, url = get_song_info(driver)
    print("Title:", title)
    print("URL:", url)
    print("Prompt:", prompt)
    save_to_db(title, prompt, url)
finally:
	driver.quit()

