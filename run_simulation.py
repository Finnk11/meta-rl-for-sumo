import os
import sys
import tempfile
import xml.etree.cElementTree as elementTree
from sumolib import checkBinary
import traci

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

LIBSUMO = 'LIBSUMO_AS_TRACI' in os.environ

netfile = os.path.join(os.getcwd(), 'nets/single_intersection/exp.net.xml')
routefile = os.path.join(os.getcwd(), 'nets/single_intersection/stat.gen.rou.xml')
sumocfg = os.path.join(os.getcwd(), 'nets/single_intersection/exp.sumocfg')

use_gui = True
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


trip_info_lst = collect_trip_info()
print('trip_info:', len(trip_info_lst))
arrivals = [float(a['arrival_sec']) for a in trip_info_lst]
print('arrivals:', len(arrivals))
arr = [x > 0 for x in arrivals]
print(sum(arr))

delays = [float(a['timeLoss_sec']) for a in trip_info_lst]
print('Jain\'s fairness index:', fairness_index(delays))
print('Throughput:', len(arr))
