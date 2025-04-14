import time
import random
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init()

# Display welcome screen
def welcome_screen():
    print(Fore.YELLOW + Style.BRIGHT + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + "     WELCOME TO TWITTER SCRAPING TOOL!")
    print(Fore.MAGENTA + Style.BRIGHT + "  Created by Mahmoud Ghazayel - @ghazayel")
    print(Fore.YELLOW + Style.BRIGHT + "=" * 50 + Style.RESET_ALL)
    print("\n")
    print(Fore.GREEN + Style.BRIGHT + "Initializing..." + Style.RESET_ALL)
    time.sleep(2)
    print(Fore.BLUE + Style.BRIGHT + "Ready to go!\n" + Style.RESET_ALL)

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    logging.info("Initializing WebDriver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def safe_get_count(tweet, selector):
    try:
        element = tweet.find_element(By.CSS_SELECTOR, selector)
        aria_label = element.get_attribute("aria-label")
        count = aria_label.split()[0]
        return count if count.isdigit() else "0"
    except:
        return "0"

def scrape_twitter_data(search_query, start_date, end_date, num_tweets):
    logging.info(f"Scraping data for: {search_query}, from {start_date} to {end_date}, aiming for {num_tweets} tweets")
    driver = setup_driver()
    url = f"https://x.com/search?q={search_query}%20since%3A{start_date}%20until%3A{end_date}&src=typed_query&f=live"
    logging.info(f"Opening URL: {url}")
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(random.uniform(4, 7))

    tweets_data = []
    tweet_ids = set()
    tweet_count = 0
    no_new_tweets_counter = 0

    while tweet_count < num_tweets:
        logging.info(f"Currently scraped {tweet_count} tweets. Scrolling...")

        # Scroll up a bit and then scroll down
        half_height = driver.execute_script("return document.body.scrollHeight / 2")
        driver.execute_script(f"window.scrollTo(0, {half_height});")
        time.sleep(random.uniform(2, 4))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(4, 7))

        tweets = driver.find_elements(By.CSS_SELECTOR, "article")
        current_scraped_tweets = tweet_count

        for tweet in tweets:
            try:
                tweet_id = tweet.get_attribute("data-testid") + tweet.text[:30]
                if tweet_id in tweet_ids:
                    continue
                tweet_ids.add(tweet_id)

                tweet_data = {}
                tweet_data['text'] = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
                tweet_data['timestamp'] = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                tweet_data['username'] = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='User-Name'] span").text

                tweet_data['retweets'] = safe_get_count(tweet, "button[data-testid='retweet']")
                tweet_data['likes'] = safe_get_count(tweet, "button[data-testid='like']")
                tweet_data['replies'] = safe_get_count(tweet, "button[data-testid='reply']")

                tweets_data.append(tweet_data)
                tweet_count += 1
                logging.info(f"Scraped {tweet_count}: {tweet_data['text'][:60]}...")

                if tweet_count >= num_tweets:
                    break
            except Exception as e:
                logging.warning(f"Skipped a tweet due to error: {e}")

        if tweet_count == current_scraped_tweets:
            no_new_tweets_counter += 1
            logging.info(f"No new tweets found. Retry attempt: {no_new_tweets_counter}")

        if no_new_tweets_counter >= 3:
            logging.info("No new tweets loaded after multiple attempts. Finishing scraping...")
            break

    driver.quit()
    print(Fore.CYAN + Style.BRIGHT + f"\nScraping complete. Total tweets collected: {tweet_count}" + Style.RESET_ALL)
    return tweets_data

def save_to_csv(tweets_data, filename="twitter_data.csv"):
    if not tweets_data:
        logging.warning("No data to save!")
        return

    keys = tweets_data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(tweets_data)
    logging.info(f"Data saved to {filename}")

if __name__ == "__main__":
    welcome_screen()

    search_term = input("Enter the search term: ")
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    number_of_tweets = int(input("Enter number of tweets to collect: "))

    try:
        datetime.strptime(start_date_str, '%Y-%m-%d')
        datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
        input("Press Enter to exit.")
        exit()

    scraped_data = scrape_twitter_data(search_term, start_date_str, end_date_str, number_of_tweets)
    if scraped_data:
        save_to_csv(scraped_data)
        input(Fore.GREEN + "\n✅ Scraping done successfully! Press Enter to exit." + Style.RESET_ALL)
    else:
        input(Fore.RED + "\n⚠️ No tweets were scraped. Check your input or connection. Press Enter to exit." + Style.RESET_ALL)
