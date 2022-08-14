import cv2
import numpy as np

img_ = cv2.imread('1.jpg')
img_ = cv2.resize(img_, (0,0), fx=1, fy=1)
gray1 = cv2.cvtColor(img_,cv2.COLOR_BGR2GRAY)

img = cv2.imread('2.jpg')
img = cv2.resize(img, (0,0), fx=1, fy=1)
gray2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()
# finding key points
kp1, des1 = sift.detectAndCompute(gray1,None)
kp2, des2 = sift.detectAndCompute(gray2,None)

match = cv2.BFMatcher()
matches = match.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if m.distance < 0.03*n.distance:
        good.append(m)

parameters = dict(matchColor=(0,255,0),
                       singlePointColor=None,
                       flags=2)
img3 = cv2.drawMatches(img_,kp1,img,kp2,good,None,**parameters)

MIN_MATCH_COUNT = 6
#checking if the images has sufficient number of matches or not
if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    #finding homography matrix 
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)

    h,w = gray1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    gray2 = cv2.polylines(gray2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
else:
    print ("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    # if it do not have sufficient matches then both pictures can't be combined
dst = cv2.warpPerspective(img_,M,(img.shape[1] + img_.shape[1], img.shape[0]))
dst[0:img.shape[0], 0:img.shape[1]] = img	

# function for removing the black portion formed due to shifting of image
def trim(frame):
    if not np.sum(frame[0]):
        return trim(frame[1:])
    if not np.sum(frame[-1]):
        return trim(frame[:-2])
    if not np.sum(frame[:,0]):
        return trim(frame[:,1:])
    if not np.sum(frame[:,-1]):
        return trim(frame[:,:-2])
    return frame

cv2.imshow("final_stiched_image.jpg", trim(dst))
cv2.imwrite("final_stiched_image.jpg", trim(dst))
cv2.waitKey()
