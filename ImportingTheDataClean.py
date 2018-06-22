import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

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

# Other constants needed to calculate the force
mass_cyclist = 83
gravitational_constant = 9.81

# Calculations for gravitational forces
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
        self.file_name = filedialog.askopenfilename(initialdir="C:\\Users\Jelle\Documents",
                                                    title="Select file...",
                                                    filetypes=(("ASC Files", "*.asc"), ("All Files", "*.*")))
        self.opened_file = open(self.file_name, 'r')
        self.read_file = self.opened_file.read()

        os.remove('Intermediate_Text_File.txt')
        new_text_file = open('Intermediate_Text_File.txt', 'w')

        for line in self.read_file:
            new_text_file.write(line)

        new_text_file = open('Intermediate_Text_File.txt', 'r')
        self.lines = []

        for line in new_text_file:
            self.lines.append(line)

        for i in range(38):
            del self.lines[0]

        self.opened_file.close()
        new_text_file.close()

    def organizing(self):
        organized_as_single_columns = []

        for i in range(len(self.lines)):
            organized_as_single_columns.append(self.lines[i].split())

        self.organized_data = np.array([np.array(j) for j in organized_as_single_columns])

        values_to_convert = [[9, 1], [10, 2], [11, 3], [6, 4], [7, 5], [8, 6], [12, 7], [13, 8], [14, 9], [15, 10],
                             [5, 11], [4, 12], [24, 13], [25, 14], [26, 15], [21, 16], [22, 17], [23, 18], [27, 19],
                             [28, 20], [29, 21], [30, 22], [20, 23], [19, 24], [34, 25], [35, 26], [36, 27]]

        for i in range(len(values_to_convert)):
            self.organized_data[:, values_to_convert[i]] = self.organized_data[:, values_to_convert[i][::-1]]

        self.organized_stripped_data = self.organized_data[:, range(28)]

    def calculations(self):
        a_rear_tube = float(A_rear_tube)
        a_chai_tube = float(A_chai_tube)
        a_sitt_tube = float(A_sitt_tube)
        a_horz_tube = float(A_horz_tube)
        a_fron_tube = float(A_fron_tube)

        self.internal_forces = np.array([]).reshape(0, 5)

        for i in range(len(self.organized_stripped_data)):
            self.internal_forces = np.append(self.internal_forces, [[float(self.organized_stripped_data[i, 24])
                                                                     * a_rear_tube,
                                                                     float(self.organized_stripped_data[i, 23])
                                                                     * a_chai_tube,
                                                                     float(self.organized_stripped_data[i, 26])
                                                                     * a_sitt_tube,
                                                                     float(self.organized_stripped_data[i, 14])
                                                                     * a_horz_tube,
                                                                     float(self.organized_stripped_data[i, 20])
                                                                     * a_fron_tube]], axis=0)

    def counting(self):
        self.max_force = max(self.internal_forces)
        self.min_force = min(self.internal_forces)
        self.force_ranges = []
        self.outer_range = self.max_force - self.min_force
        print(self.outer_range)
        for i in range(round(self.outer_range/0.5)):
            self.outer_range.append(self.min_force + i*0.5)
        print(self.outer_range)

        for j in range(len(self.force_ranges)):
            for i in range(len(self.internal_forces)):
                print('lol')
        # self.internal_forces[j]

    def plotting(self):
        horizontal_axis_internal_forces = self.organized_stripped_data[:, 0]
        vertical_axis_internal_forces = [self.internal_forces[:, 0], self.internal_forces[:, 1],
                                         self.internal_forces[:, 2], self.internal_forces[:, 3],
                                         self.internal_forces[:, 4]]

        horizontal_axis_internal_forces_maxima = self.organized_stripped_data[:, 0]
        vertical_axis_internal_forces_maxima = [max(self.internal_forces[:, 0]), max(self.internal_forces[:, 1]),
                                         max(self.internal_forces[:, 2]), max(self.internal_forces[:, 3]),
                                         max(self.internal_forces[:, 4])]
        plot_title = ['Internal Force Rear-most Tube, [N]', 'Internal Force Tube Parallel To Chain, [N]',
                      'Internal Force Sitting Tube, [N]', 'Internal Force Horizontal Tube, [N]',
                      'Internal Force Front Angled Tube, [N]']
        plt.figure(1, figsize=(20, 13))
        for i in range(5):
            plt.subplot(5, 1, i + 1)
            plt.scatter(horizontal_axis_internal_forces, vertical_axis_internal_forces[i], s=1, marker=',')
            plt.grid(True)
            plt.title(plot_title[i])
            plt.xticks([])
        plt.tight_layout()
        #plt.show()
        #plt.close()

        plt.figure(2, figsize=(20, 13))
        for i in range(5):
            plt.subplot(5, 1, i + 1)
            plt.bar(horizontal_axis_internal_forces_maxima, vertical_axis_internal_forces_maxima[i])
            plt.grid(True)
            plt.title(plot_title[i])
            plt.xticks([])
        plt.tight_layout()
        #plt.show()
        #plt.close()

# Plot settings
np.set_printoptions(linewidth=400, edgeitems=18, suppress=True)

# Classes
data = Data()

# Functions
data.organizing()
data.calculations()
data.plotting()
data.counting()
