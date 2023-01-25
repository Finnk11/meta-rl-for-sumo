import os
import sys
import tempfile
import xml.etree.cElementTree as elementTree

import matplotlib.pyplot as plt
import traci
from sumolib import checkBinary

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

LIBSUMO = 'LIBSUMO_AS_TRACI' in os.environ

netfile = os.path.join(os.getcwd(), 'nets/single_intersection/exp.net.xml')
routefile = os.path.join(os.getcwd(), 'nets/single_intersection/stat.gen.rou.xml')
sumocfg = os.path.join(os.getcwd(), 'nets/single_intersection/exp.sumocfg')

use_gui = False
conn_label = str(0)  # for trace multi-client support

if use_gui:
    sumoBinary = checkBinary('sumo-gui')
else:
    sumoBinary = checkBinary('sumo')

sumoCmd = [sumoBinary, "-c", sumocfg, '--delay', '2', '--start', '--quit-on-end']
# view settings can be provided by a file or by traci (see below)
# sumoCmd.extend(['--gui-settings-file', 'viewSettings.xml'])

record_trip_info = True
if record_trip_info:
    # file stored as /tmp/tmpxfdfe343id
    if os.name == 'nt':
        trip_file = tempfile.NamedTemporaryFile(delete=False)
    else:
        trip_file = tempfile.NamedTemporaryFile()
    sumoCmd.extend(['--tripinfo-output', trip_file.name])

traci.start(sumoCmd)

if use_gui:
    # view settings when running sumo gui
    traci.gui.setSchema(traci.gui.DEFAULT_VIEW, "real world")
    traci.gui.setZoom(traci.gui.DEFAULT_VIEW, 350)
    traci.gui.setOffset(traci.gui.DEFAULT_VIEW, 250, 250)

# That means, TimeLoss can also be computed online!
# print("stopArrivalDelay",traci.vehicle.getStopArrivalDelay(vehID))
# print("timeloss", traci.vehicle.getTimeLoss(vehID))

step = 0

while step < 3600:
    traci.simulationStep()
    # if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
    #   traci.trafficlight.setRedYellowGreenState("0", "GrGr")
    step += 1
    print('step:', step)
traci.close()


# Jain's fairness index
# Equals 1 when all vehicles have the same delay
def fairness_index(d):
    if len(d) > 1:
        return sum(d) ** 2 / (len(d) * sum([i ** 2 for i in d]))
    return 1


# store information from the trip_info file
# to a dictionary
def collect_trip_info():
    if record_trip_info:
        tree = elementTree.ElementTree(file=trip_file)
        trip_info_list = []
        for child in tree.getroot():
            trip = child.attrib
            trip_info = {'id': trip['id'],
                         'depart_sec': trip['depart'],
                         'arrival_sec': trip['arrival'],
                         'duration_sec': trip['duration'],
                         'timeLoss_sec': trip['timeLoss'],
                         'wait_step': trip['waitingCount'],
                         'wait_sec': trip['waitingTime'],
                         }
            trip_info_list.append(trip_info)
        return trip_info_list
    else:
        return []


def plot_arrival_vs_fairness_chart(trip_info_lst):
    time_window_size = 100
    time_windows = [[]]
    arrivals = [int(float(vehicle['arrival_sec'])) for vehicle in trip_info_lst]
    max_time = max(arrivals)

    for i in range(max_time // time_window_size):
        time_windows.append([])
    for vehicle in trip_info_lst:
        arrival_time = int(float(vehicle['arrival_sec']))
        time_windows[arrival_time // time_window_size].append(vehicle)

    sum_of_arrivals_per_time_window = [len(time_window) for time_window in time_windows]
    jains_fairness_per_time_window = []
    for time_window in time_windows:
        delays = [int(float(vehicle['timeLoss_sec'])) for vehicle in time_window]
        jains_fairness_per_time_window.append(fairness_index(delays))

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


def main():
    trip_info_lst = collect_trip_info()
    print('trip_info:', len(trip_info_lst))
    arrivals = [float(a['arrival_sec']) for a in trip_info_lst]
    print('arrivals:', len(arrivals))
    arr = [x > 0 for x in arrivals]
    print(sum(arr))

    delays = [float(a['timeLoss_sec']) for a in trip_info_lst]
    print('Jain\'s fairness index:', fairness_index(delays))
    print('Throughput:', len(arr))

    plot_arrival_vs_fairness_chart(trip_info_lst)


if __name__ == '__main__':
    main()
    if record_trip_info and os.name == 'nt':
        trip_file.close()
        os.unlink(trip_file.name)
