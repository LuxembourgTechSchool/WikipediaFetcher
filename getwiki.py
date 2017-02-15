import os
import argparse
import logging

from wikifetcher import WikiFetcher

# Logging
##################################################################

logger = logging.getLogger('getwiki')

def setup_logger(verbosity, is_file_log):
    if not verbosity:
        verbosity = 1
    
    verbosity = (verbosity - 1) * 10 # 1,2,3,4... to 10, 20, 30, 40
    verbosity = max(logging.DEBUG, logging.ERROR - verbosity) # Take reverse or max, because verbosity -v = 1 = ERROR

    logger.setLevel(verbosity)
    
    #formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s - %(name)s : %(message)s')
    formatter = logging.Formatter('[%(asctime)s] %(levelname)-8s : %(message)s [%(name)s]')
    
    # Console Logger
    ch = logging.StreamHandler()
    ch.setLevel(verbosity)
    
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    # File Logger
    if is_file_log:
        import datetime
        fh = logging.FileHandler('log_{}.txt'.format( datetime.datetime.now().strftime("%Y%m%d_%H%M%S") ))
        fh.setLevel(verbosity)

        fh.setFormatter(formatter)
        logger.addHandler(fh)

# Argument Parser
##################################################################

parser = argparse.ArgumentParser(description='Fetch Wikipedia Pages')

parser.add_argument('-o', '--output',
                    type=str, default='output.csv',
                    help='The output filename as a string with the CSV extension. (e.g. -o "path/to/my_file.csv")')

parser.add_argument('-t', '--term',
                    type=str,
                    help='The search term to use for finding wikipedia entries. (e.g. -t "Python")')

parser.add_argument('-n', '--n-results',
                    type=int,
                    help='The number of results to get for the search term')

parser.add_argument('-v', '--verbose', action='count',
                    help='Sets the logging level for console. Also affects file logging is enabled. (1: ERROR, 2: WARNING, 3: INFO, 4: DEBUG)')

parser.add_argument('-lf', '--log-file',
                    default=False, action="store_true",
                    help='Flag to save logs to file.')

parser.add_argument('-s', '--suggest',
                    default=False, action="store_true",
                    help='Flag use the Wikipedia suggest feature. (e.g. "Taylo Swif" will be changed to "Taylor Swift")')

args = vars(parser.parse_args()) # vars() transform the arguments to dictionary

# TODO:
# - links/depth: Traverse links, 0,1,2... depth more
# -

# Main Run Method
##################################################################

def run(arguments):
    print('****************************')
    print('       Start Get Wiki')
    print('****************************')
    
    print('\nArguments:')
    for arg in sorted(arguments.keys()):
        print('  - {:10} : {}'.format(arg, arguments[arg]))
    print()

    # Validate arguments
    
    is_arguments_ok = True
    
    if not arguments['term']:
        logger.info('[INTERUPTION] No term has been given. Please add a search term using -t or --term. Use -h, --help for help.')
        is_arguments_ok = False
    
    if is_arguments_ok:
        logger.info('Arguments are valid. Starting to scrap Wikipedia...')

        wf = WikiFetcher(arguments['term'], suggest=arguments['suggest'], n_results=arguments['n_results'])
        wf.fetch()

 
    
# Main
##################################################################

if __name__ == '__main__':
    setup_logger(args['verbose'], args['log_file'])
    run(args)

