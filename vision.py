import cv2 as cv
import numpy as np

class Vision:

    #properties
    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None

    #contructior
    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

        #save demonsions of needle
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]

        #method it will use
        self.method = method


    def find(self, field_img, threshold = 0.3 , img_mode=None):

        result = cv.matchTemplate(field_img, self.needle_img, self.method)

        #threshold is inverted becuase we r useing SQDIFF which looks for black pixels not white
        #threshold = 0.6
        locations = np.where(result >= threshold)

        #turning x and y into tuples
        locations = list(zip(*locations[::-1]))

        #makeing list to group rectanbgle so we dont get more than 1 result in a place
        #list formated per rectangle as [x, y, w, h]
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
        print(rectangles)

        points = []

        if len(rectangles):
            print('Found needle(s). ')

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            #unpacks rectangle variables and draws rectangle over objects
            for (x, y, w, h) in rectangles:

                #find center points
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)
                #saveing points to list
                points.append((center_x, center_y))

                if img_mode == 'boxes':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    #drawing box
                    cv.rectangle(field_img, top_left, bottom_right, line_color, line_type)

                elif img_mode == 'points':
                    cv.drawMarker(field_img, (center_x, center_y), marker_color, marker_type)

        if img_mode:
            cv.imshow('Matches', field_img)
            #stops window from closeing until keyboard pressed. This is already in window capture file
            #cv.waitKey()

        return points

    #pass in what images you want to use and other variables inside of class like image mode
    #points = findclickpositions('white horses2 haystack.jpg', 'white horses2 needle.jpg', img_mode='boxes')
    #print(points)