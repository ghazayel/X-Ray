
# 🐦 X-Ray: Data Extraction Tool  
### Built by [@ghazayel](https://x.com/ghazayel) | Powered by Selenium

---

### ✨ Overview

Welcome to the **X-Ray Scraping Tool** — your trusty sidekick for journalistic investigations, data analysis, or tracking public conversations across **X (formerly Twitter)**. This tool automates the scraping of live tweets within a custom date range, capturing tweet content, timestamps, usernames, retweets, likes, and replies — and outputs everything into a clean `.csv` file 📊.

> 📰 Whether you're chasing a breaking story or analyzing social sentiment, this script does the heavy lifting for you.

---

### 🚀 Features

- 🔍 **Search by keyword/hashtag**
- 🗓️ **Custom date ranges**
- 📄 **Auto-export to CSV**
- 🤖 **Uses real browser session (Chrome) for better authenticity**
- 🔐 **Preserves login/session with your own Chrome profile**
- 📈 **Retweet, like, and reply counts included**
- 🎨 **Beautiful colored CLI interface**
- 🧠 **Smart scroll & duplicate handling**

---

### 📸 Preview

```
WELCOME TO TWITTER SCRAPING TOOL!
Created by Mahmoud Ghazayel - @ghazayel

Initializing...
Ready to go!

Enter the search term: gaza
Enter start date (YYYY-MM-DD): 2025-01-01
Enter end date (YYYY-MM-DD): 2025-01-05
Enter number of tweets to collect: 100

Scraping complete. Total tweets collected: 100
✅ Scraping done successfully! Press Enter to exit.
```

---

### 🛠️ Requirements

Ensure the following Python packages are installed:

```bash
pip install selenium webdriver-manager colorama
```

And of course, have **Google Chrome** installed. The script uses your own Chrome user session for authentication.

---

### ⚙️ Setup & Usage

1. **Clone the repository:**

```bash
git clone https://github.com/ghazayel/X-Ray-scraper.git
cd X-Ray-scraper
```

2. **Customize your Chrome path:**

Make sure this line reflects your system profile path:
```python
options.add_argument("--user-data-dir=C:\Users\User\AppData\Local\Google\Chrome\User Data")
```

3. **Run the script:**

```bash
python X-Ray_scraper.py
```

4. **Input your query:**

You'll be prompted to enter:
- A keyword or hashtag (no `#` needed)
- Start date (`YYYY-MM-DD`)
- End date (`YYYY-MM-DD`)
- Number of tweets to collect

5. **Output:**

Your tweets will be saved in a file like `twitter_data.csv`.

---

### 🧠 How It Works

This scraper mimics human browsing:
- Opens a browser window with your Chrome session
- Navigates to X (Twitter) search
- Scrolls dynamically to load tweets
- Extracts data using Selenium
- Handles duplicates & errors gracefully
- Outputs a well-structured CSV

---

### 📌 Notes

- This tool **does not use Twitter/X API**, which makes it ideal for scraping without needing developer credentials.
- This tool might **NOT** work correctly if the Elon Musk decided to change the UI of X or how the LazyLoading works on the site.
- Always respect the [terms of service](https://x.com/en/tos) of any platform you interact with.
- Ideal for **journalists, researchers, analysts**, and OSINT professionals.

---

### 📁 Output Sample (CSV)

| text | timestamp | username | retweets | likes | replies |
|------|-----------|----------|----------|-------|---------|
| Breaking: UN warns of... | 2025-01-01T12:00:00Z | @UN_News | 145 | 500 | 30 |

---

### 🙋‍♂️ Author

**Mahmoud Ghazayel**  
📸 Journalist & OSINT Specialist  
📍 [@ghazayel](https://x.com/ghazayel)  
📜 [ghazayel.com](https://ghazayel.com)  
📬 Feel free to open an issue or suggest improvements!

---

### 🧪 Final Word

If this project helped your reporting or research, give it a ⭐ on GitHub.  
It keeps this tool alive, accurate, and evolving.

```
🕵️ Stay curious. Stay informed. Stay independent.
```
