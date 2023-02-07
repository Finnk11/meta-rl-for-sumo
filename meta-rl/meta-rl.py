# import run_simulation as simulation
import os

import Simulation
import SumoConfiguration
from plots import plots
from util.formulas import jains_fairness_index


def main():
    netfile = os.path.join(os.getcwd(), '../nets/single_intersection/exp.net.xml')
    routefile = os.path.join(os.getcwd(), '../nets/single_intersection/dyn.gen.rou_unbalanced.xml')
    configuration = SumoConfiguration.SumoConfiguration(netfile, routefile, 3600)

    simulation = Simulation.Simulation(configuration)
    simulation.run()

    # configuration = Configuration.Configuration()
    # print(configuration.generate_config_file())

    plots.plot_arrival_vs_fairness_chart(simulation)
    # plots.plot_fairness_over_time(simulation)


if __name__ == '__main__':
    main()
