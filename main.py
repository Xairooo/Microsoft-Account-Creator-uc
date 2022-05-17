from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, json, string, random

os.system("cls||clear")
print("Microsoft Account Creator - senoe")

# Load config
try:
    with open("config.json") as f:
        config = json.load(f)
    cfg_signup_link = str(config["signup_link"])
    cfg_webdriver = str(config["webdriver"]).lower()
except Exception as e:
    print(f"Failed to load config: {e}")

print("Launching webdriver...")

if "firefox" in cfg_webdriver or "gecko" in cfg_webdriver:
    driver = webdriver.Firefox(executable_path=r"./webdriver/geckodriver", service_log_path=os.devnull)
elif "chrome" in cfg_webdriver:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options, executable_path=r"./webdriver/chromedriver", service_log_path=os.devnull)

wait = WebDriverWait(driver, 30)

def create():
    # Go to signup link
    driver.get(cfg_signup_link)

    # Generate random email/password
    email = f"a{''.join(random.sample(string.ascii_lowercase + string.digits, 10))}@outlook.com"
    password = ''.join(random.sample(string.ascii_letters, 8))
    
    print(f"Account creation started | {email}")

    # Enter email
    wait.until(EC.visibility_of_element_located((By.ID, "MemberName"))).send_keys(email)
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    # Enter password
    wait.until(EC.visibility_of_element_located((By.ID, "PasswordInput"))).send_keys(password)
    # Uncheck promotion checkbox
    wait.until(EC.visibility_of_element_located((By.ID, "iOptinEmail"))).click()
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "BirthDateCountryAccrualInputPane")))
    # Select country
    Select(driver.find_element_by_id("Country")).select_by_value("US")
    # Select birthday month
    Select(driver.find_element_by_id("BirthMonth")).select_by_value("1")
    # Select birthday day
    Select(driver.find_element_by_id("BirthDay")).select_by_value("1")
    # Select birthday year
    driver.find_element_by_id("BirthYear").send_keys("2000")
    # Click Next
    wait.until(EC.visibility_of_element_located((By.ID, "iSignupAction"))).click()

    # Ask the user to manually complete the captcha
    wait.until(EC.visibility_of_element_located((By.ID, "enforcementFrame"))).click()
    print(f"Captcha completion required | {email}")

    WebDriverWait(driver, 20000).until(EC.visibility_of_element_located((By.ID, "microsoft_container")))

    # Save credentials to file
    with open("accounts.txt", "a") as f:
        f.write(f"{email}:{password}\n")
    
    print(f"Account created | {email}")

amount = 1
while True:
    try:
        amount = int(input("How many accounts would you like to create?\n> "))
        if amount > 0: break
        print("Please enter a valid amount.")
    except ValueError:
        print("Please enter a valid amount.")
        pass

for _ in range(amount):
    create()
