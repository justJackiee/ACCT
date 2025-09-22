import cv2

foo = cv2.imread("./flag_7ae18c704272532658c10b5faad06d74.png")
bar = cv2.imread("./lemur_ed66878c338e662d3473f0d98eedbd0d.png")

key = cv2.bitwise_xor(foo, bar)
cv2.imshow("xored data", key)
cv2.waitKey(0)