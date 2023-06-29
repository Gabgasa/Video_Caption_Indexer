import cv2
import pytube
import Utils
import numpy

class OCRProcessor:
    slides = []
    video = None

    def __init__(self, yt_link : str) -> None:
        """Initialization.

        Args:
            TODO
        """ 
        try:
            yt = pytube.YouTube(yt_link)
        except:
            print("Connection Error")
        self.video = yt.streams.get_highest_resolution()
        return

    def downloadVideo(self) -> None:
        try:
            self.video.download()
        except:
            print("Errror downloading the video")
        return

    def detectSlideTransitions(self) -> None:
        """Detects the change of slides and store the new slide in the frames variable

        Args:
            path string: Path to the video
        """
        
        cap = cv2.VideoCapture(self.video.get_file_path())
        count=0
        fps = cap.get(cv2.CAP_PROP_FPS)
        skipframes = fps*5
        past_frame = None
        current_frame = None
        matches = None
        current_matches = None
        past_matches = None
        desc_past = None
        desc_current = None

        while cap.isOpened():
            ret, frame = cap.read()
            good = []
            
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                width = img.shape[1]
                img_processed = img[:, 0:int(width*0.8)]
                current_frame = cv2.resize(img_processed, (256,256))
                sift = cv2.xfeatures2d.SIFT_create(500)

                kp_current, desc_current = sift.detectAndCompute(current_frame, None)
                if past_frame is not None:           
                    #bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
                    kp_past, desc_past = sift.detectAndCompute(past_frame, None)
                    
                    FLANN_INDEX_KDTREE = 0
                    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
                    search_params = dict(checks = 50)
                    flann = cv2.FlannBasedMatcher(index_params, search_params)
                    matches = flann.knnMatch(desc_past, desc_current, k=2)

                    for m, n in matches:
                        if m.distance < 0.7 * n.distance:
                            good.append(m)
                    p1=(float(len(good))/len(kp_past))*100
                    p2=(float(len(good))/len(kp_current))*100
                    #current_matches = len(bf.match(desc_current,desc_past))
                    #print("Current Matches: %d" % current_matches)
                    if past_matches is None:
                        past_matches = current_matches

                if matches is not None and (p1 < 75 or p2 < 75): #New slide detected
                    
                    print("New slide at time: " + Utils.adjustTimestamp((count/fps)-5))
                    cv2.imshow("Image", img_processed)
                    cv2.waitKey(0)
                    self.slides.append(img_processed)
                elif matches is None: #First Slide
                    print("First slide at time: " + Utils.adjustTimestamp(count/fps))
                    cv2.imshow("Image", img_processed)
                    cv2.waitKey(0)
                    self.slides.append(img_processed)

                count += skipframes
                cap.set(cv2.CAP_PROP_POS_FRAMES, count)

                past_frame = current_frame

            else:
                cap.release()
                break

    def clearStoredVideo(self) -> None:
        self.slides = []
        return

