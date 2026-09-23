import asyncio
from FloodingProtocol import Drone
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.handler.visualization import VisualizationHandler, VisualizationConfiguration
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration
from gradysim.simulator.handler.communication import CommunicationHandler, CommunicationMedium, CommunicationCommand, CommunicationCommandType
from gradysim.simulator.handler.mobility import MobilityHandler

def main():
    config = SimulationConfiguration(duration=20,real_time=True)

    builder = SimulationBuilder(config)

    builder.add_node(Drone, (0, 0, 10))
    builder.add_node(Drone, (100, 50, 10))
    builder.add_node(Drone, (0, 100, 10))
    builder.add_node(Drone, (0, 120, 0))
    builder.add_node(Drone, (-100, 100, 10))
    builder.add_node(Drone, (-100, 50, 0))
    builder.add_node(Drone, (-100, 0, 10))
    

    builder.add_handler(CommunicationHandler(CommunicationMedium(transmission_range=100)))

    builder.add_handler(MobilityHandler())

    builder.add_handler(TimerHandler())

    builder.add_handler(VisualizationHandler(
        VisualizationConfiguration(x_range=(-100,100), y_range=(-100,100),z_range=(0,10), open_browser=True)
    ))

    simulation = builder.build()

    asyncio.set_event_loop(asyncio.new_event_loop())

    simulation.start_simulation()


if __name__ == "__main__":
    main()