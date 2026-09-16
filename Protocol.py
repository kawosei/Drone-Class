import logging

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration, LoopMission
from gradysim.protocol.messages.communication import BroadcastMessageCommand
from gradysim.simulator.extension.visualization_controller import VisualizationController

class Drone(IProtocol):
    waypoints = {
        0: [(100,0,5), (0,0,5)],
        1: [(100,100,5), (100,0,5)],
        2: [(100,100,5), (0,100,5)],
        3: [(0,100,5)],
        4: [(0,100,5), (-100,100,5)],
        5: [(-100,0,5), (-100,100,5)],
        6: [(0,0,5), (-100,0,5)]
    }
    def initialize(self):
        self.mission = MissionMobilityPlugin(self, MissionMobilityConfiguration(speed=40, loop_mission=LoopMission.RESTART))
        self.mission.start_mission(self.waypoints[self.provider.get_id()])
        self.Sent = False
        self.vis = VisualizationController(self)

        if self.provider.get_id() == 0:
            self.provider.schedule_timer("",
                self.provider.current_time() + 1
            )

    def handle_timer(self, timer: str):
        self.provider.send_communication_command(BroadcastMessageCommand("Red Velvet"))
        self.provider.schedule_timer("",self.provider.current_time() + 1)

    def handle_packet(self, message: str):
        self.vis.paint_node(self.provider.get_id(), (255,0,0))
        if not self.provider.get_id() == 6:
            if message == "Red Velvet":
                self.provider.schedule_timer("", self.provider.current_time() + 1)
        if self.provider.get_id() == 6:
            self.provider.cancel_timer("")
            logging.info("Simulação Concluída")
            return
        if self.Sent:
            return
        self.Sent = True
        self.provider.send_communication_command(BroadcastMessageCommand("Doce de Leite"))


    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finish(self):
        pass