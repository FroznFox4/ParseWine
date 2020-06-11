import scrapy

#--run a crawler in a script stuff
from pydispatch             import dispatcher
from scrapy                 import signals
from scrapy.crawler         import CrawlerProcess
from pydispatch             import dispatcher
from scrapy.utils.project   import get_project_settings
from os                     import remove
import tablib
#--run a crawler in a script stuff

#--the spiders
from parsewine.spiders.parse_eurocave import ParsWine
#--the spiders

def run_a_spider_on_script(spider, signal=signals.item_passed, slot=None): 
    '''
    @brief  A function given a spider run it. If a signal an a slot is given connect it

    @param  spider
            The spider itself
    
    @param  signal
            scrapy signal ( defualt item passed  )
    
    @param  slot
            Function to launch after the signal is triggered
    '''
    # The spider
    spiderObj = spider()

    # The process to execute the spider
    process = CrawlerProcess( get_project_settings() )

    # if the slot is not None...
    if (slot is not None):
        # Connect the signal with the slot
        # When the signal triggers execute the slot
        dispatcher.connect( slot, signal )

    # Set in the process the spider
    process.crawl( spider )
    # process.start()

    try:
        # f = open('result.json', 'r', encoding='utf-8')
        # text = f.read()
        # f.close()
        name_import = 'result copy.json'
        name_export = 'file.xlsx'
        data = tablib.Dataset(headers = ('name', 'cost', 'status', 'url', 'color'))
        data.json = open(name_import, 'r', encoding='utf-8').read()
        data_export = data.export('xlsx')
        with open(name_export, 'wb') as f:
            f.write(data_export)
        f.close()
    except Exception as err:
        print(err)
        print('gowno')
    finally:
        pass
        # remove('result.json')
    


if __name__ == "__main__":
    run_a_spider_on_script(ParsWine)