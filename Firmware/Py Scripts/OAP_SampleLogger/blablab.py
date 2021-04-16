from Mesh_DataStructures import MeshNetwork
from Mesh_DataStructures import Mote

readLog = open('spoofed sampleLog.log', 'r')
Mesh = MeshNetwork()
Mesh.loadMesh(readLog)

plot (Mesh.Motes[3].temp, Mesh.Motes[3].timestr)