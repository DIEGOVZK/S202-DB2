import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def plot_temperature_data(fig, ax, data_array, device_name, threshold_value=38):
    normalized_values = (data_array - data_array.min()) / (data_array.max() - data_array.min())
    threshold = (threshold_value - data_array.min()) / (data_array.max() - data_array.min())

    colors = ['red' if value > threshold else plt.cm.inferno(value) for value in normalized_values]
    scatter = ax.scatter(range(len(data_array)), data_array, c=colors, s=2)

    norm = mcolors.Normalize(vmin=data_array.min(), vmax=data_array.max())
    sm = plt.cm.ScalarMappable(cmap='inferno', norm=norm)
    sm.set_array([])

    ax.axhline(y=threshold_value, color='r', linestyle='--')
    fig.colorbar(sm, ax=ax, label='Temperatura [ºC]')

    first_exceed_index = next((i for i, value in enumerate(data_array) if value > threshold_value), None)
    if first_exceed_index is not None:
        ax.plot(first_exceed_index, data_array[first_exceed_index], 'bo', label='Alarm')

    ax.set_title(f'Temperature data from IoT device {device_name}')
    ax.set_xlabel('Index')
    ax.legend()
    ax.grid(True)