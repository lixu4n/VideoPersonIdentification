#class taking both fichier et chercher pour limage, check if image is there, if not then error if yes... calc histogram,,

import cv2
import os

class HistogramCalculatorSub:
    def __init__(self):
        pass

    def calculate_histograms_from_location(self, image_folder_path, labels_file_path, output_file_path):
        '''
        takes in data from  file location
        return files of all historgrams.
        :param image_folder_path:
        :param labels_file_path:
        :param output_file_path:
        :return:
        '''
        try:
            # Create or open the output file in write mode
            with open(output_file_path, 'w') as output_file:
                # Read the labels from the labels file
                with open(labels_file_path, 'r') as file:
                    lines = file.readlines()

                # Iterate over each line in the labels
                for line in lines:
                    # Strip leading and trailing spaces from the line
                    line = line.strip()
                    img_name, x, y, width, height = line.split(',')

                    #grayscale using OenCV
                    img_path = os.path.join(image_folder_path, img_name + '.png')
                    if not os.path.exists(img_path):
                        print(f"Error: Image '{img_path}' not found.")
                        continue

                    img_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img_gray is None:
                        print(f"Error: Failed to load image '{img_path}'.")
                        continue

                    # Extract the region of interest (ROI) based on the coordinates
                    roi_full = img_gray[int(y):int(y) + int(height), int(x):int(x) + int(width)]
                    roi_half = img_gray[int(y):int(y) + int(height), int(x):int(x) + int(width) // 2]

                    # Calculate the histogram for the grayscale ROI (full image)
                    hist_full = cv2.calcHist([roi_full], [0], None, [256], [0, 256])

                    # Calculate the histogram for the grayscale ROI (first half of the image)
                    hist_half = cv2.calcHist([roi_half], [0], None, [256], [0, 256])

                    # Convert histograms to strings
                    hist_full_str = ','.join(str(bin_val[0]) for bin_val in hist_full)
                    hist_half_str = ','.join(str(bin_val[0]) for bin_val in hist_half)

                    # Write the image name, coordinates, and histograms to the output file
                    output_file.write(f"{img_name},{x},{y},{width},{height},{hist_full_str},{hist_half_str}\n")

        except Exception as e:
            print("Error:", e)
