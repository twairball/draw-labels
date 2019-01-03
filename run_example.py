import pickle
import cv2

from draw_labels.draw import draw_labels

if __name__ == "__main__":
    # read sample data
    image = cv2.imread('example/example.jpg')
    labels = pickle.load(open('example/example.pkl', 'rb'))
    # draw labels
    labeled_image = draw_labels(image, labels)
    # display
    cv2.imshow('demo', labeled_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

