import csv
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os
import re
import numpy as np


import matplotlib.pyplot as plt


def plot_energy_histogram(data_dict, show_info=False, info_list=None, voltage="NaN"):
    e_long_gate_values = [float(data['e_long_gate']) for data in data_dict.values()]
    
    plt.figure(figsize=(10, 6))
    bin_counts, bin_edges, _ = plt.hist(e_long_gate_values, bins=30, edgecolor='black')
    plt.xlabel('Energy W / ADC Channel')
    plt.ylabel('Frequency')
    plt.title('Histogram of energy')

    # Calculate bin centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Calculate mean and median
    mean_value = np.mean(e_long_gate_values)
    median_value = np.median(e_long_gate_values)

    # Plot vertical lines for mean and median (from 0% to 70% of plot height)
    max_height = max(bin_counts)
    plt.plot([mean_value, mean_value], [0, max_height * 0.8], color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value:.2f}')
    plt.plot([median_value, median_value], [0, max_height * 0.8], color='b', linestyle='dashed', linewidth=1, label=f'Median: {median_value:.2f}')

    # Add ticks on top of the lines
    plt.text(mean_value, max_height * 0.82, f'Mean\n {mean_value:.0f}', ha='center', va='bottom', color='r')
    plt.text(median_value, max_height * 0.82, f'Median\n {median_value:.0f}', ha='center', va='bottom', color='b')

    # This section adds additional information of the setup and can be selected or deselected with show_info (bool)
    if show_info and info_list:
        info_text = r"$\bf{Setup\ info:}$" + "\n" + "\n".join(["    " + info for info in info_list])
        props = dict(boxstyle='round', facecolor='white', alpha=0.5, edgecolor='none')
        plt.gca().text(0.65, 0.95, info_text, transform=plt.gca().transAxes, fontsize=10,
                       verticalalignment='top', horizontalalignment='left', bbox=props)

    plt.tight_layout()

    # Save the histogram as an SVG file
    plt.savefig(f'plots/e_long_gate_histogram_{voltage}.svg', format='svg')
    plt.close()

    return bin_centers, bin_counts, round(mean_value,1)


    

def plot_samples_scatter(data):
    samples = [float(sample) for sample in data['samples']]
    positions = list(range(len(samples)))
    
    plt.figure(figsize=(10, 6))
    plt.scatter(positions, samples, label='Samples')
    
    plt.xlabel('Position in List')
    plt.ylabel('Sample Value')
    plt.title('Scatter Plot of Samples')
    plt.legend(loc='upper right')
    
    # Save the scatter plot as an SVG file
    plt.savefig('plots/samples_scatter_plot.svg', format='svg')
    plt.close()


def get_max_samples(data_dict):
    max_samples_list = []
    
    for data in data_dict.values():
        samples = [float(sample) for sample in data['samples']]
        max_sample = max(samples)
        max_samples_list.append(max_sample)
    
    return max_samples_list


def plot_peak_height_histogram(max_samples_list, show_info=False, info_list=None, voltage="NaN"):
    plt.figure(figsize=(10, 6))
    bin_counts, bin_edges, _ = plt.hist(max_samples_list, bins=30, edgecolor='black')
    plt.xlabel('Peak height V/ADC Channel')
    plt.ylabel('Frequency')
    plt.title('Histogram of peak height')

    # Calculate mean and median
    mean_value = np.mean(max_samples_list)
    median_value = np.median(max_samples_list)

    # Plot vertical lines for mean and median (from 0% to 70% of plot height)
    max_height = max(bin_counts)
    plt.plot([mean_value, mean_value], [0, max_height * 0.7], color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_value:.2f}')
    plt.plot([median_value, median_value], [0, max_height * 0.7], color='b', linestyle='dashed', linewidth=1, label=f'Median: {median_value:.2f}')

    # Add ticks on top of the lines
    plt.text(mean_value, max_height * 0.72, f'Mean:\n{mean_value:.2f}', ha='center', va='bottom', color='r')
    plt.text(median_value, max_height * 0.72, f'Median\n{median_value:.2f}', ha='center', va='bottom', color='b')

    # This section adds additional information of the setup and can be selected or deselected with show_info (bool)
    if show_info and info_list:
        info_text = r"$\bf{Setup\ info:}$" + "\n" + "\n".join(["    " + info for info in info_list])
        props = dict(boxstyle='round', facecolor='white', alpha=0.5, edgecolor='none')
        plt.gca().text(0.65, 0.95, info_text, transform=plt.gca().transAxes, fontsize=10,
                       verticalalignment='top', horizontalalignment='left', bbox=props)

    # Calculate bin centers
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    plt.tight_layout()

    # Save the histogram as an SVG file
    plt.savefig(f'plots/peak_height_histogram_{voltage}.svg', format='svg')
    plt.close()

    return bin_centers, bin_counts, round(mean_value,1)

def read_csv_to_dict(file_path):
    data_dict = {}
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        
        # Skip the header
        next(reader)
        
        for line_number, row in enumerate(reader, start=1):
            time_stampe = row[0]
            e_long_gate = row[1]
            e_short_gate = row[2]
            flags = row[3]
            samples = row[4:]
            
            data_dict[line_number] = {
                "time_stampe": time_stampe,
                "e_long_gate": e_long_gate,
                "e_short_gate": e_short_gate,
                "flags": flags,
                "samples": samples
            }
    
    return data_dict

def convert_to_utc(dt_str):
    local = datetime.strptime(dt_str, '%Y/%m/%d %H:%M:%S.%f%z')
    utc = local.astimezone(pytz.utc)
    return utc.strftime('%Y-%m-%d %H:%M:%S')

def extract_measurement_times(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    start_time_str = None
    stop_time_str = None

    for line in lines:
        if line.startswith("time.start"):
            start_time_str = line.split('=')[1].strip()
        elif line.startswith("time.stop"):
            stop_time_str = line.split('=')[1].strip()

    if start_time_str and stop_time_str:
        start_time_utc = convert_to_utc(start_time_str)
        stop_time_utc = convert_to_utc(stop_time_str)

        start_time = datetime.strptime(start_time_str, '%Y/%m/%d %H:%M:%S.%f%z')  # Corrected format
        stop_time = datetime.strptime(stop_time_str, '%Y/%m/%d %H:%M:%S.%f%z')  # Corrected format
        duration = stop_time - start_time
        duration_sec = int(duration.total_seconds())

        result = {
            "start_time_str": f"Start time (UTC): {start_time_utc}",
            "stop_time_str": f"Stop time (UTC): {stop_time_utc}",
            "duration_str": f"Duration: {duration_sec} s",
            "duration": duration_sec
        }

        return result
    else:
        raise ValueError("Start or stop time not found in file.")


def extract_settings(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Find the value for SRV_PARAM_CH_GATE
    gate_entry = root.find(".//parameters/entry[key='SRV_PARAM_CH_GATE']")
    srv_param_ch_gate_value = gate_entry.find(".//value/value").text if gate_entry is not None else None
    
    # Find the value for SRV_PARAM_CH_ENERGY_COARSE_GAIN
    energy_coarse_gain_entry = root.find(".//parameters/entry[key='SRV_PARAM_CH_ENERGY_COARSE_GAIN']")
    srv_param_ch_energy_coarse_gain_value = energy_coarse_gain_entry.find(".//value/value").text if energy_coarse_gain_entry is not None else None
    
    # Extract only the numbers from the CHARGESENS_2560_PC_LSB string
    if srv_param_ch_energy_coarse_gain_value and 'CHARGESENS_' in srv_param_ch_energy_coarse_gain_value:
        srv_param_ch_energy_coarse_gain_value = ''.join(filter(str.isdigit, srv_param_ch_energy_coarse_gain_value))
    
    # Find the value for SRV_PARAM_CH_GATEPRE
    gatepre_entry = root.find(".//parameters/entry[key='SRV_PARAM_CH_GATEPRE']")
    srv_param_ch_gatepre_value = gatepre_entry.find(".//value/value").text if gatepre_entry is not None else None
    
    # Format the values as a dictionary with keys
    result = {
        "gate_length": f"Gate length: {srv_param_ch_gate_value} ns",
        "pre_gate_length": f"Pre-Gate length: {srv_param_ch_gatepre_value} ns",
        "energy_gain": f"Energy gain: {srv_param_ch_energy_coarse_gain_value} pC/LSB"
    }
        
    return result

def plot_compare_energy_hists(e_bins, voltages):
    # Define a list of colors
    colors = plt.cm.viridis(np.linspace(0, 1, len(voltages)))

    plt.figure()
    
    for i in range(0, len(voltages)):
        plt.plot(e_bins[voltages[i]][0], e_bins[voltages[i]][1], color=colors[i], label=f'Bias voltage: {voltages[i]} V')

    plt.xlabel('Energy W / ADC Channel')
    plt.ylabel('Frequency')
    plt.title('Comparision energy histograms')
    plt.legend()
    
    plt.tight_layout()

    plt.savefig('plots/energy_bins_comparision.svg', format='svg')
    plt.close()



def plot_compare_peak_height_hists(ph_bins, voltages):
    # Define a list of colors
    colors = plt.cm.viridis(np.linspace(0, 1, len(voltages)))

    plt.figure()
    
    for i in range(0, len(voltages)):
        plt.plot(ph_bins[voltages[i]][0], ph_bins[voltages[i]][1], color=colors[i], label=f'Bias voltage: {voltages[i]} V')

    plt.xlabel('Peak height V / ADC Channel')
    plt.ylabel('Frequency')
    plt.title('Comparision peak height histograms')
    plt.legend()
    
    plt.tight_layout()

    plt.savefig('plots/peak_height_bins_comparision.svg', format='svg')

    plt.close()


def plot_means_over_voltages(dict1, dict2,voltages):

    bais_voltages = []
    means_e = []
    means_ph = []

    for voltage in voltages:
        bais_voltages.append(int(voltage))
        means_e.append(int(dict1[voltage]))
        means_ph.append(int(dict2[voltage]))

    fig, ax1 = plt.subplots()

    ax1.plot(bais_voltages, means_e, marker='o', linestyle='-', label='Dict 1', color='b')
    ax1.set_xlabel('Mean Bias Voltage')
    ax1.set_ylabel('Mean Energy W / ADC Channels', color='b')

    ax2 = ax1.twinx()
    ax2.plot(bais_voltages, means_ph, marker='x', linestyle='--', label='Dict 2', color='r')
    ax2.set_ylabel('Peak Height V / ADC Channel', color='r')

    plt.title('Energy and Peak Height Means vs. Bias Voltage')
    fig.tight_layout()

    plt.savefig('plots/means_over_voltages.svg', format='svg')
    plt.close()


def dict_to_list(data_dict, key_list):
    return [data_dict[key] for key in key_list if key in data_dict]

def main():
    show_setup_info = True

    e_bins = {}
    ph_bins = {}
    voltages = []
    means_e = {}
    means_ph = {}

    for root, dirs, files in os.walk("data"):
        for dir in dirs:
            subdirectory_path = os.path.join(root, dir)
            file_path = os.path.join(subdirectory_path, f'FILTERED/0@DT5720B #2-3-316_Data_{subdirectory_path.split("/")[1]}.csv')
            run_info_path = os.path.join(subdirectory_path, 'run.info')
            settings_path = os.path.join(subdirectory_path, 'settings.xml')

            if os.path.exists(file_path):
                data = read_csv_to_dict(file_path)

                # Extract voltage from the file name
                voltage_match = re.search(r'_([\d]+)V_', file_path)
                voltage = voltage_match.group(1) if voltage_match else 'Unknown'

                setup_info = {}
                setup_info.update({"voltage": f"Bias voltrage: {voltage} V"})
                setup_info.update({"n_events": f'Number capt. events: {len(data)}'}) # adding number of events
                setup_info.update(extract_measurement_times(run_info_path)) # adding time related info
                setup_info.update(extract_settings(settings_path)) # adding settings related info
                setup_info.update({"events_per_sec": f'Events per sec.: {round(len(data)/setup_info["duration"],2)}'}) # calc and add events per sec

                key_list = ["voltage", "n_events", "duration_str", "events_per_sec", "start_time_str", "stop_time_str", "gate_length", "pre_gate_length", "energy_gain"]
                e_bins_pos_tmp, e_bins_counts_tmp, mean_e_tmp = plot_energy_histogram(data, show_setup_info, dict_to_list(setup_info, key_list), voltage)
                #plot_samples_scatter(data[3])
                max_samples_list = get_max_samples(data)
                key_list = ["voltage", "n_events", "duration_str", "events_per_sec", "start_time_str", "stop_time_str"]
                voltages.append(voltage)
                ph_bin_pos_tmp, ph_bin_count_tmp, mean_ph_tmp = plot_peak_height_histogram(max_samples_list, show_setup_info, dict_to_list(setup_info, key_list), voltage)
                e_bins.update({f"{voltage}": [e_bins_pos_tmp, e_bins_counts_tmp]})
                ph_bins.update({f"{voltage}": [ph_bin_pos_tmp, ph_bin_count_tmp]})
                means_e.update({f"{voltage}": mean_e_tmp})
                means_ph.update({f"{voltage}": mean_ph_tmp})

            else:
                print(f"Warning: {file_path} does not exit")


    voltages_list = sorted(voltages, key=int)
    plot_compare_energy_hists(e_bins, voltages_list)    
    plot_compare_peak_height_hists(ph_bins, voltages_list)
    plot_means_over_voltages(means_e,means_ph, voltages_list)    


if __name__ == "__main__":
    main()
