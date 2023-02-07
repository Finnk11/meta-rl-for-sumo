import os
import sys
import tempfile
import xml.etree.cElementTree as elementTree

import traci
from sumolib import checkBinary

import SumoConfiguration


class Simulation:

    def __init__(self, configuration: SumoConfiguration = None, record_trip_info: bool = True, use_gui: bool = False):
        self._record_trip_info = record_trip_info
        self._use_gui = use_gui
        self._data = None
        self._configuration = configuration

    def run(self, duration=3600):
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("Please declare the environment variable 'SUMO_HOME'")

        if self._configuration:
            sumocfg = str(self._configuration.sumo_config_file.name)

        else:
            sumocfg = os.path.join(os.getcwd(), '../nets/single_intersection/exp.sumocfg')

        if self._use_gui:
            sumo_binary = checkBinary('sumo-gui')
        else:
            sumo_binary = checkBinary('sumo')

        temp_data_xml_file = None
        sumo_parameters = [sumo_binary, "-c", sumocfg, '--delay', '2', '--start', '--quit-on-end']
        if self._record_trip_info:
            if os.name == 'nt':
                temp_data_xml_file = tempfile.NamedTemporaryFile(delete=False)
            else:
                temp_data_xml_file = tempfile.NamedTemporaryFile()
            sumo_parameters.extend(['--tripinfo-output', temp_data_xml_file.name])

        traci.start(sumo_parameters)

        if self._use_gui:
            traci.gui.setSchema(traci.gui.DEFAULT_VIEW, "real world")
            traci.gui.setZoom(traci.gui.DEFAULT_VIEW, 350)
            traci.gui.setOffset(traci.gui.DEFAULT_VIEW, 250, 250)

        step = 0
        while step < duration:
            traci.simulationStep()
            step += 1
            print('step:', step)
        traci.close()

        if self._record_trip_info:
            tree = elementTree.ElementTree(file=temp_data_xml_file)
            trip_info_list = []
            for child in tree.getroot():
                trip = child.attrib
                trip_info = {'id': trip['id'],
                             'depart': trip['depart'],
                             'arrival': trip['arrival'],
                             'duration': trip['duration'],
                             'timeLoss': trip['timeLoss'],
                             'waitingCount': trip['waitingCount'],
                             'waitingTime': trip['waitingTime'],
                             }
                trip_info_list.append(trip_info)

            self._data = trip_info_list

            if os.name == 'nt':
                temp_data_xml_file.close()
                os.unlink(temp_data_xml_file.name)

    def get_data(self):
        return self._data

    def __getitem__(self, item):
        return self._data.__getitem__(item)
