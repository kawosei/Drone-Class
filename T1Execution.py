import asyncio
from T1Protocol import Drone
from T1Satelite import Satelite
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.handler.visualization import VisualizationHandler, VisualizationConfiguration
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration
from gradysim.simulator.handler.communication import CommunicationHandler, CommunicationMedium
from gradysim.simulator.handler.mobility import MobilityHandler

def main():
    config = SimulationConfiguration(duration=40, real_time=True)

    builder = SimulationBuilder(config)

    builder.add_node(Drone, (0, 0, 10))
    builder.add_node(Drone, (75, 0, 10))
    builder.add_node(Drone, (37.5, -50, 10))
    builder.add_node(Drone, (0, -100, 10))
    builder.add_node(Drone, (-37.5, -50, 10))
    builder.add_node(Drone, (-75, 0, 10))
    builder.add_node(Drone, (-37.5, 50, 10))
    builder.add_node(Drone, (0, 100, 10))
    builder.add_node(Drone, (37.5, 50, 10))
    builder.add_node(Satelite, (115,140,10))
    builder.add_node(Satelite, (140,-140,10))
    builder.add_node(Satelite, (-115,-140,10))
    builder.add_node(Satelite, (-140,140,10))

    builder.add_handler(CommunicationHandler(CommunicationMedium(transmission_range=69)))

    builder.add_handler(MobilityHandler())

    builder.add_handler(TimerHandler())

    builder.add_handler(VisualizationHandler(
        VisualizationConfiguration(x_range=(-150,150), y_range=(-150,150),z_range=(0,10), open_browser=True)
    ))

    simulation = builder.build()

    asyncio.set_event_loop(asyncio.new_event_loop())

    simulation.start_simulation()


if __name__ == "__main__":
    main()