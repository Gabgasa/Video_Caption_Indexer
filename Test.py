import unittest
from CaptionProcessor import CaptionProcessor
from IndexProcessor import IndexProcessor
import Utils
import yaml

#For testing purpose
#yt_links = ['https://youtu.be/dsSbhW7JoCg',
#            'https://youtu.be/B9KjBEFZ3io',
#           'https://youtu.be/1sWNF4n6-pM']

try:
    with open("config.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        solr_url = config["solr_url"]
except:
    Exception("Couldn't open config.yaml file.")

class TestUtils(unittest.TestCase):
    def test_youtube_id_extractor(self):
        #Testing 3 different links with 2 type ofs youtube links
        self.assertEqual(Utils.youtubeIdExtractor('https://youtu.be/dsSbhW7JoCg'), 'dsSbhW7JoCg')
        self.assertEqual(Utils.youtubeIdExtractor('https://www.youtube.com/watch?v=dsSbhW7JoCg'), 'dsSbhW7JoCg')

        self.assertEqual(Utils.youtubeIdExtractor('https://youtu.be/B9KjBEFZ3io'), 'B9KjBEFZ3io')
        self.assertEqual(Utils.youtubeIdExtractor('https://www.youtube.com/watch?v=B9KjBEFZ3io'), 'B9KjBEFZ3io')

        self.assertEqual(Utils.youtubeIdExtractor('https://youtu.be/1sWNF4n6-pM'), '1sWNF4n6-pM')
        self.assertEqual(Utils.youtubeIdExtractor('https://www.youtube.com/watch?v=1sWNF4n6-pM'), '1sWNF4n6-pM')

    def check_video_url(self):
        #Testing 3 correct video Ids and 3 wrong video Ids
        self.assertEqual(Utils.check_video_url('dsSbhW7JoCg'), True)
        self.assertEqual(Utils.check_video_url('B9KjBEFZ3io'), True)
        self.assertEqual(Utils.check_video_url('1sWNF4n6-pM'), True)

        self.assertEqual(Utils.check_video_url('dsSbhW7JoCg1'), False)
        self.assertEqual(Utils.check_video_url('B9KjBEFZ3Io'), False)
        self.assertEqual(Utils.check_video_url('1sWNF4n6-pMk'), False)

    def adjust_timestamp(self):
        #Testing a bunch of different amounts of seconds to see if it properly formats the time
        self.assertEqual(Utils.adjustTimestamp(170), '0 hour(s) 2 minute(s) 50 second(s)')
        self.assertEqual(Utils.adjustTimestamp(3600), '1 hour(s) 0 minute(s) 0 second(s)')
        self.assertEqual(Utils.adjustTimestamp(60), '0 hour(s) 1 minute(s) 0 second(s)')
        self.assertEqual(Utils.adjustTimestamp(3661), '1 hour(s) 1 minute(s) 1 second(s)')
        self.assertEqual(Utils.adjustTimestamp(3661), '1 hour(s) 1 minute(s) 1 second(s)')        

class TestCaptionProcessor(unittest.TestCase):
    def test_get_caption(self):
        #Checking if the method is getting the caption correctly
        self.assertGreater(len(CaptionProcessor.getCaption('dsSbhW7JoCg')), 0)

class TestIndexProcessor(unittest.TestCase):
    def test_search(self):
        #Verificando se o resultado está ordenado da forma correta, e.g. "palavras juntas" 
        #devem ter score maior por proximidade na frase, keywords individuais ainda aparecem 
        # porem com score menor ainda.
        ip = IndexProcessor(solr_url)        
        ip.clearIndex()        
        ip.indexCaption([ {'start': 1, 'caption': 'palavras juntas'},
                            {'start': 2, 'caption': 'palavras lorem ipsum juntas'},
                            {'start': 3, 'caption': 'palavras lorem ipsum dolor sit juntas'},
                            {'start': 4, 'caption': 'palavras lorem ipsum dolor sit amet consectetur juntas'},
                            {'start': 5, 'caption': 'palavras lorem ipsum'},
                            {'start': 6, 'caption': 'lorem ipsum juntas'},
                            {'start': 7, 'caption': 'nenhuma das anteriores'}])        
        
        results = ip.search('palavras juntas')
        #Verificando se pegou os resultados de 1 a 6 como esperado
        self.assertEqual(len(results), 6)
        i = 1
        for res in results:
            self.assertEqual(res['start'][0], i)
            i+=1
        ip.solr.get_session().close()

if __name__ == '__main__':
    unittest.main()

