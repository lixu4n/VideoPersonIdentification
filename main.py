#logique de mon programme.
#run le main.py to test.




from objectLocationSelector import ImageGrabCut
from HistogramCalculatorSub import HistogramCalculatorSub
from CompaisonHistogram import ComparisonHistogram

if __name__ == "__main__":
    # Step 1 - Prep the Data for test images.
    # Run objectLocationSelector.py to generate labelstest.txt for the first set of images
    folder_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/test_images'
    image_grabcut = ImageGrabCut()
    image_grabcut.process_images(folder_path)

    # Path to the generated labels file for the first set of images
    labels_file_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/labelstest.txt'

    # Path to the folder containing test images for the first set
    image_folder_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/test_images'

    # Output file path to save the histograms for the first set of images
    output_file_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/histograms_output.txt'

    # Create an instance of HistogramCalculatorSub
    hist_calculator = HistogramCalculatorSub()

    # Calculate histograms from the location data for the first set of images and save them to the output file
    histograms = hist_calculator.calculate_histograms_from_location(image_folder_path, labels_file_path, output_file_path)

    # Step 2 - Repeat the process with a different set of images and labels file
    # Path to the new labels file
    labels_data_file_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/labels.txt'

    # Path to the folder containing new test images
    image_dataset_file_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/subsequence_cam1'

    # Output file path to save the histograms for the new set of images
    new_output_file_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/new_histograms_output.txt'

    # Calculate histograms from the location data for the new set of images and save them to the new output file
    new_histograms = hist_calculator.calculate_histograms_from_location(image_dataset_file_path, labels_data_file_path, new_output_file_path)

    # Path to the histogram data files
    test_histogram_file_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/histograms_output.txt'
    dataset_histogram_file_path = '/Users/lixuanguo/Uni/winter2024/CSI4355/projet/part1/new_histograms_output.txt'

    # Create an instance of ComparisonHistogram
    comparison = ComparisonHistogram(test_histogram_file_path, dataset_histogram_file_path)

    # Write results to a text file
    comparison.write_results_to_file('result.txt')