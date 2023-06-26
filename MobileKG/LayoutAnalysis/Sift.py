import cv2

sift = cv2.xfeatures2d.SIFT_create()
FLANN_INDEX_KDTREE=0
indexParams=dict(algorithm=FLANN_INDEX_KDTREE,trees=5)
searchParams=dict(checks=50)
flann=cv2.FlannBasedMatcher(indexParams,searchParams)

def getMatchNum(matches,ratio):
    matchesMask=[[0,0] for i in range(len(matches))]
    matchNum=0
    for i,(m,n) in enumerate(matches):
        if m.distance<ratio*n.distance:
            matchesMask[i]=[1,0]
            matchNum+=1
    return (matchNum,matchesMask)

def compareWithPath(pic1,pic2):
    sampleImage = cv2.imread(pic1, 0)
    kp1, des1 = sift.detectAndCompute(sampleImage, None) 
    queryImage = cv2.imread(pic2, 0)
    kp2, des2 = sift.detectAndCompute(queryImage, None) 
    matches = flann.knnMatch(des1, des2, k=2)
    (matchNum, matchesMask) = getMatchNum(matches, 0.9) 
    matchRatio = matchNum * 100 / len(matches)
    return matchRatio

def comparewithImage(sampleImage, queryImage):
    kp1, des1 = sift.detectAndCompute(sampleImage, None)
    kp2, des2 = sift.detectAndCompute(queryImage, None) 
    if des2 is None:
        return 0
    matches = flann.knnMatch(des1, des2, k=2) 
    (matchNum, matchesMask) = getMatchNum(matches, 0.9)
    matchRatio = matchNum * 100 / len(matches)
    return matchRatio
