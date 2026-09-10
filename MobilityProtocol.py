import logging

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration
from gradysim.protocol.messages.communication import BroadcastMessageCommand

class Protocol_1(IProtocol):
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
        self.mission = MissionMobilityPlugin(self, MissionMobilityConfiguration(speed=10))
        self.mission.start_mission(self.waypoints[self.provider.get_id()])

        if self.provider.get_id() == 0:
            self.provider.schedule_timer("",
                self.provider.current_time() + 1
            )

    def handle_timer(self, timer: str):
        self.provider.send_communication_command(BroadcastMessageCommand())
        self.provider.schedule_timer("",self.provider.current_time() + 1)

    def handle_packet(self, message: str):
        if not self.provider.get_id() == 6:
            self.provider.schedule_timer("", self.provider.current_time() + 1)
            raise Exception("Simulação Concluída")

    def handle_telemetry(self, telemetry: Telemetry):
        pass

    def finish(self):
        pass