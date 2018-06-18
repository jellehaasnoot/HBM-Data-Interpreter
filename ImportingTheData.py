import os
import numpy as np
import matplotlib.pyplot as plt


class ConstantValues:
    globals()
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

    mass_cyclist = 83
    gravitational_constant = 9.81

    l_sitting_tube = 0.580
    l_rear_most_angled_tube = (np.sin(np.deg2rad(beta)) * l_sitting_tube)/np.sin(np.deg2rad(alpha))
    l_rear_bracket_COM = np.sin(np.deg2rad(phi)) * l_rear_most_angled_tube
    l_wheelbase = 0.991
    l_front_bracket_COM = l_wheelbase - l_rear_bracket_COM

    F_y4 = (mass_cyclist * gravitational_constant) / (1 + (l_front_bracket_COM / l_rear_bracket_COM))
    F_y1 = mass_cyclist * gravitational_constant - F_y4

    A_horz_tube = np.pi * ((34.9 / 2) ** 2 - ((34.9 - 2.6) / 2) ** 2)
    A_sitt_tube = np.pi * ((31.8 / 2) ** 2 - ((31.8 - 3.2) / 2) ** 2)
    A_fron_tube = np.pi * ((5 / 2) ** 2 - ((5 - 2.6) / 2) ** 2)
    A_rear_tube = 97.3
    A_chai_tube = 98.7


class OpeningAndOrganizingTheData:
    '''In the following class, the Data is extracted from the ASCII Text file resulting from the test. This will be done
        as follows: Open the file, read the file, write the file to a new file as an intermediate step, remove the lines
        which contain no data, organize the columns so that they are recognized as single columns ... '''

    @staticmethod
    def opening_the_file():
        file_name = 'DAQTest2_50Hz_+Channel_info.ASC'
        matlab_file_contents = open(file_name, 'r')

        return matlab_file_contents

    @staticmethod
    def reading_the_file():
        previously_opened = OpeningAndOrganizingTheData()
        opened_file = previously_opened.opening_the_file()
        read_data = opened_file.read()
        opened_file.close()

        return read_data

    @staticmethod
    def writing_to_an_intermediate_file():
        previously_read = OpeningAndOrganizingTheData()
        read_file = previously_read.reading_the_file()

        os.remove('Intermediate_Text_File.txt')
        new_text_file = open('Intermediate_Text_File.txt', 'w')

        for line in read_file:
            new_text_file.write(line)

        new_text_file.close()
        return new_text_file

    @staticmethod
    def removing_lines_that_are_not_needed():
        previously_opened = OpeningAndOrganizingTheData()
        opened_file = previously_opened.opening_the_file()

        lines = opened_file.readlines()
        opened_file.close()

        for i in range(38):
            del lines[0]
        return lines

    @staticmethod
    def organizing():
        previously_read = OpeningAndOrganizingTheData()
        read_file = previously_read.removing_lines_that_are_not_needed()

        organized_as_single_columns = []

        for i in range(len(read_file)):
            organized_as_single_columns.append(read_file[i].split())

        organized_as_array = np.array([np.array(j) for j in organized_as_single_columns])
        return organized_as_array


class NamingColumnsOfData:
    '''In this class the columns of the dataset will be named and assigned values from the processed data. This will
    be done by firstly, creating names for each column of the data file, then organizing the columns from the
    original file to match them to the right values, then deleting the unused columns.'''
    @staticmethod
    def creating_list_of_names():
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
        return names

    @staticmethod
    def ordering_order_columns():
        organized_class = OpeningAndOrganizingTheData()
        organized_data = organized_class.organizing()

        # Horizontal_tube_rosette_strain
        organized_data[:, [9, 1]] = organized_data[:, [1, 9]]
        organized_data[:, [10, 2]] = organized_data[:, [2, 10]]
        organized_data[:, [11, 3]] = organized_data[:, [3, 11]]

        # Sitting_tube_rosette_strain
        organized_data[:, [6, 4]] = organized_data[:, [4, 6]]
        organized_data[:, [7, 5]] = organized_data[:, [5, 7]]
        organized_data[:, [8, 6]] = organized_data[:, [6, 8]]

        # Front_angled_tube_rosette_strain
        organized_data[:, [12, 7]] = organized_data[:, [7, 12]]
        organized_data[:, [13, 8]] = organized_data[:, [8, 13]]
        organized_data[:, [14, 9]] = organized_data[:, [9, 14]]

        # Single strain gauges - strain
        organized_data[:, [15, 10]] = organized_data[:, [10, 15]]
        organized_data[:, [5, 11]] = organized_data[:, [11, 5]]
        organized_data[:, [4, 12]] = organized_data[:, [12, 4]]

        # Horizontal_tube_rosette_stress
        organized_data[:, [24, 13]] = organized_data[:, [13, 24]]
        organized_data[:, [25, 14]] = organized_data[:, [14, 25]]
        organized_data[:, [26, 15]] = organized_data[:, [15, 26]]

        # Sitting_tube_rosette_stress
        organized_data[:, [21, 16]] = organized_data[:, [16, 21]]
        organized_data[:, [22, 17]] = organized_data[:, [17, 22]]
        organized_data[:, [23, 18]] = organized_data[:, [18, 23]]

        # Front_angled_tube_rosette_stress
        organized_data[:, [27, 19]] = organized_data[:, [19, 27]]
        organized_data[:, [28, 20]] = organized_data[:, [20, 28]]
        organized_data[:, [29, 21]] = organized_data[:, [21, 29]]

        # Single strain gauges - stress
        organized_data[:, [30, 22]] = organized_data[:, [22, 30]]
        organized_data[:, [20, 23]] = organized_data[:, [23, 20]]
        organized_data[:, [19, 24]] = organized_data[:, [24, 19]]

        # Rosette_main_stresses
        organized_data[:, [34, 25]] = organized_data[:, [25, 34]]
        organized_data[:, [35, 26]] = organized_data[:, [26, 35]]
        organized_data[:, [36, 27]] = organized_data[:, [27, 36]]

        organized_stripped_data = organized_data[:, range(28)]

        return organized_stripped_data


class PerformingCalculations:
    '''In this class a number of small calculations are performed. Some cross-sectional values are calculated, the
    values from the original file are "floated" and the internal stresses are multiplied by their respective cross-
    section, so the internal force is calculated.'''
    @staticmethod
    def calculating_internal_forces_from_data():
        organized_class = NamingColumnsOfData()

        a_rear_tube = float(ConstantValues.A_rear_tube)
        a_chai_tube = float(ConstantValues.A_chai_tube)
        a_sitt_tube = float(ConstantValues.A_sitt_tube)
        a_horz_tube = float(ConstantValues.A_horz_tube)
        a_fron_tube = float(ConstantValues.A_fron_tube)

        organized_stripped_data = organized_class.ordering_order_columns()

        internal_forces = np.array([]).reshape(0, 5)

        for i in range(len(organized_stripped_data)):
            internal_forces = np.append(internal_forces, [[float(organized_stripped_data[i, 24]) * a_rear_tube, float(organized_stripped_data[i, 23]) * a_chai_tube, float(organized_stripped_data[i, 26]) * a_sitt_tube, float(organized_stripped_data[i, 14]) * a_horz_tube, float(organized_stripped_data[i, 20]) * a_fron_tube]], axis=0)

        return internal_forces

class VisualizingTheData:

    @staticmethod
    def plotting_the_forces():
        organized_class = NamingColumnsOfData()
        organized_stripped_data = organized_class.ordering_order_columns()

        calculated_class = PerformingCalculations()
        internal_forces_data = calculated_class.calculating_internal_forces_from_data()

        horizontal_axis_internal_forces = organized_stripped_data[:, 0]
        vertical_axis_internal_forces_1 = internal_forces_data[:, 0]
        vertical_axis_internal_forces_2 = internal_forces_data[:, 1]
        vertical_axis_internal_forces_3 = internal_forces_data[:, 2]
        vertical_axis_internal_forces_4 = internal_forces_data[:, 3]
        vertical_axis_internal_forces_5 = internal_forces_data[:, 4]

        plt.figure(1, figsize=(20, 13))

        plt.subplot(5, 1, 1)
        plt.scatter(horizontal_axis_internal_forces, vertical_axis_internal_forces_1, s=1, marker=',')
        plt.grid(True)
        plt.title('Internal Force Rear-most Tube, [N]')
        plt.xticks([])

        plt.subplot(5, 1, 2)
        plt.scatter(horizontal_axis_internal_forces, vertical_axis_internal_forces_2, s=1, marker=',')
        plt.grid(True)
        plt.title('Internal Force Tube Parallel To Chain, [N]')
        plt.xticks([])

        plt.subplot(5, 1, 3)
        plt.scatter(horizontal_axis_internal_forces, vertical_axis_internal_forces_3, s=1, marker=',')
        plt.grid(True)
        plt.title('Internal Force Sitting Tube, [N]')
        plt.xticks([])

        plt.subplot(5, 1, 4)
        plt.grid(True)
        plt.scatter(horizontal_axis_internal_forces, vertical_axis_internal_forces_4, s=1, marker=',')
        plt.title('Internal Force Horizontal Tube, [N]')
        plt.xticks([])

        plt.subplot(5, 1, 5)
        plt.scatter(horizontal_axis_internal_forces, vertical_axis_internal_forces_5, s=1, marker=',')
        plt.grid(True)
        plt.title('Internal Force Front Angled Tube, [N]')
        plt.xticks([])

        plt.tight_layout()
        plt.show()


class RunningImportingTheData:
    np.set_printoptions(linewidth=400, edgeitems=18, suppress=True)

    # Classes
    Opening = OpeningAndOrganizingTheData()
    Naming = NamingColumnsOfData()
    Constants = ConstantValues()
    Calculations = PerformingCalculations()
    Visualizing = VisualizingTheData()

    # Functions
    Opening.opening_the_file()
    Read = Opening.reading_the_file()
    Opening.writing_to_an_intermediate_file()
    Opening.removing_lines_that_are_not_needed()
    Organized = Naming.ordering_order_columns()
    Calculated = Calculations.calculating_internal_forces_from_data()
    Visualizing.plotting_the_forces()

    print(len(Organized))
    print(len(Organized[0]))
    print(len(Calculated))
    print(len(Calculated[0]))
    print(np.amax(Calculated))


    # print(Organized)
    # print(Calculated)
