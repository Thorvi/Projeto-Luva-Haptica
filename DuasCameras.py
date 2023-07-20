import cv2

cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)

while cap1.isOpened() & cap2.isOpened():
    success, image1 = cap1.read()
    success, image2 = cap2.read()

    cv2.imshow('Camera 1', cv2.flip(image1, 1))
    cv2.imshow('Camera 2', cv2.flip(image2, 1))

    if cv2.waitKey(5) & 0xFF == 27:
        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()
        break