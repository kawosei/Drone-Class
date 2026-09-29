import json
import logging
import math

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration, LoopMission
from gradysim.protocol.messages.communication import BroadcastMessageCommand, SendMessageCommand
from gradysim.simulator.extension.visualization_controller import VisualizationController

class Drone(IProtocol):
    waypoints = {
        0: [(0,0,10)],
        1: [(0,-100,10), (-75,0,10), (0,100,10), (75,0,10)],
        2: [(0,-100,10), (-75,0,10), (0,100,10), (75,0,10)],
        3: [(-75,0,10), (0,100,10), (75,0,10), (0,-100,10)],
        4: [(-75,0,10), (0,100,10), (75,0,10), (0,-100,10)],
        5: [(0,100,10), (75,0,10), (0,-100,10), (-75,0,10)],
        6: [(0,100,10), (75,0,10), (0,-100,10), (-75,0,10)],
        7: [(75,0,10), (0,-100,10), (-75,0,10), (0,100,10)],
        8: [(75,0,10), (0,-100,10), (-75,0,10), (0,100,10)]
    }

    def initialize(self):
        self.mission = MissionMobilityPlugin(self, MissionMobilityConfiguration(speed=10, loop_mission=LoopMission.RESTART))
        self.mission.start_mission(self.waypoints[self.provider.get_id()])

        self.provider.schedule_timer("broadcast", self.provider.current_time() + 1)

        self.recebidas = set()

        self.vis = VisualizationController(self)
    def handle_timer(self, timer: str):
        if timer == "broadcast":
            self.provider.send_communication_command(BroadcastMessageCommand(json.dumps({
                "id": self.provider.get_id(), "posicao": self.position, "type": "broadcast"})))
            if "Blue" in self.recebidas and math.dist(self.position, (115,0,10)) < 69:
                self.provider.send_communication_command(SendMessageCommand("Blue", 9))
                self.provider.schedule_timer("discard blue", self.provider.current_time() + 3)
            if "Yellow" in self.recebidas and math.dist(self.position, (0,-140,10)) < 69:
                self.provider.send_communication_command(SendMessageCommand("Yellow", 10))
                self.provider.schedule_timer("discard yellow", self.provider.current_time() + 3)
            if "Red" in self.recebidas and math.dist(self.position, (-115,0,10)) < 69:
                self.provider.send_communication_command(SendMessageCommand("Red", 11))
                self.provider.schedule_timer("discard red", self.provider.current_time() + 3)
            if "Green" in self.recebidas and math.dist(self.position, (0,140,10)) < 69:
                self.provider.send_communication_command(SendMessageCommand("Green", 12))
                self.provider.schedule_timer("discard green", self.provider.current_time() + 3)
            self.provider.schedule_timer("broadcast", self.provider.current_time() + 1)
            
        if timer == "discard red":
            self.recebidas.discard("Red")
            self.vis.paint_node(self.provider.get_id(), (255,255,255))
        if timer == "discard green":
            self.recebidas.discard("Green")
            self.vis.paint_node(self.provider.get_id(), (255,255,255))
        if timer == "discard blue":
            self.recebidas.discard("Blue")
            self.vis.paint_node(self.provider.get_id(), (255,255,255))
        if timer == "discard yellow":
            self.recebidas.discard("Yellow")
            self.vis.paint_node(self.provider.get_id(), (255,255,255))

    def handle_packet(self, message: str):
        if message[-3] == "t":
            self.broadcast = json.loads(message)
            return
        self.data = json.loads(message)
        cor = self.data["message"]
        if cor in self.recebidas:
            return
        self.recebidas.add(cor)
        if cor == "Red":
            self.vis.paint_node(self.provider.get_id(), (255,0,0))
            if math.dist(self.broadcast["posicao"], (-115,0,10)) < math.dist(self.position, (-115,0,10)):
                self.provider.send_communication_command(SendMessageCommand(json.dumps(self.data), self.broadcast["id"]))
        if cor == "Green":
            self.vis.paint_node(self.provider.get_id(), (0,255,0))
            if math.dist(self.broadcast["posicao"], (0,140,10)) < math.dist(self.position, (0,140,10)):
                self.provider.send_communication_command(SendMessageCommand(json.dumps(self.data), self.broadcast["id"]))
        if cor == "Blue":
            self.vis.paint_node(self.provider.get_id(), (0,0,255))
            if math.dist(self.broadcast["posicao"], (115,0,10)) < math.dist(self.position, (115,0,10)):
                self.provider.send_communication_command(SendMessageCommand(json.dumps(self.data), self.broadcast["id"]))
        if cor == "Yellow":
            self.vis.paint_node(self.provider.get_id(), (255,255,0))
            if math.dist(self.broadcast["posicao"], (0,-140,10)) < math.dist(self.position, (0,-140,10)):
                self.provider.send_communication_command(SendMessageCommand(json.dumps(self.data), self.broadcast["id"]))

    def handle_telemetry(self, telemetry: Telemetry):
        self.position = telemetry.current_position

    def finish(self):
        pass
