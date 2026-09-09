import asyncio
from FirstProject import CounterProtocol
from gradysim.simulator.handler.timer import TimerHandler
from gradysim.simulator.handler.visualization import VisualizationHandler, VisualizationConfiguration
from gradysim.simulator.simulation import SimulationBuilder, SimulationConfiguration
from gradysim.simulator.handler.communication import CommunicationHandler, CommunicationMedium
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration

def main():
    # Configuring the simulator. The only option that interests us
    # is limiting the simulator to 10 real-world seconds.
    config = SimulationConfiguration(duration=60,real_time=True)

    # Instantiating the simulator builder with the created config
    builder = SimulationBuilder(config)

    # Calling the add_node function we create a network node that
    # will run the CounterProtocol we created.
    builder.add_node(CounterProtocol, (10, 0, 0))
    builder.add_node(CounterProtocol, (0, 0, 0))

    # Handlers enable certain simulator features. In the case of our
    # simulator all we really need is a timer.
    builder.add_handler(TimerHandler())

    # Visualization runs a live 3D view at http://localhost:5678
    # It requires real_time=True in the configuration above.
    builder.add_handler(VisualizationHandler(
        VisualizationConfiguration(open_browser=True)
    ))

    # Calling the build functions creates a simulator from the previously
    # specified options.
    simulation = builder.build()

    # The start_simulation() method will run the simulator until our 10-second
    # limit is reached.
    # Python 3.12+ nao cria mais um event loop automaticamente, e o gradysim
    # depende de um existir quando real_time=True. Criamos um aqui.
    asyncio.set_event_loop(asyncio.new_event_loop())

    simulation.start_simulation()


if __name__ == "__main__":
    main()
