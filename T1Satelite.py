import json
import logging

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration, LoopMission
from gradysim.protocol.messages.communication import BroadcastMessageCommand, SendMessageCommand
from gradysim.simulator.extension.visualization_controller import VisualizationController

class Satelite(IProtocol):
    waypoints = {
        9: [(115,-140,10), (115,140,10)],
        10: [(-140,-140,10), (140,-140,10)],
        11: [(-115,140,10), (-115,-140,10)],
        12: [(140,140,10), (-140,140,10)],
    }

    SateliteID = {
        9: (255,0,0),
        10: (0,255,0),
        11: (0,0,255),
        12: (255,255,0)
    }

    Packets = {
        9: "Red",
        10: "Green",
        11: "Blue",
        12: "Yellow"
    }

    count = int()

    def initialize(self):
        self.mission = MissionMobilityPlugin(self, MissionMobilityConfiguration(speed=30, loop_mission=LoopMission.REVERSE))
        self.mission.start_mission(self.waypoints[self.provider.get_id()])
        self.vis = VisualizationController(self)
        self.provider.schedule_timer("pintar", 2)
        
    def handle_timer(self, timer: str):
        if timer == "pintar":
            self.vis.paint_node(self.provider.get_id(),self.SateliteID[self.provider.get_id()])
            self.provider.schedule_timer("pintar", self.provider.current_time() + 1)

    def handle_packet(self, message: str):
        if message[-3] == "t":
            self.data = json.loads(message)
            self.provider.send_communication_command(SendMessageCommand(json.dumps({
                "message": self.Packets[self.provider.get_id()],"id": self.provider.get_id(),"posicao": self.position, "type": "info"}), self.data["id"]))
            return

        if self.provider.get_id() == 9:
            if message == "Blue":
                logging.info("Mensagem Recebida")
                self.count += 1
        if self.provider.get_id() == 10:
            if message == "Yellow":
                logging.info("Mensagem Recebida")
                self.count += 1
        if self.provider.get_id() == 11:
            if message == "Red":
                logging.info("Mensagem Recebida")
                self.count += 1
        if self.provider.get_id() == 12:
            if message == "Green":
                logging.info("Mensagem Recebida")
                self.count += 1

    def handle_telemetry(self, telemetry: Telemetry):
        self.position = telemetry.current_position

    def finish(self):
        logging.info(self.count)
