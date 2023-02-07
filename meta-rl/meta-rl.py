# import run_simulation as simulation
import Simulation
import Configuration
from plots import plots
from util.formulas import jains_fairness_index


def main():
    simulation = Simulation.Simulation()
    simulation.run()

    # configuration = Configuration.Configuration()
    # print(configuration.generate_config_file())

    # plots.plot_arrival_vs_fairness_chart(simulation)
    plots.plot_fairness_over_time(simulation)


if __name__ == '__main__':
    main()
