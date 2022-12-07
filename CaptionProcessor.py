from youtube_transcript_api import YouTubeTranscriptApi

#A caption consists of a series of objects with a timestamp and its text.
class CaptionProcessor:   
    def getCaption(youtube_id : str) -> list[dict[int,str]]:
        """Attempts to get the caption for the youtube video, by default the API will get the manually generated
        caption over the automatically generated one.

        Args:
            youtube_id (str): id for the youtube video.

        Raises:
            Exception: Unable to recover caption.

        Returns:
            Caption: Full caption with timestamps and text
        """
        try:
           transcript =  YouTubeTranscriptApi.get_transcript(youtube_id, languages = ['pt'])
        except:
            raise Exception('Unable to recover the Caption for the video.')
        caption = []
        i = 0
        #We will not need the duration of the caption so we grab only start and text
        for i in range(len(transcript)):
            start = int(transcript[i]['start'])
            text = transcript[i]['text']
            caption.append({'start':start, 'caption': text})
        
        return caption

        