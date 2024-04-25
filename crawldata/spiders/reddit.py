from urllib.parse import urljoin
from crawldata.items import CrawldataItem
import scrapy
import sys
import pandas as pd
from datetime import datetime

class RedditSpider(scrapy.Spider):
    name = "reddit"
    STARTDATE = "25/06/2023"  # Enter Start Date of Date Range in dd/mm/yyyy format
    ENDDATE = "26/06/2023"    # Enter End date Date of Date Range in dd/mm/yyyy format the entered dates will also be included

    allowed_domains = ["old.reddit.com"]
    # add subreddit names in the list to scrape more subreddit
    subreddits = [
        "businessschool",
        "ApplyingToCollege",
        "School",
        "HighSchool",
        "college",
        "careerguidance",
        "findapath",
        "Accounting",
        "consulting",
        "marketing",
        "law",
        "medicine",
        "jobs",
    ]
    baseurl = "https://old.reddit.com/"

    headers = {
        "authority": "old.reddit.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "csrf_token=05d72004a76d2b3b81a6659c8bbaabe8; csv=2; edgebucket=jjEuq1ceoJqq6WHuBn; eu_cookie={%22opted%22:true%2C%22nonessential%22:true}; USER=eyJwcmVmcyI6eyJ0b3BDb250ZW50VGltZXNEaXNtaXNzZWQiOjAsInRvcENvbnRlbnREaXNtaXNzYWxUaW1lIjowLCJzdWJzY3JpcHRpb25zUGlubmVkIjpmYWxzZSwibmlnaHRtb2RlIjp0cnVlLCJjb2xsYXBzZWRUcmF5U2VjdGlvbnMiOnsiZmF2b3JpdGVzIjpmYWxzZSwibXVsdGlzIjpmYWxzZSwibW9kZXJhdGluZyI6ZmFsc2UsInN1YnNjcmlwdGlvbnMiOmZhbHNlLCJwcm9maWxlcyI6ZmFsc2V9LCJnbG9iYWxUaGVtZSI6IlJFRERJVCJ9fQ==; reddit_session=1473378848893%2C2023-06-25T10%3A10%3A33%2C20b8e17f27abe2b938fc4cc4294fedfef5ef46fa; loid=0000000000isuzq3r1.2.1642601720045.Z0FBQUFBQmttQktaeVlJa1BZcDJLMkx4ck9OMHpHQy1yczFWajVpNVo3SVRwWHA2UFZzdHo5VldET1MwU2sxZGZJTmNFVm1nUVZkS045MjJaQ1FiVjJfUEpCYjhCNTJCSTREalZfMjR0Z3hLS1ZTVkRPc1ZfZVNXNmRHN3dYYVA5cEt3S3dYSDM4T1k; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJleUpoYkdjaU9pSlNVekkxTmlJc0ltdHBaQ0k2SWxOSVFUSTFOanB6UzNkc01ubHNWMFZ0TWpWbWNYaHdUVTQwY1dZNE1YRTJPV0ZGZFdGeU1ucExNVWRoVkd4amRXTlpJaXdpZEhsd0lqb2lTbGRVSW4wLmV5SnpkV0lpT2lKMWMyVnlJaXdpWlhod0lqb3hOamczTnpjME1qTTFMakEzTmpBek15d2lhV0YwSWpveE5qZzNOamczT0RNMUxqQTNOakF6TWl3aWFuUnBJam9pWVZaT1JGOWhNRmRrVUZCZmFIbHNXbVZ3YXpoM1lqZDVNa2t3UmpCbklpd2lZMmxrSWpvaU9YUk1iMFl3YzI5d05WSktaMEVpTENKc2FXUWlPaUowTWw5cGMzVjZjVE55TVNJc0ltRnBaQ0k2SW5ReVgybHpkWHB4TTNJeElpd2liR05oSWpveE5qUXlOakF4TnpJd01EUTFMQ0p6WTNBaU9pSmxTbmhyYTJSSFR6bERRVWxvWkMxR1lUVmZaMlkxVlY5dE5ERldUMnRPVjNCUlNITmFUalV0V1hsMVpFcHVkbFpCTFdSVU5HWlJYMWxKTVZWSlRVSkhRa0ZHYVZOMGVXSlJXVUZyYlVSUFdsRm5SRTFPUkhCeWFWTlJVVFJGYkhGTVJ6aEpVVUp0WW10Uk1WcGhUV05oVnpOM1owSkxhV05GTjJWV1NIQmpNbTloVldKcE5UUmtkalp3ZVV4cWVYQlBWV1pzTTA1cWJVeFhlRkE1UkUxaWNUQXljRmRPV2xSdFkxSXhjRmhSVjB4ZmIxcFBPVk16T1hWVmVsOVRZVEJTT0U5TGNYWkhRbTk1VFZrNFgwaGFWMDFhYVVkMlpuaHVjSEl3V2tZd2QzRTNNMHhSVjNCbU5uSkhOemxyVjFRd1JFczBYMUo0ZG5aRVlWUkhXRXBsYlhBM1VsOTBNekZUTFdwQlVHTmZURGxPY1VKSFlYWTNXSEp5ZEZkaWRGOHhVVFZWZW1scVVsZEtlalJPUW5rMVkzWnJaWFozVkdKT1pXeG1ORE5hYTB4TU5GcGpaRTFpWm0xek5rOXVTbmcwZEVOdU9HWlZZa0ZCUkY5Zk1UaFRNa1pGSWl3aWNtTnBaQ0k2SWs5blRUWnFhbUpMZUZkRFYxVnNja0Y0VDJvMmVGSmZaVGx2TWt0dFlYUmtaSEEyZUhGd1VXWjVWRkVpTENKbWJHOGlPako5Lmg1RkRXWUVpaWJmZXFrVFFXalRHVWlUbjJabktuVzF4NEUyTTM5VmMyMXR3U0FOS2xGRlp6RUMzQnZQekhXMTVUb3lfX3pWdHdKXzJkNHFCUnhqaS1hQTMyTE9RMFhiYzktaF8wdTRfeUM5dzhhbDJDLThTeWRIMzFyTklkUHJWSXNGdEkyUWNqNkRFNE03MDRWNUhWZVFnbXBNX0xYcDZwWW5yZjN4bTNHRU4xX3h0TzVZeXRROVRhQWZ3R1oweHp6RjZ2MUYtaVgxbVRadDZ6a0lobVRGVEtWLVNvYlFFN2J4UUp1dFBNM05NTFRiaWJ1RmY5YlEtMEctLWdXQVl1NmdicDJfM1FWVTVKNk1sRTc2c2UyRGN1dThFcmRfVWVOSnVCRGczMWhVZnFVbUpCdEdjdlE1LTZwQV9QRGR0X0pUdEpoNUZPbUJoN2pMLTZoSy1lUSIsImV4cCI6MTY4Nzc3NDExNSwibG9nZ2VkSW4iOnRydWUsInNjb3BlcyI6WyIqIiwiZW1haWwiLCJwaWkiXSwiY2lkIjoiOXRMb0Ywc29wNVJKZ0EifQ.XYhK5vFVLub0gOcKlAu927nIAXDZW3FcNio3LBCnFOk; pc=cv; datadome=3hs-rgeBOKxWeBdU8vyIqbw~KYz~YVliPITDlhQ_-Dro8tImregpNWT2Dl0nWZuHRypHIGh1gfwSGGqTlQjvb1EXyPKJFV2VZaFj9CODtt3fLagvmT~GKAj_3HiDhBum; recent_srs=t5_10ap6m%2Ct5_2qh4a%2Ct5_318ly%2Ct5_2tkw1%2Ct5_2s0lb%2C; burgerheaded_recentclicks2=t3_12smq3l%2Ct3_13v5zc1%2Ct3_1430256%2Ct3_14iev6d%2Ct3_1326wdr; session_tracker=qWzsJrH3pIJOKyOYcT.0.1687697420233.Z0FBQUFBQmttRGdNVTY2S0syYVdKWUFaYjJKc0MtVXVwVncxNThBUjUtcVpNbk1mZXljUkd6REYyNjNwRGdRa0Ixdi1fMU1Pa0I5cVZfMGpmbktfX0V2Rnp3aXNsWHJOS0lKSVJmOFg1TF9MMzBySDZYaUFQdGRVajdhY2VacnJaemdReEQ0U2FHRXU",
        "referer": "https://old.reddit.com/r/businessschool/comments/14iev6d/alternative_lifestyle_anticonsumerism/",
        "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    category_keywords = {
        "Accounting": ["accountant", "accounting"],
        "Finance": ["finance", "analyst", "financing"],
        "Consultant": ["consultant", "management"],
        "Marketing": ["marketing"],
        "Law": ["law", "lawyer"],
        "Medicine": ["medicine", "doctor", "physician"],
    }
    def dateInRange(self,date,format="%d/%m/%Y",isScrapAll = False):
        '''
        A Utility Function To Check If the Article Date is in Required Date Range
        Send isScrapAll True if You want to scrap all articles without date filter
        '''
        startdate = self.STARTDATE
        enddate = self.ENDDATE
        if not isScrapAll:
            datetime_obj = datetime.fromisoformat(date)
            try:
                startdate_obj = datetime.strptime(startdate,format)
                enddate_obj = datetime.strptime(enddate,format)
            except:
                print(f"The Start Date {startdate} or End Date {enddate} Format Doesnt Match With dd/mm/yyyy")
            if startdate_obj.date() <= datetime_obj.date() <= enddate_obj.date():
                return True
            else:
                return False
        else:
            return True

    def closed(self,reason):
        """
        This function reads a CSV file, filters it based on a list of subreddits, and saves the filtered
        data back to the same file.
        
        :param reason: The reason parameter is a string that represents the reason for closing the
        connection or WebSocket. It is typically used in WebSocket applications to provide a reason for
        why the connection was closed, such as "normal closure" or "abnormal closure". In this specific
        code snippet, the reason parameter is not used directly
        """
        filename = sys.argv[-1]
        df = pd.read_csv(filename, low_memory=False)
        filtered_df = df[df["Subreddit"].isin(self.subreddits)]
        filtered_df.to_csv(filename, index=False)

    def start_requests(self):
        """
        This function sends a request to each subreddit in a list and calls the "getPosts" function with
        the response.
        """
        for sub in self.subreddits:
            url = f"https://old.reddit.com/r/{sub}/"
            yield scrapy.Request(url, callback=self.getPosts, headers=self.headers)

    def getPosts(self, response):
        """
        This function extracts posts from a Reddit page and follows the next page link if available.
        
        :param response: The response parameter is the HTTP response received after making a request to
        a website using Scrapy. It contains the HTML content of the webpage and can be parsed using
        XPath or CSS selectors to extract the required data
        """
        nextpageurl = response.xpath("//span[@class = 'next-button']/a/@href").get()

        for post in response.xpath(
            "//div[@id = 'siteTable']/div[contains(@class,'thing') and not(contains(@class, 'promoted'))]"
        ):
            posturl = urljoin(self.baseurl, post.xpath(".//@data-url").get())
            if "old.reddit" in posturl:
                yield scrapy.Request(
                    posturl, callback=self.parse, dont_filter=True, headers=self.headers
                )
        if nextpageurl:
            yield scrapy.Request(
                nextpageurl,
                callback=self.getPosts,
                dont_filter=True,
                headers=self.headers,
            )

    def parse(self, response):
        """
        This is a Python function that extracts data from Reddit comments and posts based on certain
        criteria and returns the data as items.
        
        :param response: The response object contains the HTML content of the webpage that was requested
        and is used to extract data using XPath or CSS selectors
        """
        mylist = [li.lower() for li in self.subreddits]
        Subreddit = response.xpath("//div[@id = 'siteTable']/div/@data-subreddit").get()
        if Subreddit.lower() in mylist:
            Thread_title = response.xpath("//p[@class = 'title']/a/text()").get()
            Comment_text = " ".join(
                [
                    i.strip()
                    for i in response.xpath(
                        "//p[@class = 'title']/parent::div/following-sibling::div/form/div/div//text()"
                    ).extract()
                    if i.strip() != ""
                ]
            ).replace("\n", "")
            Comment_poster_ID = response.xpath("//div/@data-author").get()
            Original_poster = 1
            Date_posted = response.xpath(
                "//p[@class = 'tagline ']/time/@datetime"
            ).get()

            category_flags = {}
            for category, keywords in self.category_keywords.items():
                category_flags[category] = (
                    "Yes"
                    if any(keyword in Comment_text.lower() for keyword in keywords)
                    else "No"
                )
            Accounting = category_flags.get("Accounting", "No")
            Finance = category_flags.get("Finance", "No")
            Consultant = category_flags.get("Consultant", "No")
            Marketing = category_flags.get("Marketing", "No")
            Law = category_flags.get("Law", "No")
            Medicine = category_flags.get("Medicine", "No")

            if self.dateInRange(Date_posted):
                items = CrawldataItem()
                items["Subreddit"] = Subreddit
                items["Thread_title"] = Thread_title
                items["Comment_text"] = Comment_text
                items["Comment_poster_ID"] = Comment_poster_ID
                items["Original_poster"] = Original_poster
                items["Date_posted"] = Date_posted
                items["Accounting"] = Accounting
                items["Finance"] = Finance
                items["Consultant"] = Consultant
                items["Marketing"] = Marketing
                items["Law"] = Law
                items["Medicine"] = Medicine
                items["URL"] = response.url
                yield items

            users = response.xpath(
                '//div[@class="sitetable nestedlisting"]//a[contains(@class,"author ")]/text()'
            ).extract()
            datetime = response.xpath(
                '//div[@class="sitetable nestedlisting"]//time/@datetime'
            ).extract()
            for num, replies in enumerate(
                response.xpath(
                    '//div[@class="sitetable nestedlisting"]//div[contains(@class,"usertext-body")]'
                )
            ):
                text = " ".join(
                    [
                        i.strip()
                        for i in replies.xpath(".//text()").extract()
                        if i.strip() != ""
                    ]
                ).replace("\n", "")
                try:
                    PosterId = users[num]
                    postdate = datetime[num]
                except IndexError:
                    break
                Original_poster = 0

                category_flags = {}
                for category, keywords in self.category_keywords.items():
                    category_flags[category] = (
                        "Yes"
                        if any(keyword in text.lower() for keyword in keywords)
                        else "No"
                    )
                Accounting = category_flags.get("Accounting", "No")
                Finance = category_flags.get("Finance", "No")
                Consultant = category_flags.get("Consultant", "No")
                Marketing = category_flags.get("Marketing", "No")
                Law = category_flags.get("Law", "No")
                Medicine = category_flags.get("Medicine", "No")

                if self.dateInRange(postdate):
                    items = CrawldataItem()
                    items["Subreddit"] = Subreddit
                    items["Thread_title"] = Thread_title
                    items["Comment_text"] = text
                    items["Comment_poster_ID"] = PosterId
                    items["Original_poster"] = Original_poster
                    items["Date_posted"] = postdate
                    items["Accounting"] = Accounting
                    items["Finance"] = Finance
                    items["Consultant"] = Consultant
                    items["Marketing"] = Marketing
                    items["Law"] = Law
                    items["Medicine"] = Medicine
                    items["URL"] = response.url
                    yield items
