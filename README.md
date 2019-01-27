# Scraping Webpage and Deducing its Topic using NLP

## Project Setup

`pip install Scrapy beautifulsoup4 ` <br>
`pip install spacy && python3 -m spacy download en_core_web_sm`


## Project Run

- All Links to be scraped are in [../brightedge/spiders/main_spider.py](../brightedge/spiders/main_spider.py)
- The data scraped is cleaned and stored in **_"domainname".txt_** in the base of this directory
- All generated list of topics are stored in **_"domainname_tags.txt"_** in the base of this directory

### Run
`scrapy crawl scraper`

### Results
 Outputed in terminal in form of a list immediately after every webpage being crawled.
 They are also stored in txt file in base of directory
 They are stored for every crawl in `tags` variable in **_main_spider.py_**
