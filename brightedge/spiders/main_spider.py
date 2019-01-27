import scrapy
import spacy
import string
from bs4 import BeautifulSoup
import re

class MainSpider(scrapy.Spider):
    name = "scraper"
    def start_requests(self):
        urls = [
            'http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/',

            'http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/',

            'http://www.amazon.com/Cuisinart-CPT-122-Compact-2-SliceToaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        page = response.url.split("/")[2]
        filename = '%s.txt' % page
        soup = BeautifulSoup(response.text, 'lxml')
        headers = soup.find_all(re.compile('^h[1-6]$'))
        headers_text = ''
        for headlines in headers:
            headers_text += headlines.text.strip() + '. '
        # print(headers_text)
        # Remove all extraneous text like links images vidoes ads
        for script in soup(["script", "style","a","span","i","input","textarea","img"]):
            script.decompose()    # rip it out
        # get text
        all_p = soup.find_all('p')

        text = soup.get_text()
        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        nlp = spacy.load('en_core_web_sm')
        sentences = nlp(text)
        # print(sentences)
        output_list = {}
        # Create key topics list and frequency using lemming and sentence trees
        # bad_list = ['he','she','to','they','He','She','who','Who','it']
        for token in sentences:
            if token.dep_ == 'nsubj' or token.tag_ == 'NNP':
                if token.text not in string.punctuation and token.tag_ != 'PRP' and token.tag_ != 'DT' and token.tag_ != 'WP' and token.text.isalpha() :
                    in_text = token.text
                    weight = 1
                    if token.tag_ == 'NN':
                        in_text = token.lemma_
                    if token.dep_ == 'nsubj':
                        weight += 1
                    if token.tag_ == 'NNP':
                        weight += 1
                    if in_text == 'he':
                        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_)
                    if in_text not in output_list:
                        output_list[in_text] = 0
                    output_list[in_text] += 1
        # print(output_list)
        # Sort and take top five topics and Print them
        final_list = sorted(output_list, key=output_list.__getitem__, reverse=True)
        tags = final_list[:max(len(final_list)//10,5)]
        print(tags)
        # Save all scraped text to txt file with name "top-domainname.txt"
        with open(filename, 'w') as f:
            f.write(text)
        tagfile = '%s_tags.txt' % page
        with open(tagfile, 'w') as f:
            f.write((',').join(tags))
        self.log('Saved file %s' % filename)
