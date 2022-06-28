"""Code for plotting input and output noise of a module's response curve.
Uses the standard data fromat from ITSDAQ and assumes that data for each test is
stored seprately in a folder with the run number as its name. Folders are located 
inside of folders corresponding to their sensor type. 

example path: R4_Data/1351/

The program takes as argument module type and a list of run numbers to compare."""

import argparse
import glob as glob
import re 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

gain_col = 2
innse_col = 4
e_per_fc = 6242
expected_noise = {'R1':[[500, 510],[580, 600]],
                  'R2':[580, 640],
                  'R4':[790,810],
                  'R5':[660, 920]}

def get_module_data(test_number, sensor_type, data):
    """Extracts the channel number, module input noise (innse) and gain from the response curve data
    for a particular test number. Currently just works for R5 and R4"""


    # Get the data files
    path = sensor_type + '_Data/' + str(test_number) + '/*'
    print(path)
    files = glob.glob(path)
    print(files)
    r = re.compile('.*ABCStar_R\dH\d_Hybrid\d_RC_\d{4}_\d+.txt') #Hybrid Version
    #r = re.compile('.*ABCStar_R\dH\d_Panel_RC_\d+_\d+.txt') #Pannel Version
    valid_files = list(filter(r.match, files))
    print(valid_files)
    
    # Open the data files and load into appropriate lists
    hybrid_number = 0
    for file in valid_files:
        with open(file, 'r') as f:
            lines = f.readlines()

        # Initialize vaiables for organizing plots
        segment_number = 0
        suffix = str(hybrid_number) + '_' + str(segment_number)
        channel = data.get('channel_' + suffix, [])
        input_noise = data.get('noise_in_' + suffix, [])
        output_noise = data.get('noise_out_' + suffix, [])
        segment_channel = []
        segment_input_noise = []
        segment_output_noise = []
        if sensor_type == 'R2':
            split_point = len(lines) - 2 # No need to split
        else :
            split_point = (len(lines) - 1)/2 - 1 # Split evenly
        i = 0

        # Extract data and write to dictionary
        for line in lines[1:]:
            line_data = line.split('\t')
            segment_channel.append(i)
            segment_input_noise.append(float(line_data[innse_col]))
            segment_output_noise.append(float(line_data[gain_col]) * float(line_data[innse_col]) / e_per_fc)
            i += 1
            # Reset variables for next segment
            if i > split_point:
                channel.append(segment_channel)
                input_noise.append(segment_input_noise)
                output_noise.append(segment_output_noise)
                data['channel_' + suffix] = channel
                data['noise_in_' + suffix] = input_noise
                data['noise_out_' + suffix] = output_noise

                segment_number += 1
                suffix = str(hybrid_number) + '_' + str(segment_number)
                channel = data.get('channel_' + suffix, [])
                input_noise = data.get('noise_in_' + suffix, [])
                output_noise = data.get('noise_out_' + suffix, [])
                segment_channel = []
                segment_input_noise = []
                segment_output_noise = []
                i = 0
        hybrid_number += 1
    return data


def plot_data(data, sensor_type, labels):
    """Plot the data in a series of subplots"""
    print(data.keys())
    if sensor_type == 'R2':
        fig1, axes1 = plt.subplots(2)
        fig2, axes2 = plt.subplots(2)
        for i in range(0,len(data['channel_0_0'])):
            # Input Noise Plot
            axes1[0].scatter(data['channel_1_0'][i],data['noise_in_1_0'][i],s=10, label=labels[i])
            axes1[1].scatter(data['channel_0_0'][i],data['noise_in_0_0'][i],s=10, label=labels[i])
            # Output Noise Plot
            axes2[0].scatter(data['channel_1_0'][i],data['noise_out_1_0'][i],s=10, label=labels[i])
            axes2[1].scatter(data['channel_0_0'][i],data['noise_out_0_0'][i],s=10, label=labels[i])

        axes1[0].hlines(y=expected_noise[sensor_type][1], xmin=0, xmax=len(data['channel_1_0'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')
        axes1[1].hlines(y=expected_noise[sensor_type][0], xmin=0, xmax=len(data['channel_0_0'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')

        fig1.suptitle('Input Noise for ' + sensor_type + ' Module')
        fig1.subplots_adjust(hspace=0.5)
        axes1[0].set_title('Hybrid 1, Stream 1')
        axes1[1].set_title('Hybrid 0, Stream 1')

        fig2.suptitle('Output Noise for ' + sensor_type + ' Module')
        fig2.subplots_adjust(hspace=0.5)
        axes2[0].set_title('Hybrid 1, Stream 1')
        axes2[1].set_title('Hybrid 0, Stream 1')

    elif sensor_type == 'R1':
        fig1, axes1 = plt.subplots(4)
        fig2, axes2 = plt.subplots(4)
        for i in range(0,len(data['channel_0_0'])):
            print(i)
            # Input Noise Plot
            axes1[0].scatter(data['channel_1_0'][i],data['noise_in_1_0'][i],s=10, label=labels[i]) #TODO: Fix the naming
            axes1[1].scatter(data['channel_1_1'][i],data['noise_in_1_1'][i],s=10, label=labels[i])
            axes1[2].scatter(data['channel_0_0'][i],data['noise_in_0_0'][i],s=10, label=labels[i])
            axes1[3].scatter(data['channel_0_1'][i],data['noise_in_0_1'][i],s=10, label=labels[i])
            # Output Noise Plot
            axes2[0].scatter(data['channel_1_0'][i],data['noise_out_1_0'][i],s=10, label=labels[i])
            axes2[2].scatter(data['channel_0_0'][i],data['noise_out_0_0'][i],s=10, label=labels[i])
            axes2[1].scatter(data['channel_1_1'][i],data['noise_out_1_1'][i],s=10, label=labels[i])
            axes2[3].scatter(data['channel_0_1'][i],data['noise_out_0_1'][i],s=10, label=labels[i])

        #Plot the expected noise line
        axes1[0].hlines(y=expected_noise[sensor_type][1][1], xmin=0, xmax=len(data['channel_1_0'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')
        axes1[2].hlines(y=expected_noise[sensor_type][0][1], xmin=0, xmax=len(data['channel_0_0'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')
        axes1[1].hlines(y=expected_noise[sensor_type][1][0], xmin=0, xmax=len(data['channel_1_1'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')
        axes1[3].hlines(y=expected_noise[sensor_type][0][1], xmin=0, xmax=len(data['channel_0_1'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')

        fig1.suptitle('Input Noise for ' + sensor_type + ' Module')
        fig1.subplots_adjust(hspace=1)
        axes1[0].set_title('Hybrid 1, Stream 1')
        axes1[1].set_title('Hybrid 1, Stream 0')
        axes1[2].set_title('Hybrid 0, Stream 1')
        axes1[3].set_title('Hybrid 0, Stream 0')

        fig2.suptitle('Output Noise for ' + sensor_type + ' Module')
        fig2.subplots_adjust(hspace=1)
        axes2[0].set_title('Hybrid 1, Stream 1')
        axes2[1].set_title('Hybrid 1, Stream 0')
        axes2[2].set_title('Hybrid 0, Stream 1')
        axes2[3].set_title('Hybrid 0, Stream 0')
    else:
        fig1, axes1 = plt.subplots(2,2)
        fig2, axes2 = plt.subplots(2,2)
        for i in range(0,len(data['channel_0_0'])):
            print(i)
            # Input Noise Plot
            axes1[0,0].scatter(data['channel_1_0'][i],data['noise_in_1_0'][i],s=10, label=labels[i]) #TODO: Fix the naming
            axes1[0,1].scatter(data['channel_0_0'][i],data['noise_in_0_0'][i],s=10, label=labels[i])
            axes1[1,0].scatter(data['channel_1_1'][i],data['noise_in_1_1'][i],s=10, label=labels[i])
            axes1[1,1].scatter(data['channel_0_1'][i],data['noise_in_0_1'][i],s=10, label=labels[i])
            # Output Noise Plot
            axes2[0,0].scatter(data['channel_1_0'][i],data['noise_out_1_0'][i],s=10, label=labels[i])
            axes2[0,1].scatter(data['channel_0_0'][i],data['noise_out_0_0'][i],s=10, label=labels[i])
            axes2[1,0].scatter(data['channel_1_1'][i],data['noise_out_1_1'][i],s=10, label=labels[i])
            axes2[1,1].scatter(data['channel_0_1'][i],data['noise_out_0_1'][i],s=10, label=labels[i])

        axes1[0,0].hlines(y=expected_noise[sensor_type][1], xmin=0, xmax=len(data['channel_1_0'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')
        axes1[0,1].hlines(y=expected_noise[sensor_type][1], xmin=0, xmax=len(data['channel_0_0'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')
        axes1[1,0].hlines(y=expected_noise[sensor_type][0], xmin=0, xmax=len(data['channel_1_1'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')
        axes1[1,1].hlines(y=expected_noise[sensor_type][0], xmin=0, xmax=len(data['channel_0_1'][0]), linewidth=2, label='Expected Noise', linestyle='dashed', color='g')

        fig1.suptitle('Input Noise for ' + sensor_type + ' Module')
        fig1.subplots_adjust(hspace=0.5)
        axes1[0,0].set_title('Hybrid 1, Stream 1')
        axes1[0,1].set_title('Hybrid 0, Stream 1')
        axes1[1,0].set_title('Hybrid 1, Stream 0')
        axes1[1,1].set_title('Hybrid 0, Stream 0')

        fig2.suptitle('Output Noise for ' + sensor_type + ' Module')
        fig2.subplots_adjust(hspace=0.5)
        axes2[0,0].set_title('Hybrid 1, Stream 1')
        axes2[0,1].set_title('Hybrid 0, Stream 1')
        axes2[1,0].set_title('Hybrid 1, Stream 0')
        axes2[1,1].set_title('Hybrid 0, Stream 0')

    for ax in axes1.flat:
        ax.set(xlabel='channel', ylabel='innse (ENC)')
        ax.legend(loc='lower right')
        ax.set(ylim=(400,4000))
        ax.xaxis.set_major_locator(MultipleLocator(128))
        #ax.yaxis.set_major_locator(MultipleLocator(200))
        #ax.yaxis.set_minor_locator(MultipleLocator(50))
        ax.grid(linestyle='dotted')

    for ax in axes2.flat:
        ax.set(xlabel='channel', ylabel='outnse (mV)')
        ax.legend(loc='lower right')
        ax.set(ylim=(0,30))
        ax.xaxis.set_major_locator(MultipleLocator(128))
        ax.yaxis.set_major_locator(MultipleLocator(10))
        ax.yaxis.set_minor_locator(MultipleLocator(2.5))
        ax.grid(linestyle='dotted')
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plots the input noise in ENC and output noise in mV for a list of modules")
    parser.add_argument("--run_numbers", nargs='+', help="The run numbers to be plotted")
    parser.add_argument("--sensor_type", help="Sensor type - ex. R4 ")
    parser.add_argument("--labels", nargs='+', help="Legend labels for run numbers as strings. \
                        If spaces are included, need to be surrounded by double or single quotes")

    args = parser.parse_args()

    data = {}
    for run in args.run_numbers:
        print(run)
        data = get_module_data(run, args.sensor_type, data)
    plot_data(data, args.sensor_type, args.labels)

    #data = get_module_data(1322, 'R4', {})
    #plot_data(data, 'R4', ['test'])

