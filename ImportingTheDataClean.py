import os
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os.path
import warnings
import sys

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
mass_cyclist = 82.5
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

        # File 1
        self.file_name_1 = filedialog.askopenfilename(
            initialdir="C:\\Users\Jelle\Documents\GitHub\HBM-Data-Interpreter",
            title="Select first file...",
            filetypes=(("ASC Files", "*.asc"), ("Text Files", "*.txt"),
                       ("All Files", "*.*")))
        self.opened_file_1 = open(self.file_name_1, 'r')
        self.read_file_1 = self.opened_file_1.readlines()

        self.lines_1 = []
        for line in self.read_file_1:
            self.lines_1.append(line)

        for i in range(38):
            del self.lines_1[0]
        self.opened_file_1.close()

        # File 2
        root = tk.Tk()
        root.withdraw()

        self.file_name_2 = filedialog.askopenfilename(
            initialdir="C:\\Users\Jelle\Documents\GitHub\HBM-Data-Interpreter",
            title="Select second file...",
            filetypes=(("ASC Files", "*.asc"), ("Text Files", "*.txt"),
                       ("All Files", "*.*")))
        self.opened_file_2 = open(self.file_name_2, 'r')
        self.read_file_2 = self.opened_file_2.readlines()

        self.lines_2 = []
        for line in self.read_file_2:
            self.lines_2.append(line)

        for i in range(38):
            del self.lines_2[0]

        self.opened_file_2.close()

    def user_input(self):
        self.no_of_graphs = input('How many strain gauges do you want to process? Type a number, max. is 5: ')
        if int(self.no_of_graphs) > 5 or int(self.no_of_graphs) <= 0:
            print('That is not an option. Please restart the program.')
            sys.exit()
        else:
            pass

        self.channels = input(
            '\nWhich channels do you want to display in the graphs? Type max. 5 numbers, all below or equal to 16, separated by spaces: ')
        self.channels = [x.strip() for x in self.channels.split()]
        if len(self.channels) != int(self.no_of_graphs):
            print('That is not a valid entry. Please restart the program.')
            sys.exit()
        else:
            pass

        for entry in range(len(self.channels)):
            if int(self.channels[entry]) <= 16:
                continue
            if int(self.channels[entry]) > 16 or int(self.channels[entry]) < 0:
                print('That is not an allowed entry. Please restart the program.')
                sys.exit()

        self.to_print = input('\nDo you want the graphs to be shown? Type [yes] or [no]: ')
        if self.to_print == 'yes' or self.to_print == 'Yes' or self.to_print == 'y' or self.to_print == 'Y':
            self.to_print_result = 1
        elif self.to_print == 'no' or self.to_print == 'No' or self.to_print == 'n' or self.to_print == 'N':
            self.to_print_result = 0
        else:
            print('That was not a valid input. Please restart the program.')
            sys.exit()

        if self.to_print_result == 1:
            self.integrated = input('\nDo you want the two graphs to be viewed as integrated? Type [yes] or [no]: ')
            if self.integrated == 'yes' or self.integrated == 'Yes' or self.integrated == 'y' or self.integrated == 'Y':
                self.integrated = 1
                self.no_of_subplots = 1
            elif self.integrated == 'no' or self.integrated == 'No' or self.integrated == 'n' or self.integrated == 'N':
                self.integrated = 2
                self.no_of_subplots = 2
            else:
                print('That was not a valid input. Please restart the program.')
                sys.exit()

        else:
            pass

        self.channel_names = input(
            '\nWhat do you want to call the channels, in the same order as you gave them above? Give max. five names, now separated by commas (multiple words possible): ')
        self.channel_names = [x.strip() for x in self.channel_names.split(',')]
        if len(self.channel_names) != int(self.no_of_graphs):
            print('That is not as many names as there are graphs to be viewed. Please restart the program.')
            sys.exit()
        else:
            pass

        self.amount_of_ranges = input(
            '\nIn how many parts should the data be divided? In other words, how many ranges should be visible? Type a number: ')
        if int(self.amount_of_ranges) <= 0:
            print('This is not a valid input. Please restart the program.')
            sys.exit()
        else:
            pass

        self.youngs_modulus = input('\nWhat is the Youngs Modulus of the material, in MPa? Enter only rounded values: ')
        if int(self.youngs_modulus) <= 0:
            print('This is not a valid number. Please restart the program.')
            sys.exit()
        else:
            pass

        self.youngs_modulus = float(self.youngs_modulus)

    def organizing(self):
        """
        This function is used to organize the input data which is given in the loaded text file.
        """
        # File 1
        organized_as_single_columns_1 = []
        for i in range(len(self.lines_1)):
            organized_as_single_columns_1.append(self.lines_1[i].split())

        self.organized_stripped_data_1 = [[float(float(j)) for j in i] for i in organized_as_single_columns_1]
        self.organized_stripped_data_1 = np.array(self.organized_stripped_data_1)

        # File 2
        organized_as_single_columns_2 = []
        for i in range(len(self.lines_2)):
            organized_as_single_columns_2.append(self.lines_2[i].split())

        self.organized_stripped_data_2 = [[float(float(j)) for j in i] for i in organized_as_single_columns_2]
        self.organized_stripped_data_2 = np.array(self.organized_stripped_data_2)

    def calculations(self):
        """
        This function calculates the stresses acting on each tube. This will be calculated with the known tube area and
        known stress.
        """
        # File 1
        self.internal_stresses_1 = [] #np.array([]).reshape(0, int(self.no_of_graphs))
        for i in range(int(self.no_of_graphs)):
            self.internal_stresses_1.append(float(self.youngs_modulus) * self.organized_stripped_data_1[:, int(self.channels[i])] / 1000000)

        # File 2
        self.internal_stresses_2 = [] #np.array([]).reshape(0, int(self.no_of_graphs))
        for i in range(int(self.no_of_graphs)):
            self.internal_stresses_2.append(float(self.youngs_modulus) * self.organized_stripped_data_2[:, int(self.channels[i])] / 1000000)

    def counting(self):
        """
        This function will be used to count the stress peaks acting on the bicycle. These peaks will determine if the
        bike will fatigue. These values will be shown in box plots and compared between the different situations. The
        bike frames will fatigue the same on indoor trainers as training outdoor if these graphs match. If not, further
        research is required.
        """
        # File 1
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
        self.range_factor_1 = self.outer_range_1 / int(self.amount_of_ranges)
        for i in range(int(round(self.outer_range_1 / self.range_factor_1, 1)) - 1):
            self.stress_ranges_1.append(min_stress_1 + self.range_factor_1 * i)



        # Defining the counter of datapoints. When a certain datapoint falls between two of the above defined ranges, it is counted as being in that range.
        self.sum_of_peaks_in_range_all_columns_1 = []
        for j in range(len(self.stress_ranges_1) - 1):
            sum_of_peaks_in_range_one_column_1 = []

            for i in range(len(self.internal_stresses_1)):
                counter = 0

                for k in range(len(self.internal_stresses_1[0])):
                    if self.stress_ranges_1[j] < self.internal_stresses_1[i][k] < self.stress_ranges_1[j + 1]:
                        counter += 1

                sum_of_peaks_in_range_one_column_1.append(counter)
            self.sum_of_peaks_in_range_all_columns_1.append(sum_of_peaks_in_range_one_column_1)

        self.sum_of_peaks_in_all_ranges_1 = []
        for i in range(int(self.no_of_graphs)):
            self.sum_of_peaks_in_all_ranges_1.append([])

        for i in range(len(self.sum_of_peaks_in_range_all_columns_1)):
            for j in range(len(self.sum_of_peaks_in_range_all_columns_1[i])):
                self.sum_of_peaks_in_all_ranges_1[j].append(self.sum_of_peaks_in_range_all_columns_1[i][j])

        # File 2
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
        self.range_factor_2 = (self.outer_range_1 / int(self.amount_of_ranges))

        for i in range(int(round(self.outer_range_2 / self.range_factor_2, 1)) - 1):
            self.stress_ranges_2.append(min_stress_2 + self.range_factor_2 * i)

        # Defining the counter of datapoints. When a certain datapoint falls between two of the above defined ranges, it is counted as being in that range.
        self.sum_of_peaks_in_range_all_columns_2 = []
        for j in range(len(self.stress_ranges_2) - 1):
            sum_of_peaks_in_range_one_column_2 = []

            for i in range(len(self.internal_stresses_2)):
                counter = 0

                for k in range(len(self.internal_stresses_2[0])):
                    if self.stress_ranges_2[j] < self.internal_stresses_2[i][k] < self.stress_ranges_2[j + 1]:
                        counter += 1

                sum_of_peaks_in_range_one_column_2.append(counter)
            self.sum_of_peaks_in_range_all_columns_2.append(sum_of_peaks_in_range_one_column_2)

        self.sum_of_peaks_in_all_ranges_2 = []
        for i in range(int(self.no_of_graphs)):
            self.sum_of_peaks_in_all_ranges_2.append([])

        for i in range(len(self.sum_of_peaks_in_range_all_columns_2)):
            for j in range(len(self.sum_of_peaks_in_range_all_columns_2[i])):
                self.sum_of_peaks_in_all_ranges_2[j].append(self.sum_of_peaks_in_range_all_columns_2[i][j])

    def plotting(self):
        """
        Plots both graphs:
            - The first graph will show the stress over time in the bicycle frame.
            - The second graph will show the box plot of the stress peaks.
        """
        # File 1
        del self.stress_ranges_1[-1]
        bar_horizontal_axis_1 = tuple(self.stress_ranges_1)
        bar_vertical_axis_1 = self.sum_of_peaks_in_all_ranges_1

        bar_horizontal_ticks_1 = []
        bar_horizontal_ticks_1_factor = int(round(len(self.stress_ranges_1) / 15, 1))
        for i in range(int(round((len(self.stress_ranges_1)) / bar_horizontal_ticks_1_factor, 1))):
            bar_horizontal_ticks_1.append(self.stress_ranges_1[i * bar_horizontal_ticks_1_factor])

        line_horizontal_ticks_1 = []
        line_horizontal_ticks_1_factor = int(round(len(self.organized_stripped_data_1) / 10))
        for i in range(10):
            line_horizontal_ticks_1.append(self.organized_stripped_data_1[i * line_horizontal_ticks_1_factor, 0])

        # File 2
        del self.stress_ranges_2[-1]
        bar_horizontal_axis_2 = tuple(self.stress_ranges_2)
        bar_vertical_axis_2 = self.sum_of_peaks_in_all_ranges_2

        bar_horizontal_ticks_2 = []
        bar_horizontal_ticks_2_factor = int(round(len(self.stress_ranges_2) / 15, 1))
        for i in range(int(round((len(self.stress_ranges_2)) / bar_horizontal_ticks_2_factor, 1))):
            bar_horizontal_ticks_2.append(self.stress_ranges_2[i * bar_horizontal_ticks_2_factor])

        line_horizontal_ticks_2 = []
        line_horizontal_ticks_2_factor = int(round(len(self.organized_stripped_data_2) / 10))
        for i in range(10):
            line_horizontal_ticks_2.append(self.organized_stripped_data_2[i * line_horizontal_ticks_2_factor, 0])

        plot_title = []
        for i in range(int(self.no_of_graphs)):
            plot_title.append(self.channel_names[i] + ' [MPa]')

        # Bar plot 1
        plt.figure(1, figsize=(18, 10))
        for j in range(int(self.no_of_graphs)):
            plt.subplot(int(self.no_of_graphs), self.integrated, j * self.no_of_subplots + 1)
            plt.bar(bar_horizontal_axis_1, bar_vertical_axis_1[j], 0.2 * round(60 / len(self.stress_ranges_1), 1), align='edge', color='k',
                    label=str(os.path.basename(self.file_name_1)))
            plt.grid(True)
            plt.title(plot_title[j])
            plt.xticks(bar_horizontal_ticks_1)
            plt.xlabel('Interne Spanningen [MPa]')
            plt.ylabel('Aantal instanties')
            plt.legend()
            plt.tight_layout()

            plt.subplot(int(self.no_of_graphs), self.integrated, j * self.no_of_subplots + self.integrated)
            plt.bar(bar_horizontal_axis_2, bar_vertical_axis_2[j], -0.2 * round(60 / len(self.stress_ranges_2), 1), align='edge', color='r',
                    label=str(os.path.basename(self.file_name_2)))
            plt.title(plot_title[j])
            plt.grid(True)
            plt.xticks(bar_horizontal_ticks_2)
            plt.xlabel('Interne Spanningen [MPa]')
            plt.ylabel('Aantal instanties')
            plt.legend()
            plt.tight_layout()

        # Normal plot
        plt.figure(2, figsize=(18, 10))
        for i in range(int(self.no_of_graphs)):
            plt.subplot(int(self.no_of_graphs), self.integrated, i * self.no_of_subplots + 1)
            plt.plot(self.organized_stripped_data_1.T[0], self.internal_stresses_1[i], linewidth=0.6,
                     color='k', label=str(os.path.basename(self.file_name_1)))
            plt.minorticks_on()
            plt.grid(b=True, which='major', linestyle='-')
            plt.grid(b=True, which='minor', linestyle='--')
            plt.title(plot_title[i])
            if self.integrated == 1 and len(line_horizontal_ticks_2) >= len(line_horizontal_ticks_1):
                plt.xticks(line_horizontal_ticks_2, color='r')
            elif self.integrated == 1 and len(line_horizontal_ticks_2) <= len(line_horizontal_ticks_1):
                plt.xticks(line_horizontal_ticks_1)
            elif self.integrated == 2:
                plt.xticks(line_horizontal_ticks_1)
            plt.xlabel('Tijd [s]')
            plt.ylabel('Interne Spanning [MPa]')
            plt.legend()
            plt.tight_layout()

            plt.subplot(int(self.no_of_graphs), self.integrated, i * self.no_of_subplots + self.integrated)
            plt.plot(self.organized_stripped_data_2.T[0], self.internal_stresses_2[i], linewidth=0.6,
                     color='r', label=str(os.path.basename(self.file_name_2)))
            plt.minorticks_on()
            plt.grid(b=True, which='major', linestyle='-')
            plt.grid(b=True, which='minor', linestyle='--')
            plt.title(plot_title[i])
            if self.integrated == 1 and len(line_horizontal_ticks_2) >= len(line_horizontal_ticks_1):
                plt.xticks(line_horizontal_ticks_2, color='r')
            elif self.integrated == 1 and len(line_horizontal_ticks_2) <= len(line_horizontal_ticks_1):
                plt.xticks(line_horizontal_ticks_1)
            elif self.integrated == 2:
                plt.xticks(line_horizontal_ticks_2, color='r')
            plt.xlabel('Tijd [s]')
            plt.ylabel('Interne Spanning [MPa]')
            plt.legend()
            plt.tight_layout()

        plt.show()
        plt.close()

    def cls(self):
        clear = "\n" * 5
        print(clear)

    def plotting_statistics(self):
        """
        In this function, some of the basic statistics of each file will be displayed. Among these are, for example, what range has the highest amount of datapoints in it, or how long is the file, etc.
        """

        #Amount of tab difference after names
        name_length_1 = len(os.path.basename(self.file_name_1))
        name_length_2 = len(os.path.basename(self.file_name_2))

        name_length_difference = (name_length_1 - name_length_2)
        name_tabs_difference = int(round(abs(name_length_difference) / 4, 1))

        if name_length_difference < 0:
            amount_of_tabs_1 = "\t" * (name_tabs_difference + 5)
            amount_of_tabs_2 = "\t" * 5
        elif name_length_difference > 0:
            amount_of_tabs_1 = "\t" * 5
            amount_of_tabs_2 = "\t" * (name_tabs_difference + 5)
        else:
            amount_of_tabs_1 = "\t" * 5
            amount_of_tabs_2 = "\t" * 5

        # Collecting statistics for the first file:
        print("File 1")
        max_range_columns_1 = []
        max_range_columns_indices_1 = []
        for i in range(len(self.sum_of_peaks_in_all_ranges_1)):
            max_range_columns_1.append(max(self.sum_of_peaks_in_all_ranges_1[i]))
            max_range_columns_indices_1.append(self.sum_of_peaks_in_all_ranges_1[i].index(max_range_columns_1[i]))

        max_range_1 = max(max_range_columns_1)
        max_range_1_index = max_range_columns_1.index(max_range_1)
        print("The maximum occuring stress in " + str(os.path.basename(self.file_name_1)) + " is in the range from: " + amount_of_tabs_1 + "%.2f" % self.stress_ranges_1[max_range_1_index] + " to " + "%.2f" % self.stress_ranges_1[max_range_1_index + 1] + " MPa.")
        print("The times this stress occurs in " + str(os.path.basename(self.file_name_1)) + " is: " + amount_of_tabs_1 + "\t\t\t\t\t" + "%.0f" % max_range_1 + " times.")
        print("The strain gauge channel in which the highest stress occured in " + str(os.path.basename(self.file_name_1)) + " is: \t" + amount_of_tabs_1 + "%.0f" % (max_range_1_index + 1) + ".")

        # Collecting statistics for the second file:
        print("\nFile 2")
        max_range_columns_2 = []
        max_range_columns_indices_2 = []
        for i in range(len(self.sum_of_peaks_in_all_ranges_2)):
            max_range_columns_2.append(max(self.sum_of_peaks_in_all_ranges_2[i]))
            max_range_columns_indices_2.append(self.sum_of_peaks_in_all_ranges_2[i].index(max_range_columns_2[i]))

        max_range_2 = max(max_range_columns_2)
        max_range_2_index = max_range_columns_2.index(max_range_2)
        print("The maximum occuring stress in " + str(os.path.basename(self.file_name_2)) + " is in the range from: " + amount_of_tabs_2 + "%.2f" % self.stress_ranges_2[max_range_2_index] + " to " + "%.2f" % self.stress_ranges_2[max_range_2_index + 1] + " MPa.")
        print("The times this stress occurs in " + str(os.path.basename(self.file_name_2)) + " is: " + amount_of_tabs_2 + "\t\t\t\t" + "%.0f" % max_range_2 + " times.")
        print("The strain gauge channel in which the highest stress occured in " + str(os.path.basename(self.file_name_2)) + " is: " + amount_of_tabs_2 + "%.0f" % (max_range_2_index + 1) + ".")

# Plot settings
np.set_printoptions(linewidth=400, edgeitems=18, suppress=True)

# Classes
data = Data()

# Functions
warnings.filterwarnings("ignore")
data.user_input()
data.organizing()
data.calculations()
data.counting()
data.cls()
data.plotting_statistics()
if data.to_print_result == 1:
    data.plotting()
else:
    pass
