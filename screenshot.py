from PIL import ImageGrab

def makepscreenshot():
    snapshot = ImageGrab.grab()
    return snapshot

def showscreenshot(snapshot):
    return snapshot.show()


