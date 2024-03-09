import cv2
import os
import numpy as np

#for my test img....
class ImageGrabCut:
    def __init__(self):
        self.results = []

    def process_images(self, image_folder):
        '''

        :param image_folder:
        :return:
        '''
        # Load images from the folder
        image_files = [file for file in os.listdir(image_folder) if file.endswith('.png') or file.endswith('.jpg')]
        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Failed to read {image_path}")
                continue

            #GrabCut on the image
            result = self.grabcut(image, image_file)

            # Store the results
            self.results.extend(result)

        # Save the results
        with open('labelstest.txt', 'w') as f:
            for r in self.results:
                # Remove the file extension from the image name
                image_name = os.path.splitext(r[0])[0]
                f.write(','.join([image_name] + list(map(str, r[1:]))) + '\n')

        # Print the results
        for r in self.results:
            print(','.join(map(str, r)))

    def grabcut(self, image, image_name):
        '''

        :param image:
        :param image_name:
        :return:
        '''




        cv2.namedWindow('Select ROIs for ' + image_name)
        cv2.imshow('Select ROIs for ' + image_name, image)
        cv2.waitKey(1)  # Needed for the window to appear

        # Initialize empty list to store results for this image
        result = []

        # Allow the user to select ROIs until they press 'q'
        while True:
            # Select ROI using GrabCut
            rect = cv2.selectROI('Select ROIs for ' + image_name, image, fromCenter=False, showCrosshair=True)
            if rect == (0, 0, 0, 0):  # If 'q' is pressed or no ROI selected
                break
            result.append((image_name,) + rect)
            # Perform GrabCut using the selected ROI
            mask = np.zeros(image.shape[:2], np.uint8)
            x, y, w, h = rect
            mask[y:y + h, x:x + w] = cv2.GC_PR_FGD
            bgdModel = np.zeros((1, 65), np.float64)
            fgdModel = np.zeros((1, 65), np.float64)
            cv2.grabCut(image, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

            #mask on image
            masked_img = cv2.bitwise_and(image, image, mask=mask)

            #display
            cv2.imshow('Masked Image', masked_img)
            cv2.waitKey(0)

        cv2.destroyAllWindows()
        return result
