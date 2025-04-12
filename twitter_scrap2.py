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

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    logging.info("Initializing WebDriver...")
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_twitter_data(search_query, start_date, end_date, num_tweets):
    logging.info(f"Scraping data for: {search_query}, from {start_date} to {end_date}, aiming for {num_tweets} tweets")
    driver = setup_driver()
    url = f"https://x.com/search?q={search_query}%20since%3A{start_date}%20until%3A{end_date}&src=typed_query"
    logging.info(f"Opening URL: {url}")
    driver.get(url)

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(random.uniform(3, 6))  # Initial delay to allow page to load

    tweets_data = []
    tweet_count = 0
    no_new_tweets_counter = 0  # Counter for when no new tweets are found

    while tweet_count < num_tweets:
        logging.info(f"Currently scraped {tweet_count} tweets, scrolling...")
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(random.uniform(2, 5))

        tweets = driver.find_elements(By.CSS_SELECTOR, "article")
        if not tweets:
            logging.warning("No tweets found on this page! Check if the structure has changed.")
            break

        # Keep track of how many tweets were already scraped
        current_scraped_tweets = tweet_count

        for tweet in tweets:
            try:
                tweet_data = {}
                tweet_data['text'] = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']").text
                tweet_data['timestamp'] = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
                tweet_data['username'] = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='User-Name'] span").text

                # Extract the number of retweets from the aria-label
                retweet_button = tweet.find_element(By.CSS_SELECTOR, "button[data-testid='retweet']")
                tweet_data['retweets'] = retweet_button.get_attribute("aria-label").split()[0]  # Extract the number of retweets

                # Extract the number of likes from the aria-label
                like_button = tweet.find_element(By.CSS_SELECTOR, "button[data-testid='like']")
                tweet_data['likes'] = like_button.get_attribute("aria-label").split()[0]  # Extract the number of likes

                # Extract the number of replies from the aria-label
                reply_button = tweet.find_element(By.CSS_SELECTOR, "button[data-testid='reply']")
                tweet_data['replies'] = reply_button.get_attribute("aria-label").split()[0]  # Extract the number of replies

                # Extract the number of views from the analytics link
                #view_analytics_button = tweet.find_element(By.CSS_SELECTOR, "div[data-testid='app-text-transition-container']")
                #tweet_data['views'] = view_analytics_button.text

                tweets_data.append(tweet_data)
                tweet_count += 1
                logging.info(f"Scraped {tweet_count}: {tweet_data}")

                if tweet_count >= num_tweets:
                    break
            except Exception as e:
                logging.error(f"Error processing tweet: {e}")
        
        # Check if no new tweets were added
        if tweet_count == current_scraped_tweets:
            no_new_tweets_counter += 1
            logging.info(f"No new tweets found in this scroll attempt. Count: {no_new_tweets_counter}")
        
        # If no new tweets after 3 attempts, stop the process
        if no_new_tweets_counter >= 3:
            logging.info("No new tweets retrieved after multiple attempts. Stopping the process.")
            break

    driver.quit()
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
    search_term = input("Enter the search term: ")
    start_date_str = input("Enter start date (YYYY-MM-DD): ")
    end_date_str = input("Enter end date (YYYY-MM-DD): ")
    number_of_tweets = int(input("Enter number of tweets to collect: "))

    try:
        datetime.strptime(start_date_str, '%Y-%m-%d')
        datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        logging.error("Invalid date format. Please use YYYY-MM-DD.")
        exit()

    scraped_data = scrape_twitter_data(search_term, start_date_str, end_date_str, number_of_tweets)
    if scraped_data:
        save_to_csv(scraped_data)
    else:
        logging.warning("No tweets were scraped. Possible reasons: No tweets available, page structure changed, or login issues.")
