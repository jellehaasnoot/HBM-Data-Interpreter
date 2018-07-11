import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os.path

# Constants dimensions
alpha = 68.7
gamma = 45.5
beta = 180 - gamma - alpha
delta = 77
epsilon = 73
tau = 45.7
zeta = 73
eta = 180 - delta - tau
ksi = epsilon - beta
theta = 90 - beta - ksi
phi = 90 - alpha + ksi
l_sitting_tube = 0.580
l_rear_most_angled_tube = (np.sin(np.deg2rad(beta)) * l_sitting_tube) / np.sin(np.deg2rad(alpha))
l_rear_bracket_COM = np.sin(np.deg2rad(phi)) * l_rear_most_angled_tube
l_wheelbase = 0.991
l_front_bracket_COM = l_wheelbase - l_rear_bracket_COM

# Constants areas bike tubes
A_horz_tube = np.pi * ((34.9 / 2) ** 2 - ((34.9 - 2.6) / 2) ** 2)
A_sitt_tube = np.pi * ((31.8 / 2) ** 2 - ((31.8 - 3.2) / 2) ** 2)
A_fron_tube = np.pi * ((5 / 2) ** 2 - ((5 - 2.6) / 2) ** 2)
A_rear_tube = 97.3
A_chai_tube = 98.7

# Other constants needed to calculate the stress
mass_cyclist = 83
gravitational_constant = 9.81

# Calculations for gravitational stresses
F_y4 = (mass_cyclist * gravitational_constant) / (1 + (l_front_bracket_COM / l_rear_bracket_COM))
F_y1 = mass_cyclist * gravitational_constant - F_y4

# Names columns
list_of_column_names_strain = ['Horizontal_tube_rosette_1_strain', 'Horizontal_tube_rosette_2_strain',
                               'Horizontal_tube_rosette_3_strain', 'Sitting_tube_rosette_1_strain',
                               'Sitting_tube_rosette_2_strain', 'Sitting_tube_rosette_3_strain',
                               'Front_angled_tube_1_strain', 'Front_angled_tube_2_strain',
                               'Front_angled_tube_3_strain', 'Drive_train_gauge_strain',
                               'Chain_tube_gauge_strain', 'Rear_most_angled_tube_strain']
list_of_column_names_stress = ['Horizontal_tube_rosette_1_stress', 'Horizontal_tube_rosette_2_stress',
                               'Horizontal_tube_rosette_3_stress', 'Sitting_tube_rosette_1_stress',
                               'Sitting_tube_rosette_2_stress', 'Sitting_tube_rosette_3_stress',
                               'Front_angled_tube_1_stress', 'Front_angled_tube_2_stress',
                               'Front_angled_tube_3_stress', 'Drive_train_gauge_stress',
                               'Chain_tube_gauge_stress', 'Rear_most_angled_tube_stress',
                               'Horizontal_tube_nominal_main_stress', 'Sitting_tube_nominal_main_stress',
                               'Front_angled_tube_nominal_main_stress']
names = [list_of_column_names_strain, list_of_column_names_stress]


class Data:
    """
    This class converts the raw data into usable data, there will also be some operations to make this happen in this
    class. The file will be read and opened in the init method.
    """

    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        self.file_name_1 = filedialog.askopenfilename(initialdir="C:\\Users\Jelle\Documents",
                                                      title="Select first file...",
                                                      filetypes=(("Text Files", "*.txt"), ("ASC Files", "*.asc"),
                                                                 ("All Files", "*.*")))
        self.opened_file_1 = open(self.file_name_1, 'r')
        self.read_file_1 = self.opened_file_1.read()

        path_directory = str(os.path.dirname(self.file_name_1))
        path_file_1 = os.path.join(path_directory, "Intermediate_Text_File_1.txt")
        if os.path.exists(path_file_1):
            os.remove('Intermediate_Text_File_1.txt')
        else:
            pass
        new_text_file_1 = open('Intermediate_Text_File_1.txt', 'w')

        for line in self.read_file_1:
            new_text_file_1.write(line)

        new_text_file_1 = open('Intermediate_Text_File_1.txt', 'r')
        self.lines_1 = []

        for line in new_text_file_1:
            self.lines_1.append(line)

        for i in range(38):
            del self.lines_1[0]

        self.opened_file_1.close()
        new_text_file_1.close()

        self.file_name_2 = filedialog.askopenfilename(initialdir="C:\\Users\Jelle\Documents",
                                                      title="Select second file...",
                                                      filetypes=(("Text Files", "*.txt"), ("ASC Files", "*.asc"),
                                                                 ("All Files", "*.*")))
        self.opened_file_2 = open(self.file_name_2, 'r')
        self.read_file_2 = self.opened_file_2.read()

        path_file_2 = os.path.join(path_directory, "Intermediate_Text_File_2.txt")
        if os.path.isfile(path_file_2):
            os.remove('Intermediate_Text_File_2.txt')
        else:
            pass
        new_text_file_2 = open('Intermediate_Text_File_2.txt', 'w')

        for line in self.read_file_1:
            new_text_file_2.write(line)

        new_text_file_2 = open('Intermediate_Text_File_2.txt', 'r')
        self.lines_2 = []

        for line in new_text_file_2:
            self.lines_2.append(line)

        for i in range(38):
            del self.lines_2[0]

        self.opened_file_2.close()
        new_text_file_2.close()

    def organizing(self):
        """
        This function is used to organize the input data which is given in the loaded text file.
        """
        organized_as_signle_columns_1 = []

        for i in range(len(self.lines_1)):
            organized_as_signle_columns_1.append(self.lines_1[i].split())

        self.organized_data_1 = np.array([np.array(j) for j in organized_as_signle_columns_1])

        values_to_convert_1 = [[9, 1], [10, 2], [11, 3], [6, 4], [7, 5], [8, 6], [12, 7], [13, 8], [14, 9], [15, 10],
                               [5, 11], [4, 12], [24, 13], [25, 14], [26, 15], [21, 16], [22, 17], [23, 18], [27, 19],
                               [28, 20], [29, 21], [30, 22], [20, 23], [19, 24], [34, 25], [35, 26], [36, 27]]

        for i in range(len(values_to_convert_1)):
            self.organized_data_1[:, values_to_convert_1[i]] = self.organized_data_1[:, values_to_convert_1[i][::-1]]

        self.organized_stripped_data_1 = self.organized_data_1[:, range(28)]

        organized_as_signle_columns_2 = []

        for i in range(len(self.lines_2)):
            organized_as_signle_columns_2.append(self.lines_2[i].split())

        self.organized_data_2 = np.array([np.array(j) for j in organized_as_signle_columns_2])

        values_to_convert_2 = [[9, 1], [10, 2], [11, 3], [6, 4], [7, 5], [8, 6], [12, 7], [13, 8], [14, 9], [15, 10],
                               [5, 11], [4, 12], [24, 13], [25, 14], [26, 15], [21, 16], [22, 17], [23, 18], [27, 19],
                               [28, 20], [29, 21], [30, 22], [20, 23], [19, 24], [34, 25], [35, 26], [36, 27]]

        for i in range(len(values_to_convert_2)):
            self.organized_data_2[:, values_to_convert_2[i]] = self.organized_data_2[:, values_to_convert_2[i][::-1]]

        self.organized_stripped_data_2 = self.organized_data_2[:, range(28)]

    def calculations(self):
        """
        This function calculates the stresses acting on each tube. This will be calculated with the known tube area and
        known stress.
        """
        # a_rear_tube = float(A_rear_tube)
        # a_chai_tube = float(A_chai_tube)
        # a_sitt_tube = float(A_sitt_tube)
        # a_horz_tube = float(A_horz_tube)
        # a_fron_tube = float(A_fron_tube)

        self.internal_stresses_1 = np.array([]).reshape(0, 5)

        for i in range(len(self.organized_stripped_data_1)):
            self.internal_stresses_1 = np.append(self.internal_stresses_1,
                                                 [[float(self.organized_stripped_data_1[i, 24]),
                                                   float(self.organized_stripped_data_1[i, 23]),
                                                   float(self.organized_stripped_data_1[i, 26]),
                                                   float(self.organized_stripped_data_1[i, 14]),
                                                   float(self.organized_stripped_data_1[i, 20])]],
                                                 axis=0)

        self.internal_stresses_2 = np.array([]).reshape(0, 5)

        for i in range(len(self.organized_stripped_data_2)):
            self.internal_stresses_2 = np.append(self.internal_stresses_2,
                                                 [[float(self.organized_stripped_data_2[i, 24]),
                                                   float(self.organized_stripped_data_2[i, 23]),
                                                   float(self.organized_stripped_data_2[i, 26]),
                                                   float(self.organized_stripped_data_2[i, 14]),
                                                   float(self.organized_stripped_data_2[i, 20])]],
                                                 axis=0)

    def counting(self):
        """
        This function will be used to count the stress peaks acting on the bicycle. These peaks will determine if the
        bike will fatigue. These values will be shown in box plots and compared between the different situations. The
        bike frames will fatigue the same on indoor trainers as training outdoor if these graphs match. If not, further
        research is required.
        """
        # Defining the ranges in which the different forces will be categorized.
        max_stress_columns_1 = []
        min_stress_columns_1 = []
        for i in range(len(self.internal_stresses_1)):
            max_stress_columns_1.append(max(self.internal_stresses_1[i]))
            min_stress_columns_1.append(min(self.internal_stresses_1[i]))

        max_stress_1 = max(max_stress_columns_1)
        min_stress_1 = min(min_stress_columns_1)

        self.stress_ranges_1 = []
        self.outer_range_1 = max_stress_1 - min_stress_1
        for i in range(int(round(self.outer_range_1, 1))):
            self.stress_ranges_1.append(min_stress_1 + i)

        # Defining the counter of datapoints. When a certain datapoint falls between two of the above defined ranges, it is counted as being in that range.
        self.sum_of_peaks_in_range_all_columns_1 = []
        for j in range(len(self.stress_ranges_1) - 1):
            sum_of_peaks_in_range_one_column_1 = []

            for i in range(len(self.internal_stresses_1[1])):
                counter = 0

                for k in range(len(self.internal_stresses_1)):
                    if self.stress_ranges_1[j] < self.internal_stresses_1[k, i] < self.stress_ranges_1[j + 1]:
                        counter += 1

                sum_of_peaks_in_range_one_column_1.append(counter)
            self.sum_of_peaks_in_range_all_columns_1.append(sum_of_peaks_in_range_one_column_1)

        self.sum_of_peaks_in_all_ranges_1 = [[], [], [], [], []]
        for i in range(len(self.sum_of_peaks_in_range_all_columns_1)):
            for j in range(len(self.sum_of_peaks_in_range_all_columns_1[i])):
                self.sum_of_peaks_in_all_ranges_1[j].append(self.sum_of_peaks_in_range_all_columns_1[i][j])

        # Defining the ranges in which the different forces will be categorized.
        max_stress_columns_2 = []
        min_stress_columns_2 = []
        for i in range(len(self.internal_stresses_2)):
            max_stress_columns_2.append(max(self.internal_stresses_2[i]))
            min_stress_columns_2.append(min(self.internal_stresses_2[i]))

        max_stress_2 = max(max_stress_columns_2)
        min_stress_2 = min(min_stress_columns_2)

        self.stress_ranges_2 = []
        self.outer_range_2 = max_stress_2 - min_stress_2
        for i in range(int(round(self.outer_range_2, 1))):
            self.stress_ranges_2.append(min_stress_2 + i)

        # Defining the counter of datapoints. When a certain datapoint falls between two of the above defined ranges, it is counted as being in that range.
        self.sum_of_peaks_in_range_all_columns_2 = []
        for j in range(len(self.stress_ranges_2) - 1):
            sum_of_peaks_in_range_one_column_2 = []

            for i in range(len(self.internal_stresses_2[1])):
                counter = 0

                for k in range(len(self.internal_stresses_2)):
                    if self.stress_ranges_2[j] < self.internal_stresses_2[k, i] < self.stress_ranges_2[j + 1]:
                        counter += 1

                sum_of_peaks_in_range_one_column_2.append(counter)
            self.sum_of_peaks_in_range_all_columns_2.append(sum_of_peaks_in_range_one_column_2)

        self.sum_of_peaks_in_all_ranges_2 = [[], [], [], [], []]
        for i in range(len(self.sum_of_peaks_in_range_all_columns_2)):
            for j in range(len(self.sum_of_peaks_in_range_all_columns_2[i])):
                self.sum_of_peaks_in_all_ranges_2[j].append(self.sum_of_peaks_in_range_all_columns_2[i][j])

    def plotting(self):
        """
        Plots both graphs:
            - The first graph will show the stress over time in the bicycle frame.
            - The second graph will show the box plot of the stress peaks.
        """
        horizontal_axis_internal_stresses_1 = self.organized_stripped_data_1[:, 0]
        vertical_axis_internal_stresses_1 = [self.internal_stresses_1[:, 0], self.internal_stresses_1[:, 1],
                                             self.internal_stresses_1[:, 2], self.internal_stresses_1[:, 3],
                                             self.internal_stresses_1[:, 4]]

        del self.stress_ranges_1[-1]
        bar_horizontal_axis_1 = tuple(self.stress_ranges_1)
        bar_vertical_axis_1 = self.sum_of_peaks_in_all_ranges_1

        bar_horizontal_ticks_1 = []
        for i in range(int(round(self.outer_range_1 / 2, 1)) - 1):
            bar_horizontal_ticks_1.append(self.stress_ranges_1[i * 2])

        horizontal_axis_internal_stresses_2 = self.organized_stripped_data_2[:, 0]
        vertical_axis_internal_stresses_2 = [self.internal_stresses_2[:, 0], self.internal_stresses_2[:, 1],
                                             self.internal_stresses_2[:, 2], self.internal_stresses_2[:, 3],
                                             self.internal_stresses_2[:, 4]]

        del self.stress_ranges_2[-1]
        bar_horizontal_axis_2 = tuple(self.stress_ranges_2)
        bar_vertical_axis_2 = self.sum_of_peaks_in_all_ranges_2

        bar_horizontal_ticks_2 = []
        for i in range(int(round(self.outer_range_2 / 2, 1)) - 1):
            bar_horizontal_ticks_2.append(self.stress_ranges_2[i * 2])

        plot_title = ['Internal stress Rear-most Tube, [MPa]', 'Internal stress Tube Parallel To Chain, [MPa]',
                      'Internal stress Sitting Tube, [MPa]', 'Internal stress Horizontal Tube, [MPa]',
                      'Internal stress Front Angled Tube, [MPa]']

        # Bar plot 1
        plt.figure(1, figsize=(20, 13))
        for j in range(5):
            plt.subplot(5, 1, j + 1)
            plt.bar(bar_horizontal_axis_1, bar_vertical_axis_1[j], 0.8, align='edge')
            plt.grid(True)
            plt.title(plot_title[j])
            plt.xticks(bar_horizontal_ticks_1)
            plt.xlabel('Interne Spanningen [MPa]')
            plt.tight_layout()

        # Scatter plot
        plt.figure(2, figsize=(20, 13))
        for i in range(5):
            plt.subplot(5, 1, i + 1)
            plt.scatter(horizontal_axis_internal_stresses_1, vertical_axis_internal_stresses_1[i], s=1, marker=',')
            plt.grid(True)
            plt.title(plot_title[i])
            plt.xticks([])
            plt.xlabel('Tijd [s]')
            plt.tight_layout()
        plt.show()


# Plot settings
np.set_printoptions(linewidth=400, edgeitems=18, suppress=True)

# Classes
data = Data()

# Functions
data.organizing()
data.calculations()
data.counting()
data.plotting()
