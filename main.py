import sys
from CaptionProcessor import CaptionProcessor
from IndexProcessor import IndexProcessor
import Utils
import yaml


def main():
    assert len(sys.argv) == 3
    
    try:
        with open("config.yaml", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except:
        Exception("Couldn't open config.yaml file.")
    
    solr_url = config['solr_url']
    youtube_link = sys.argv[1]
    query = sys.argv[2]

    

    #Connects to the solr server
    ip = IndexProcessor(solr_url)
    
    #Clears the solr server to prepare for a new video
    ip.clearIndex()

    #Extracts the id from the youtube link
    youtube_id = Utils.youtubeIdExtractor(youtube_link)
    
    #Check if its a valid youtube id
    if Utils.check_video_url(youtube_id):
        caption = CaptionProcessor.getCaption(youtube_id)
        ip.indexCaption(caption)
        results = ip.search(query)
        print("\nDisplaying {0} top results.\n".format(len(results)))
        Utils.showResults(results)

        
    else:
        raise Exception('Invalid youtube link')

    ip.solr.get_session().close()


if __name__ == '__main__':
    main()