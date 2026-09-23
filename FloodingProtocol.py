import logging

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration, LoopMission
from gradysim.protocol.messages.communication import BroadcastMessageCommand
from gradysim.simulator.extension.visualization_controller import VisualizationController

class Drone(IProtocol):
    waypoints = {
            0: [(100,0,10), (0,0,10)],
            1: [(100,100,10), (100,0,10)],
            2: [(100,100,10), (0,100,10)],
            3: [(0,100,0)],
            4: [(0,100,10), (-100,100,10)],
            5: [(-100,0,10), (-100,100,10)],
            6: [(0,0,10), (-100,0,10)]
    }
    def initialize(self):
        self.mission = MissionMobilityPlugin(self, MissionMobilityConfiguration(speed=40, loop_mission=LoopMission.RESTART))
        self.mission.start_mission(self.waypoints[self.provider.get_id()])
        self.vis = VisualizationController(self)
        self.enviado = False

        if self.provider.get_id() == 0:
            self.provider.schedule_timer("",
            self.provider.current_time() + 1
            )
            

    def handle_timer(self, timer: str):
        self.provider.send_communication_command(BroadcastMessageCommand("Red Velvet"))
        self.provider.schedule_timer("",self.provider.current_time() + 1)
        self.vis.paint_node(0,(255,0,0))
        
    def handle_packet(self, message: str):
        if self.enviado:
            return
        self.enviado = True
        self.vis.paint_node(self.provider.get_id(), (255, 0, 0))
        self.provider.send_communication_command(BroadcastMessageCommand("Red Velvet"))

    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finish(self):
        pass