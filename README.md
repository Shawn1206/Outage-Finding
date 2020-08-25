# Outage-Finding
All the resources in this project is for Columbia University's SNL's COVID-19 project.

## Details about data
1. Facebook: data from Facebook is not included now. Because the quality(the ratio of posts contain locational words) and the quantity of the posts in private groups is rather low. 
2. Twitter: data/Twitter_outage_Xfinity.txt

       -1. Current data include the tweet and username and timestamp
       -2. Current data is all the tweets from Jan/2020 to August/2020 searched by keyword 'outage Xfinity'
       -3. You can refer to the function twitter_sp in nlp project/info_extraction.py to know how to use the data
3. Reddit: data/reddit_data4.csv 

       -1. Current scraping tool can scrape the posts(comments not included), each entry is consist of timestamp, subreddit, title and text.
       -2. Current data is all the posts from Jan/2020 to August/2020 searched by keyword 'outage' in the subreddit 'Comcast Xfinity'
       -3. You can refer to the function reddit_sp in nlp project/info_extraction.py to know how to use the data
4. Forum: data/forum_data0.1.txt

       -1. Current scraping tool can only scrape the preview part of the posts(the first 80 words, no replies included) shown on the searching web-page, as well as timestamp and username
       -2. Current data is all the posts from Jan/2020 to August/2020 searched by keyword 'outage' in the Comcast Xfinity's official customer forum
       -3. You can refer to the function forum_sp in nlp project/info_extraction.py to know how to use the data
            
