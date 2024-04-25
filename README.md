# Reddit Spider
Reddit Spider is a web scraping tool built with Scrapy framework that crawls various subreddits on old.reddit.com and extracts information from forum threads based on start and end date. The spider visits multiple subreddits related to education, careers, and professions, and retrieves relevant data for further analysis.

# Features:
- Scrapes multiple subreddits on old.reddit.com to gather information from forum threads.
- Extracts data such as post titles, comments, and user details based on given dates.
- Handles pagination to crawl through multiple pages of threads within each subreddit.
- Uses cookies and headers for authentication and session management.

# Prerequisites:
Before running the Reddit Spider, ensure that the following dependencies are installed:

- Python 3.x
- Scrapy
- Pandas
- To install Scrapy, you can use pip:
```bash
pip install scrapy
```

# Usage:
- Clone the repository or download the source code.
- Open a terminal or command prompt and navigate to the project directory.
- Modify the subreddits list in the reddit.py file to include the desired subreddits you want to scrape.
- Optionally, update the allowed_domains and baseurl variables if you want to scrape a different version of Reddit or specific domains.
- Add STARTDATE and ENDDATE to extract data in the spider. Example:
```bash
STARTDATE = "25/06/2023"
ENDDATE = "26/06/2023"
```
Run the spider using the following command:
```bash
scrapy crawl reddit -o ./datafolder/data.csv
```
The spider will start crawling the subreddits and extract the desired information from the forum threads.
The extracted data will be stored in the data.csv in datafolder directory

# Customization:
You can customize the behavior of the Reddit Spider by modifying the spider's attributes and settings. Here are some possible customizations:

Adjust the allowed_domains attribute to restrict crawling to specific domains.
Modify the cookies and headers attributes to handle authentication and session management.
Change the output format or file name by modifying the Scrapy settings.
