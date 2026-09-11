import asyncio
from MobilityProtocol import Protocol_1
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.handler.visualization import VisualizationHandler, VisualizationConfiguration
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration
from gradysim.simulator.handler.communication import CommunicationHandler, CommunicationMedium, CommunicationCommand, CommunicationCommandType
from gradysim.simulator.handler.mobility import MobilityHandler

def main():
    config = SimulationConfiguration(duration=30,real_time=True)

    builder = SimulationBuilder(config)

    builder.add_node(Protocol_1, (0, 0, 0))
    builder.add_node(Protocol_1, (100, 50, 0))
    builder.add_node(Protocol_1, (0, 100, 0))
    builder.add_node(Protocol_1, (0, 100, 0))
    builder.add_node(Protocol_1, (-100, 100, 0))
    builder.add_node(Protocol_1, (-100, 50, 0))
    builder.add_node(Protocol_1, (-100, 0, 0))
    

    builder.add_handler(CommunicationHandler(CommunicationMedium(transmission_range=50)))

    builder.add_handler(MobilityHandler())

    builder.add_handler(TimerHandler())

    builder.add_handler(VisualizationHandler(
        VisualizationConfiguration(open_browser=True)
    ))

    simulation = builder.build()

    asyncio.set_event_loop(asyncio.new_event_loop())

    simulation.start_simulation()


if __name__ == "__main__":
    main()
