import matplotlib.pyplot as plt
from util.formulas import jains_fairness_index


def plot_arrival_vs_fairness_chart(simulation):
    trip_infos = simulation.get_data()
    time_window_size = 100
    time_windows = [[]]
    arrivals = [int(float(vehicle['arrival'])) for vehicle in trip_infos]
    max_time = max(arrivals)

    for i in range(max_time // time_window_size):
        time_windows.append([])
    for vehicle in trip_infos:
        arrival_time = int(float(vehicle['arrival']))
        time_windows[arrival_time // time_window_size].append(vehicle)

    sum_of_arrivals_per_time_window = [len(time_window) for time_window in time_windows]
    jains_fairness_per_time_window = []
    for time_window in time_windows:
        delays = [int(float(vehicle['timeLoss'])) for vehicle in time_window]
        jains_fairness_per_time_window.append(jains_fairness_index(delays))

    assert len(sum_of_arrivals_per_time_window) == len(jains_fairness_per_time_window)

    fig, ax1 = plt.subplots()
    ax1.set_xlabel(f'time window (size: {time_window_size})')
    ax1.set_ylabel('number of arrvials', color='tab:blue')
    ax1.plot(sum_of_arrivals_per_time_window, color='tab:blue', alpha=0.75)
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('jains fairness index', color='tab:red')
    ax2.plot(jains_fairness_per_time_window, color='tab:red', alpha=0.75)
    ax2.tick_params(axis='y', labelcolor='tab:red')

    for x in range(len(sum_of_arrivals_per_time_window)):
        plt.axvline(x=x, color='black', alpha=0.1)

    fig.suptitle('Arrivals vs. Jain\'s fairness index per time window')
    fig.tight_layout()
    plt.show()
