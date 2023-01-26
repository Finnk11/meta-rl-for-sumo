import os
import sys
import tempfile
import xml.etree.cElementTree as elementTree
from sumolib import checkBinary
import traci
from nets.generate import generate_dyn_routefile

avg_queue_length_lst=[]
lane_index_lst=[]

fairness_index_lst=[]

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

LIBSUMO = 'LIBSUMO_AS_TRACI' in os.environ

# choose a fix peak
for peak in [0.4]:
    flow_file = tempfile.NamedTemporaryFile()
    generate_dyn_routefile(flow_file.name, pns_peak=peak, pwe_peak=peak)

    netfile = os.path.join(os.getcwd(), 'nets/single_intersection/exp.net.xml')

    # new sumo-config needed
    config_str = """<configuration>
\t  <input>
\t\t    <net-file value="{net_file}"/>"
\t\t    <route-files value="{flow_file}"/>
\t  </input>
\t  <time>
\t\t    <begin value="0"/>
\t\t    <end value="3600"/>
\t  </time>
</configuration>
        """.format(flow_file=flow_file.name, net_file=str(netfile))

    # generate temp sumo config file
    config_file = tempfile.NamedTemporaryFile(suffix='.sumocfg')
    with open(config_file.name, 'w') as config:
        config.write(config_str)
        config.close()

    netfile = os.path.join(os.getcwd(), 'nets/single_intersection/exp.net.xml')
    # routefile = os.path.join(os.getcwd(), 'nets/single_intersection/stat.gen.rou.xml')
    routefile = flow_file
    #sumocfg = os.path.join(os.getcwd(), 'nets/single_intersection/exp.sumocfg')
    sumocfg=config_file.name

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
        trip_file = tempfile.NamedTemporaryFile()
        sumoCmd.extend(['--tripinfo-output', trip_file.name])

    traci.start(sumoCmd)

    if use_gui:
        # view settings when running sumo gui
        traci.gui.setSchema(traci.gui.DEFAULT_VIEW, "real world")
        traci.gui.setZoom(traci.gui.DEFAULT_VIEW, 350)
        traci.gui.setOffset(traci.gui.DEFAULT_VIEW, 250, 250)

    step = 0
    queue_length_lst = []

    while step < 3600:
        traci.simulationStep()

        # inspect every 5 steps, start at step=100
        if (step+1) % 5 == 0 and step > 100:
            for i, laneID in enumerate(traci.trafficlight.getControlledLanes('nt1')):
                vehicles_on_lane = traci.lane.getLastStepVehicleIDs(laneID)
                # either rGrG, GrGr, yryr, ryry
                phase = traci.trafficlight.getRedYellowGreenState('nt1')
                # count vehicles with speed < 0.1 m/s
                speeds_waiting_vehicles = [traci.vehicle.getSpeed(c) for c in vehicles_on_lane if traci.vehicle.getSpeed(c) <0.1]
                # add number of vehicles waiting at red
                if len(speeds_waiting_vehicles) > 0 and phase[i] == 'r':
                    queue_length_lst.append(len(speeds_waiting_vehicles))
                    # record the lane
                    lane_index_lst.append(i)

        step += 1
        # print('step:', step)
    # average queue length of vehicles waiting at red
    avg_queue_len = float(sum(queue_length_lst))/len(queue_length_lst)
    print('average queue length:', avg_queue_len)
    # collect average queue length for different arrival probs
    avg_queue_length_lst.append(avg_queue_len)

    traci.close()

    # Jain's fairness index
    # Equals 1 when all vehicles have the same delay
    def fairness_index(d):
        return sum(d)**2/(len(d)*sum([i**2 for i in d]))

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


    #trip_info_lst = collect_trip_info()
    #print('trip_info:', len(trip_info_lst))
    #arrivals = [float(a['arrival_sec']) for a in trip_info_lst]
    #print('arrivals:', len(arrivals))
    #arr = [x > 0 for x in arrivals]
    #print(sum(arr))

    #delays = [float(a['timeLoss_sec']) for a in trip_info_lst]
    #fairness_index = fairness_index(delays)
    #print('Jain\'s fairness index:', fairness_index)

    # collect fairness index for various arrival probs
    #fairness_index_lst.append(fairness_index)
    #print('Throughput:', len(arr))

#print("AVG QUEUE LENGTH:", avg_queue_length_lst)
#print("FAIRNESS INDEX:", fairness_index_lst)


import json

laneID_queue_length_dict = {0: [], 1: [], 2: [], 3: []}
for laneID, queue_length in zip(lane_index_lst, queue_length_lst):
    laneID_queue_length_dict[laneID].append(queue_length)


# To save the dictionary into a file:
json.dump(laneID_queue_length_dict, open("Json/boxplot_data.json", 'w'))

