from OCRProcessor import OCRProcessor


op = OCRProcessor('https://youtu.be/dsSbhW7JoCg')
op.downloadVideo()

op.detectSlideTransitions()
print("Number of slides: %d" % len(op.slides))