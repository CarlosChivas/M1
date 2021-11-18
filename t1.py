#Model design
import agentpy as ap

#Visualization
import matplotlib.pyplot as plt
import time
#import seaborn as sns
#import IPython

moves = 0
start_time = 0
end_time = 0
class ForestModel(ap.Model):
    def setup(self):
        
        #Create agents(trees)
        n_dirty = int(self.p['sucias'] * (self.p.size[0] * self.p.size[1]))
        #trees = self.agents = ap.AgentList(self, n_trees)
        dirty =  ap.AgentList(self, n_dirty)
        robots = ap.AgentList(self, self.p.agents)
        robots.condition = 0
        dirty.condition = 1

        #Create grid
        self.forest = ap.Grid(self, [self.p.size[1], self.p.size[0]], track_empty=True)
        agentsPositions = [(1,1)]*(self.p.agents)
        self.forest.add_agents(dirty, random=True, empty=True)
        self.forest.add_agents(robots, positions=agentsPositions,random=False)

        self.agents = dirty + robots

        #Condition 0: Robot, 1: Dirty, 2: Cleaned

        global start_time
        start_time = time.time()
    def step(self):
        global moves

        cochinas = self.agents.select(self.agents.condition == 1)
        robots = self.agents.select(self.agents.condition == 0)
        max = self.p['time']

        for robot in robots:
            neighborList = self.forest.neighbors(robot).to_list()
            neighbor = self.random.choice(neighborList)
            if((time.time() - start_time)>=max):
                self.stop()
            #if(moves>=max):
             #   self.stop()
            if neighbor.condition != 0:
                newPosRobot = self.forest.positions[neighbor] 
                self.forest.move_to(robot, newPosRobot)
                neighbor.condition = 2
                moves += 1

        #Stop simulation if no fire is left
        if len(cochinas) == 0:
            self.stop()
    
    def end(self):
        global moves
        global end_time
        end_time = time.time()
        #Document a measure at the end of the simulation
        dirty_rooms= len(self.agents.select(self.agents.condition == 1))
        total_cells = (self.p.size[0] * self.p.size[1])
        used_time = end_time-start_time
        self.report('clean_rooms', 
                    (total_cells - dirty_rooms) / total_cells)
        self.report('movements', moves)
        self.report('time', used_time)



print("Ingresa el tamaño de grid para las celdas\nLargo: ")
largo:int = input()
print("Ancho: ")
ancho:int = input()
print("Numero de agentes: ")
numAgents:int = input()
print("Porcentaje de celdas incialmente sucias (ej 0.7): ")
celdasSucias = input()
print("Tiempo maximo de ejecucion: ")
tiempoEjecucion:int = input()

#Define parameters
parameters = {
    'sucias': float(celdasSucias), #Percentage of grid covered by trees
    'size': (int(largo), int(ancho)), #Height and length of the grid
    'time': int(tiempoEjecucion),#500,
    'agents': int(numAgents),
}

sample =ap.Sample(parameters, n=10)
exp = ap.Experiment(ForestModel, sample)
results = exp.run()
print("\nTiempo usado: " + str(results.reporters['time'][0]) + " seg")
print("Movimientos realizados: " + str(results.reporters['movements'][0]))
print("Porcentaje de habitaciones limpias: " + str(results.reporters['clean_rooms'][0]*100) + "%")
