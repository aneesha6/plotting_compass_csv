import csv
import matplotlib.pyplot as plt
import numpy as np


def plot_hist_compare_energy(list_data_dict):
    labels = ['Data from 3h run', 'Data from 30min run']
    
    plt.figure(figsize=(10, 6))

    all_energies = []
    for data_dict in list_data_dict:
        for key in data_dict.keys():
            all_energies.append(float(data_dict[key]["e_long_gate"]))

    # Determine common bins
    bins = np.linspace(min(all_energies), max(all_energies), 30)

    for data_dict in list_data_dict:
        list_energies = [float(data_dict[key]["e_long_gate"]) for key in data_dict.keys()]
        plt.hist(list_energies, bins=bins, edgecolor='black', alpha=0.7, label=labels[list_data_dict.index(data_dict)])

    plt.xlabel('Energy')
    plt.ylabel('Frequency')
    plt.title('Histogram of energy of two runs with same setup but different duration (1400V)')
    plt.legend(loc='upper right')
    plt.tight_layout()

    plt.text(0.98, 0.85, 'Data superimposed on \ntop of each other', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes)

    plt.savefig(f'plots/comparing_durations/comparing_duration_energy.svg', format='svg')
    plt.close()


def plot_hist_compare_ph(list_data_dict):
    labels = ['Data from 3h run', 'Data from 30min run']
    
    plt.figure(figsize=(10, 6))

    all_peak_heights = []
    for data_dict in list_data_dict:
        for key in data_dict.keys():
            samples = [float(sample) for sample in data_dict[key]['samples']]
            max_sample = max(samples)
            all_peak_heights.append(max_sample)

    # Determine common bins
    bins = np.linspace(min(all_peak_heights), max(all_peak_heights), 30)

    for data_dict in list_data_dict:
        list_ph = []
        for key in data_dict.keys():
            samples = [float(sample) for sample in data_dict[key]['samples']]
            max_sample = max(samples)
            list_ph.append(max_sample)
        plt.hist(list_ph, bins=bins, edgecolor='black', alpha=0.7, label=labels[list_data_dict.index(data_dict)])

    plt.xlabel('Peak height')
    plt.ylabel('Frequency')
    plt.title('Histogram of peak height of two runs with same setup but different duration (1400V)')
    plt.legend(loc='upper right')
    plt.tight_layout()

    plt.text(0.98, 0.85, 'Data superimposed on \ntop of each other', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes)

    plt.savefig(f'plots/comparing_durations/comparing_duration_ph.svg', format='svg')
    plt.close()

def read_csv_to_dict(file_path):
    data_dict = {}

    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        # Skip the header
        next(reader)

        for line_number, row in enumerate(reader, start=1):
            time_stamp = row[0]
            e_long_gate = row[1]
            e_short_gate = row[2]
            flags = row[3]
            samples = row[4:]

            data_dict[line_number] = {
                "time_stamp": time_stamp,
                "e_long_gate": e_long_gate,
                "e_short_gate": e_short_gate,
                "flags": flags,
                "samples": samples
            }

    return data_dict


def main():
    list_of_files = [
        "data/comparing_durations/p10_1400V_10x_bline-95_80LSB_3hr_fix/FILTERED/0@DT5720B #2-3-316_Data_p10_1400V_10x_bline-95_80LSB_3hr_fix.csv",
        "data/comparing_durations/p10_1400V_10x_bline-95_30min/FILTERED/0@DT5720B #2-3-316_Data_p10_1400V_10x_bline-95_30min.csv"
    ]
    list_data_dict = []
    for file in list_of_files:
        list_data_dict.append(read_csv_to_dict(file))

    plot_hist_compare_energy(list_data_dict)
    plot_hist_compare_ph(list_data_dict)


if __name__ == "__main__":
    main()