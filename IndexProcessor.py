import pysolr

class IndexProcessor:
    solr = None
    def __init__(self, solr_url : str) -> None:
        """Initialization.

        Args:
            solr_url (str): A url for the connection with a solr server.
        """ 
        try:
            self.solr = pysolr.Solr(solr_url)
        except:
            Exception('Error when attempting connection to the Solr server, check if the url is correct') 
  


    def indexLine(self, line : dict[int,str]) -> None:
        """Will attempt to index a single line from the Caption.

        Args:
            line (dict[int,str]): One line from the caption list containing a start timestamp and a text
        """       
        try:
            self.solr.add([{"start" : line['start'], "caption": line['caption']}])
        except:
            Exception("Failed to add a line to Solr.")

    def indexCaption(self, caption : list[dict[int,str]]):
        """This will attempt to index all lines from the caption.

        Args:
            caption (list[dict[int,str]]): A list of dict objects that contain a start timestamp and a text.
        """        
        
        i = 0
        for i in range(len(caption)):
            self.indexLine(caption[i]) 
        self.solr.commit()
        
    def search(self, search : str) -> list[dict[int, str]]:
        """This will search the captions for the string inputed.

        Args:
            search (str): The string representing the term the user is searching in the video.

        Returns:
            list[dict[int, str]]: The matches for the search, the int represents the time in seconds of the video and str the text found.
        """
        captionField = "caption:\""
        i = 0
        searchString = search
        keywords = searchString.split()
        if len(keywords) == 1:
            return self.solr.search("caption:" + keywords[0])
        
        else:
            #Doing the proximity search ex: caption:"keyword1 keyword2 keyword3 ... keywordn"~10
            searchString = captionField
            for i in range(len(keywords)-1):
                searchString = searchString + keywords[i] + " "
            searchString = searchString + keywords[i+1] + "\"~10" 

            #Searching for individual keywords in case it doesn't have all keywords in the same query
            for i in range(len(keywords)):
                searchString = searchString + " " + "OR" + " " + "caption:" + keywords[i]
            
            results = self.solr.search(searchString)

            return results
        

    def clearIndex(self):
        """Will clear the index from solr to get ready for a new video.
        """        
        self.solr.delete(q='*:*')
        self.solr.commit()