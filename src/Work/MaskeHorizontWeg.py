# import opencv
import cv2 as cv

# Loading images
img1 = cv.imread("/home/pi/FE_2025/Work/Bilder_machen/Bilder/Weg_vor_auto_04.01.2025.png")
img2 = cv.imread("/home/pi/FE_2025/Data/Mask_white_top.png")

# We want to put the logo on the top-left corner, so we create ROI
rows, cols, channels = img2.shape
roi = img1[0:rows, 0:cols]

# Now create a mask of the logo and create its inverse mask, also
img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 10, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

# Now black out the area of the logo in ROI
img1_bg = cv.bitwise_and(roi, roi, mask=mask_inv)

# Take only the region of the logo from the logo image.
img2_fg = cv.bitwise_and(img2, img2, mask=mask)

# Put logo in ROI and modify the main image
dst = cv.add(img1_bg, img2_fg)
img1[0:rows, 0:cols] = dst

cv.imshow("mask", mask)
cv.imshow("inv_mask", mask_inv)
cv.imshow("img1_bg", img1_bg)
cv.imshow("img2_fg", img2_fg)
cv.imshow("Final image", img1)
cv.waitKey(0)
cv.destroyAllWindows()