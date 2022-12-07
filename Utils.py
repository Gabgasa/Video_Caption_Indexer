import requests

def youtubeIdExtractor(youtube_link : str) -> str:
    """Will attempt to extract the id from the youtube video.

    Args:
        youtube_link (str): A link for a youtube video.

    Raises:
        ValueError: Invalid youtube link.

    Returns:
        str: The id for the youtube video.
    """
    #Shortened version of youtube link doesn't have "?v="
    if 'youtu.be' in youtube_link:
        idstart = youtube_link.rfind("/") + 1
        idend = len(youtube_link)
        youtube_id = youtube_link[idstart:idend]
        
    
    else:
        idstart = youtube_link.find("?v=")+3
        idend = youtube_link[idstart:].find('&')
        if idend == -1:
            youtube_id = youtube_link[idstart:]
        else:
            youtube_id = youtube_link[idstart : idstart + idend]
        
    
    if not check_video_url(youtube_id):
        raise ValueError("Your youtube link is invalid, check again if it is the correct link.")
    
    return youtube_id

def check_video_url(youtube_id : str) -> bool:
    """Checks if the link provided by the user is a valid youtube link.

    Args:
        youtube_link (str): A link for a youtube video.
    Returns:
        bool: True if the video is valid and False if it isn't.
    """     
    
    check_url = "https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v="
    video_url = check_url + youtube_id
    
    return requests.get(video_url).status_code == 200

def adjustTimestamp(seconds : int) -> str:
    """Formats the time from seconds to Hours Minutes and seconds to make it easier to understand the timestamp from the video.

    Args:
        seconds (int): The timestamp in seconds

    Returns:
        str: A formated time with hours minutes and seconds
    """
    assert seconds > 0

    hours = int(seconds/3600)
    minutes = int(seconds/60)
    seconds = seconds - hours*3600 - minutes*60
    return "{0} hour(s) {1} minute(s) {2} second(s)".format(hours,minutes,seconds)

def showResults(results : dict[list[int], str, str, str]) -> None:
    """This function will format and display the results found by the query.

    Args:
        results (dict[list[int], str, str, str]): This is the object returned by solr which contains the results of
    """    
    for res in results:
        start = adjustTimestamp(res['start'][0])
        caption = res['caption']
        print('Start: {0}, Caption:"{1}"'.format(start,caption))