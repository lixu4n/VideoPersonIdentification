import cv2
import numpy as np

class ComparisonHistogram:
    def __init__(self, test_histogram_file, dataset_histogram_file):
        self.test_histogram_file = test_histogram_file
        self.dataset_histogram_file = dataset_histogram_file
        self.test_histograms = self.read_my_histograms_files(self.test_histogram_file)
        self.dataset_histograms = self.read_my_histograms_files(self.dataset_histogram_file)

    def calculate_intersection(self, hist1, hist2):
        '''
        Fonction qui calcule la valeur de l'intersection entre deux histogrammes
        :param hist1:
        :param hist2:
        :return: intersection
        '''
        intersection = cv2.compareHist(hist1, hist2, cv2.HISTCMP_INTERSECT)
        return intersection


    def read_my_histograms_files(self, file_path):
        '''
        lire les fichiers. cette fonction lire mes fichier conetenant les histogrammes de mes images,
        dans notre cas:  histograms_output et new_histograms_output
        :param file_path:
        :return:
        '''

        histograms = {} #init dictionnaire

        with open(file_path, 'r') as file:
            lines = file.readlines()
            current_img_name = None
            current_obj = None
            for line in lines:
                data = line.strip().split(',')
                if len(data) < 8:
                    #ici si pas de data... on skip la lecture de la ligne
                    print("Data on line not complete. Skipping...")
                    continue
                img_name = data[0]
                if img_name != current_img_name:
                    current_img_name = img_name
                    current_obj = 1
                else:
                    current_obj += 1
                x, y, w, h = map(int, data[1:5])
                hist_str1 = data[5]
                hist_str2 = data[6]
                hist1 = np.array(eval(hist_str1), dtype=np.float32)
                hist2 = np.array(eval(hist_str2), dtype=np.float32)
                obj = int(float(data[7]))  # Convert float to int
                histograms.setdefault(img_name, []).append({'x': x, 'y': y, 'w': w, 'h': h, 'hist1': hist1, 'hist2': hist2, 'obj': obj, 'img_name': img_name})  # Store img_name
        return histograms

    def compare_histograms(self, image_data):
        '''
        Compare les histogrammes en utilisant OpenCV.
        :param image_data: Données des histogrammes de l'image de test.
        :return: Dictionnaire contenant les valeurs d'intersection.
        '''
        intersection_values = {}
        test_hist_data = image_data
        for dataset_img_data_list in self.dataset_histograms.values():
            for dataset_hist_data in dataset_img_data_list:
                max_intersection = 0
                intersection_full = cv2.compareHist(test_hist_data['hist1'], dataset_hist_data['hist1'],
                                                    cv2.HISTCMP_INTERSECT)
                intersection_half = cv2.compareHist(test_hist_data['hist2'], dataset_hist_data['hist2'],
                                                    cv2.HISTCMP_INTERSECT)
                intersection = max(intersection_full, intersection_half)
                intersection_values.setdefault(dataset_hist_data['img_name'], []).append(
                    (test_hist_data['obj'], intersection))
        return intersection_values


    def calculate_similarity_percentage(self, intersection_values):
        '''
        calculation de pourcentage de similarite!
        :param intersection_values:
        :return:
        '''
        similarity_percentages = {}
        for img_name, similarity_values in intersection_values.items():
            sorted_values = sorted(similarity_values, key=lambda x: x[1], reverse=True)[:100]
            similarity_percentage = sum(value for _, value in sorted_values) / len(sorted_values)
            similarity_percentages[img_name] = similarity_percentage
        return similarity_percentages


    def write_results_to_file(self, output_file):
        '''
        save all info dans le txt result.txt
        :param output_file:
        :return:
        '''
        with open(output_file, 'w') as file:
            for img_name, hist_data_list in self.test_histograms.items():
                file.write(f"Image {img_name}\n")



                for hist_data in hist_data_list:
                    file.write(f"Object {hist_data['obj']} coordinates: ({hist_data['x']}, {hist_data['y']}, {hist_data['w']}, {hist_data['h']})\n")
                    intersection_values = self.compare_histograms(hist_data)
                    similarity_percentages = self.calculate_similarity_percentage(intersection_values)


                    for dataset_img_name, similarity_percentage in similarity_percentages.items():
                        file.write(f"- Similar image: {dataset_img_name}, Percentage of similarity: {similarity_percentage:.2f}%\n")
                file.write("\n")

