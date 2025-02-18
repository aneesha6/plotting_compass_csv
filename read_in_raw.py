import csv

import matplotlib.pyplot as plt

def plot_histogram(data_dict):
    e_short_gate_values = [float(data['e_long_gate']) for data in data_dict.values()]
    
    plt.figure(figsize=(10, 6))
    plt.hist(e_short_gate_values, bins=50, edgecolor='black')
    plt.xlabel('e_long_gate: E / ADC Channel')
    plt.ylabel('Frequency')
    plt.title('Histogram of e_long_gate')
    
    # Save the histogram as an SVG file
    plt.savefig('e_long_gate_histogram.svg', format='svg')
    plt.close()
    

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
    plt.savefig('samples_scatter_plot.svg', format='svg')
    plt.close()


def get_max_samples(data_dict):
    max_samples_list = []
    
    for data in data_dict.values():
        samples = [float(sample) for sample in data['samples']]
        max_sample = max(samples)
        max_samples_list.append(max_sample)
    
    return max_samples_list

def plot_max_samples_histogram(max_samples_list):
    plt.figure(figsize=(10, 6))
    plt.hist(max_samples_list, bins=50, edgecolor='black')
    plt.xlabel('Peak height V/ADC Channel')
    plt.ylabel('Frequency')
    plt.title('Histogram of peak height')
    
    # Save the histogram as an SVG file
    plt.savefig('peak_hight_histogram.svg', format='svg')
    plt.close()

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

def main():
    file_path = '0@DT5720B #2-3-316_Data_p10_1000V_5h.csv'
    data = read_csv_to_dict(file_path)
    plot_histogram(data)
    plot_samples_scatter(data[3])
    max_samples_list = get_max_samples(data)
    plot_max_samples_histogram(max_samples_list)


if __name__ == "__main__":
    main()
