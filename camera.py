import numpy as np
import cv2 as cv
import matplotlib
import time
import random
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.preprocessing import normalize

fileL = "/Users/newowner/Dev/img/L.png"
fileR = "/Users/newowner/Dev/img/R.png"
# streamL = "http://10.0.0.162:8080/stream/video.mjpeg"
# streamR = "http://10.0.0.62:8080/stream/video.mjpeg"
streamL = "http://172.20.10.10:8080/stream/video.mjpeg"
streamR = "http://172.20.10.11:8080/stream/video.mjpeg"
capL = cv.VideoCapture()
capR = cv.VideoCapture()
fast = cv.FastFeatureDetector_create(40)
# stereo = cv.StereoSGBM_create(
# 	minDisparity = 16,
# 	numDisparities = 16,
# 	blockSize = 16,
# 	P1 = 8*3*3**2,
# 	P2 = 32*3*3**2,
# 	disp12MaxDiff = 1,
# 	uniquenessRatio = 10,
# 	speckleWindowSize = 100,
# 	speckleRange = 32
# )
left_matcher = cv.StereoSGBM_create(
    minDisparity=-16,
    numDisparities=16,      # max_disp has to be dividable by 16 f. E. HH 192, 256       
    blockSize=5,
    P1=8 * 3 * 3 ** 2,    	# wsize default 3; 5; 7 for SGBM reduced size image; 
							# 15 for SGBM full size image (1300px and above); 5 Works nicely
    P2=32 * 3 * 3 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=15,
    speckleWindowSize=0,
    speckleRange=2,
    preFilterCap=63,
    mode=cv.STEREO_SGBM_MODE_SGBM_3WAY
)
right_matcher = cv.ximgproc.createRightMatcher(left_matcher)
ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def displayStereo(L, R, title):
	numpy_horizontal = np.hstack((L, R))
	numpy_horizontal_concat = np.concatenate((L, R), axis=1)
	cv.imshow(title, numpy_horizontal_concat)


def runFAST(L, R):
	#---Creating image of solid color with same size as image---
	mask = np.zeros((L.shape[0], L.shape[1], 3), np.uint8)
	mask[:] = (0, 0, 0) 

	kpL = fast.detect(L, None)
	kpR = fast.detect(R, None)
	imgL2 = cv.drawKeypoints(mask, kpL, None, color=(0,255,0))
	imgR2 = cv.drawKeypoints(mask, kpR, None, color=(0,255,0))
	displayStereo(imgL2, imgR2, 'FAST')

	return imgL2, imgR2, kpL, kpR


def runEdgeDetection(L, R):
	edged_frameL = cv.Canny(L, 100, 200)
	edged_frameR = cv.Canny(R, 100, 200)
	displayStereo(edged_frameL, edged_frameR, 'EDGE')

	return edged_frameL, edged_frameR


def runDisparity(L, R):
	disparity = left_matcher.compute(L, R).astype(np.float32) / 16.0
	cv.imshow('Disparity', (disparity-16.0)/16.0)

	return disparity


def runCensusTransform(L, R):
	h, w = L.shape

	#Initialize output array
	censusL = np.zeros((h-2, w-2), dtype='uint8')
	censusR = np.zeros((h-2, w-2), dtype='uint8')

	#centre pixels, which are offset by (1, 1)
	cpL = L[1:h-1, 1:w-1]
	cpR = R[1:h-1, 1:w-1]

	#offsets of non-central pixels 
	offsetsL = [(uL, vL) for vL in range(3) for uL in range(3) if not uL == 1 == vL]
	offsetsR = [(uR, vR) for vR in range(3) for uR in range(3) if not uR == 1 == vR]

	#Do the pixel comparisons
	for u,v in offsetsL:
	    censusL = (censusL << 1) | (L[v:v+h-2, u:u+w-2] >= cpL)
	for u,v in offsetsR:
	    censusR = (censusR << 1) | (R[v:v+h-2, u:u+w-2] >= cpR)

	displayStereo(censusL, censusR, 'Census Transformation')

	return censusL, censusR

def runDepth(L, R):
	lmbda = 80000
	sigma = 1.2
	visual_multiplier = 1.0
	wls_filter = cv.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
	wls_filter.setLambda(lmbda)
	wls_filter.setSigmaColor(sigma)

	displ = left_matcher.compute(L, R)  		# .astype(np.float32)/16
	dispr = right_matcher.compute(R, L)  		# .astype(np.float32)/16
	displ = np.int16(displ)
	dispr = np.int16(dispr)
	filteredImg = wls_filter.filter(displ, L, None, dispr)  # important to put "imgL" here!!!
	filteredImg = cv.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv.NORM_MINMAX);
	filteredImg = np.uint8(filteredImg)
	cv.imshow('Disparity Map', filteredImg)

	return filteredImg

def generatePointCloud(img, disp):
	print('generating 3d point cloud...',)
	h, w = img.shape[:2]
	f = 0.8*w                          			# guess for focal length
	Q = np.float32([[1, 0, 0, -0.5*w],
                    [0,-1, 0,  0.5*h], 			# turn points 180 deg around x-axis,
                    [0, 0, 0,     -f], 			# so that y-axis looks up
                    [0, 0, 1,      0]])
	points = cv.reprojectImageTo3D(disp, Q)
	colors = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	mask = disp > disp.min()
	out_points = points[mask]
	out_colors = colors[mask]
	out_fn = 'out2.ply'
	write_ply('out2.ply', out_points, out_colors)
	print('%s saved' % 'out2.ply')

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'wb') as f:
        f.write((ply_header % dict(vert_num=len(verts))).encode('utf-8'))
        np.savetxt(f, verts, fmt='%f %f %f %d %d %d ')

def main():
	count = 0
	capL.open(streamL)
	capR.open(streamR)

	while(True):
	    retL, frameL = capL.read()
	    retR, frameR = capR.read()
	    grayL = cv.cvtColor(frameL, cv.COLOR_BGR2GRAY)
	    grayR = cv.cvtColor(frameR, cv.COLOR_BGR2GRAY)

	    # Detect Feature/Support Points
	    runEdgeDetection(grayL, grayR)
	    runFAST(grayL, grayR)	

	    # Compute Census Transform
	    runCensusTransform(grayL, grayR)

	    # Sparse Stereo Matching
	    # runDisparity(L, R)
	    runDepth(grayL, grayR)

	    # Display
	    displayStereo(frameL, frameR, 'Original')

	    #if count % 10 == 0 :
		    #Generate 3D Point Cloud
		    #generatePointCloud(frameL, D)

	    if cv.waitKey(1) & 0xFF == ord('q'):
	        break
	    
	    count += 1

	    # time.sleep(1)

	capL.release()
	capR.release()
	cv.destroyAllWindows()

if __name__ == '__main__':
	main()