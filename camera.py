import numpy as np
import cv2 as cv
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt


def display(L, R):
    cv.imshow('L', L)
    cv.imshow('R', R)
    # plt.imshow(disparity,'gray')
    # plt.show()

def runFAST(L, R):
 	# find and draw the keypoints
    kpL = fast.detect(L, None)
    kpR = fast.detect(R, None)
    imgL2 = cv.drawKeypoints(L, kpL, None, color=(255,0,0))
    imgR2 = cv.drawKeypoints(R, kpR, None, color=(255,0,0))
    
    # Disable nonmaxSuppression
    # fast.setNonmaxSuppression(0)
   	# kpL = fast.detect(L, None)
    # kpR = fast.detect(R, None)
    # print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
    # imgL3 = cv.drawKeypoints(L, kpL, None, color=(255,0,0))
    # imgR3 = cv.drawKeypoints(R, kpR, None, color=(255,0,0))
    # cv.imwrite('fast_true.png', img2)
    # cv.imwrite('fast_false.png',img3)

    return imgL2, imgR2

def runEdgeDetection(L, R):
	edged_frameL = cv.Canny(L,100,200)
	edged_frameR = cv.Canny(R,100,200)

	return edged_frameL, edged_frameR

def runDisparity(L, R):
	# disparity = stereo.compute(imgL, imgR)
	disparity = stereo.compute(L, R).astype(np.float32) / 16.0
	
	return disparity

if __name__ == '__main__':
	fileL = "/Users/newowner/Dev/img/L.png"
	fileR = "/Users/newowner/Dev/img/R.png"
	streamL = "http://10.0.0.162:8080/stream/video.mjpeg"
	streamR = "http://10.0.0.62:8080/stream/video.mjpeg"
	capL = cv.VideoCapture()
	capR = cv.VideoCapture()
	capL.open(streamL)
	capR.open(streamR)
	fast = cv.FastFeatureDetector_create(50)
	# stereo = cv.StereoBM_create(numDisparities=16, blockSize=15)
	stereo = cv.StereoSGBM_create(minDisparity = 16,
		numDisparities = 112-min_disp,
		blockSize = 1,
		P1 = 8*3*3**2,
		P2 = 32*3*3**2,
		disp12MaxDiff = 1,
		uniquenessRatio = 10,
		speckleWindowSize = 100,
		speckleRange = 32
	)

	# Print all default params
	print( "Threshold: {}".format(fast.getThreshold()) )
	print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
	print( "neighborhood: {}".format(fast.getType()) )
	#print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )

	while(True):
	    # imgL = cv.imread(fileL,0)
		# imgR = cv.imread(fileR,0)
	    retL, frameL = capL.read()
	    retR, frameR = capR.read()
	    grayL = cv.cvtColor(frameL, cv.COLOR_BGR2GRAY)
	    grayR = cv.cvtColor(frameR, cv.COLOR_BGR2GRAY)
	    # L, R = runEdgeDetection(grayL, grayR)
	    # disparity = runDisaparity(grayL, grayR)
	    L, R = runFAST(grayL, grayR)	   
	    display(L, R)
	    	
	    if cv.waitKey(1) & 0xFF == ord('q'):
	        break

	capL.release()
	capR.release()
	cv.destroyAllWindows()