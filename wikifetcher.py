import logging

import wikipedia as wiki

import pandas as pd

import multiprocessing

module_logger = logging.getLogger('getwiki.wikifetcher')

class WikiFetcher:
    
    def __init__(self, term, suggest=False, n_results=10, parallel=True):
        self.logger = logging.getLogger('getwiki.wikifetcher.WikiFetcher')
        self.logger.info('Creating instance of WikiFetcher')
        
        self.term = term
        self.search_term = term
        self.suggest = suggest
        self.n_results = n_results
    
        self.parallel = parallel
        
        self.dataframe = pd.DataFrame()
    
    def fetch(self):
        self.logger.info('Start fetching')
        
        # Call suggestion method and maybe use it
        suggestion = self.__suggest_term()
        if suggestion:
            self.logger('Using suggested term')
            self.search_term = suggestion
            
        # Search
        search_result = self.__search()

        # Get Content
        pool_size = self.__get_pool_size()
        self.logger.info('Using {} cores (CPU).'.format(pool_size))
        
        p = multiprocessing.Pool(pool_size)
        for result in p.imap(WikiFetcher.page_to_dict, search_result):
            self.logger.info('Successfully fetched data of Page "{}"'.format(result['title']))
            self.dataframe = self.dataframe.append(result, ignore_index=True)

        self.dataframe.to_csv('wikipedia_dump.csv')
    
    
    
    def __suggest_term(self):
        ''' Request a suggestion of the term. The request is sent if self.suggest is True.
        
        Returns:    a suggestion search term as string or None
        '''
        if self.suggest:
            suggestion = wiki.suggest(self.term)
            self.logger.info('Suggested term: {}'.format(suggestion))
            
            return suggestion
        
    def __search(self):
        ''' Searches Wikipedia with the self.search_term and return the raw result.
        
        Returns:    a list of page titles
        '''
        result = wiki.search(self.search_term, results=self.n_results)
        self.logger.info('Search Result for "{}": {}'.format(self.search_term, result))
        
        return result

    def __get_pool_size(self):
        ''' Get the number of cores to use.
        Returns the number of physical cores minus 1, or 1 if self.parallel is
        set to False. (minimum value returned is 1)
        '''
        pool_size = 1
        if self.parallel:
            cores = multiprocessing.cpu_count()
            pool_size = max(1, cores - 1)
        
        return pool_size


    @staticmethod
    def page_to_dict(title):
        ''' Request a WikipediaPage for the given title and
        returns the a dictionary containing the information.
        '''
        page = wiki.page(title)
        
        return {
            'title'     : page.title,
            'content'   : page.content,
            'summary'   : page.summary,
            'images'    : ';'.join(page.images),
            'categories': ';'.join(page.categories),
            'link'      : ';'.join(page.links)
        }
    