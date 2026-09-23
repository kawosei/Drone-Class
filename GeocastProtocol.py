import json
import logging
import math

from gradysim.protocol.interface import IProtocol
from gradysim.protocol.messages.communication import SendMessageCommand, BroadcastMessageCommand
from gradysim.protocol.plugin.mission_mobility import MissionMobilityPlugin, MissionMobilityConfiguration, LoopMission
from gradysim.protocol.messages.telemetry import Telemetry
from gradysim.simulator.extension.visualization_controller import VisualizationController


class Drone(IProtocol):
    waypoints = {
        0: [(100,0,10), (0,0,10)],
        1: [(100,100,10), (100,0,10)],
        2: [(100,100,10), (0,100,10)],
        3: [(0,100,0)],
        4: [(0,100,10), (-100,100,10)],
        5: [(-100,0,10), (-100,100,10)],
        6: [(-100,0,10), (0,0,10)]
    }
    def initialize(self):
        self.recebidoRV = False
        self.recebidoDL = False
        self.enviouRV = False
        self.enviouDL = False
        self.voltouRV = False
        self.voltouDL = False
        self.mission = MissionMobilityPlugin(self, MissionMobilityConfiguration(speed=40, loop_mission=LoopMission.RESTART))
        self.mission.start_mission(self.waypoints[self.provider.get_id()])

        self.vis = VisualizationController(self)

        self.provider.schedule_timer("pintar 0",1)
        self.provider.schedule_timer("pintar 6",1)
        self.provider.schedule_timer("enviar", 2)

    def handle_timer(self, timer: str):
        if timer == "enviar":
            self.provider.send_communication_command(BroadcastMessageCommand(json.dumps({
                "id": self.provider.get_id(), "posicao": self.posicao})))
            self.provider.schedule_timer("enviar", self.provider.current_time()+1)
        if timer == "pintar 0":
            self.vis.paint_node(0, (255,0,0))
        if timer == "pintar 6":
            self.vis.paint_node(6, (0,255,0))
        if timer == "voltar RV":
            self.provider.send_communication_command(SendMessageCommand("Red Velvet b",4))
            self.vis.paint_node(4, (255,0,0))
            self.provider.schedule_timer("voltar RV", self.provider.current_time()+2)
        if timer == "voltar DL":
            self.provider.send_communication_command(SendMessageCommand("Doce de Leite b",2))
            self.vis.paint_node(2, (0,255,0))
            self.provider.schedule_timer("voltar DL", self.provider.current_time()+2)

    def handle_packet(self, message: str):
        if message.startswith("{"):
            if (self.provider.get_id() == 0 or self.recebidoRV) and not self.enviouRV:
                loc = json.loads(message)
                if math.dist(loc["posicao"],(0,100,0)) < math.dist(self.posicao,(0,100,0)):
                        self.enviouRV = True
                        self.provider.send_communication_command(SendMessageCommand("Red Velvet",loc["id"]))
                        self.vis.paint_node(loc["id"],(255,0,0))
            if (self.provider.get_id() == 6 or self.recebidoDL) and not self.enviouDL:
                loc = json.loads(message)
                if math.dist(loc["posicao"],(0,100,0)) < math.dist(self.posicao,(0,100,0)):
                        self.enviouDL = True
                        self.provider.send_communication_command(SendMessageCommand("Doce de Leite",loc["id"]))
                        self.vis.paint_node(loc["id"],(0,255,0))
            if self.voltouRV:
                loc = json.loads(message)
                if math.dist(loc["posicao"],(-50,0,0)) < math.dist(self.posicao,(-50,0,0)):
                    self.voltouRV = False
                    self.provider.send_communication_command(SendMessageCommand("Red Velvet b",loc["id"]))
                    self.vis.paint_node(loc["id"],(255,0,0))
            if self.voltouDL:
                loc = json.loads(message)
                if math.dist(loc["posicao"],(50,0,0)) < math.dist(self.posicao,(50,0,0)):
                    self.voltouDL = False
                    self.provider.send_communication_command(SendMessageCommand("Doce de Leite b",loc["id"]))
                    self.vis.paint_node(loc["id"],(0,255,0))
        else:
            if message == "Red Velvet":
                self.recebidoRV = True
            if message == "Doce de Leite":
                self.recebidoDL = True

        if not self.provider.get_id() == 3 and message == "Red Velvet b":
            self.provider.send_communication_command(BroadcastMessageCommand("RV recebido"))
            self.voltouRV = True
        if not self.provider.get_id() == 3 and message == "Doce de Leite b":
            self.provider.send_communication_command(BroadcastMessageCommand("DL recebido"))
            self.voltouDL = True

        if self.provider.get_id() == 3:
            if message == "Red Velvet" and not self.voltouRV:
                self.voltouRV = True
                self.provider.schedule_timer("voltar RV",self.provider.current_time()+2)
                self.vis.paint_node(3,(0,0,255))
            if message == "Doce de Leite" and not self.voltouDL:
                self.voltouDL = True
                self.provider.schedule_timer("voltar DL",self.provider.current_time()+2)
                self.vis.paint_node(3,(0,0,255))

            
        if self.provider.get_id() == 3:
            if message == "RV recebido":
                self.provider.cancel_timer("voltar RV")
            if message == "DL recebido":
                self.provider.cancel_timer("voltar DL")
            
        if self.provider.get_id() == 3 and message in ("Red Velvet", "Doce de Leite"):
             logging.info("Mensagem recebida")

    def handle_telemetry(self, telemetry):
        self.posicao = telemetry.current_position

    def finish(self):
        pass
