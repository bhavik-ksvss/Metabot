# Loading the necessary packages
from metaphor_python import Metaphor
from bs4 import BeautifulSoup
from datetime import date,timedelta

class MetaphorSearch:
    def __init__(self,api_key):
        self.metaphor = Metaphor(api_key)
        #print('API Connection successful!')
    
    def search(self, search_value,keyword = False):
        if keyword == False:
            number_results = 8
            search_response = self.metaphor.search(
                search_value,
                num_results=number_results,
                start_crawl_date = (date.today()).strftime("%Y-%m-%d"),
                use_autoprompt=True)
            #print(len(search_response.results))
            if len(search_response.results) == 0:
                search_response = self.metaphor.search(
                search_value,
                num_results=number_results,
                start_published_date = (date.today()-timedelta(days=7)).strftime("%Y-%m-%d"),
                use_autoprompt=True, )
        else:
            number_results = 8
            print('Now Keyword=True')
            search_response = self.metaphor.search(
                search_value,
                num_results=number_results,
                start_crawl_date = (date.today()).strftime("%Y-%m-%d"),
                type = 'keyword',)
        contents_response = search_response.get_contents()
        documents = [ BeautifulSoup(content.extract.replace('<|endoftext|>',''), 'html.parser').get_text() for content in contents_response.contents]
        #print(len(documents))
        return ' '.join(documents)
        #return documents
