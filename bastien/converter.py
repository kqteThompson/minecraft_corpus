from typing import List

class Position:
  def __init__(self, X, Y, Z, Yaw, Pitch):
    self.X = X
    self.Y = Y
    self.Z = Z
    self.Yaw = Yaw
    self.Pitch = Pitch
    
class BlockData: 
  def __init__(self, X, Y, Z, Type, Colour):
    self.X = X
    self.Y = Y
    self.Z = Z
    self.Type = Type
    self.Colour = Colour
    
class ScreenshotData: 
	def __init__(self, Path, Timestamp):
		self.Path = Path
		self.Timestamp = Timestamp

class WorldState:
  def __init__(self, architect_Position: Position, builder_Position: Position, ChatHistory: List[str], Timestamp: str, blocksInGrid: List[BlockData], Screenshots: ScreenshotData):
    self.architect_Position = architect_Position
    self.builder_Position = builder_Position
    self.ChatHistory = ChatHistory
    self.Timestamp = Timestamp
    self.blocksInGrid = blocksInGrid
    self.Screenshots = Screenshots

class Observation:
  def __init__(self, WorldStates: List[WorldState]):
    self.WorldStates = WorldStates

import json
import os
import sys

if len(sys.argv) <= 1:
	print("arguments should be \"python3 converter.py [path/to/file.json]\"") 
else:
	fn = sys.argv[1]
	if os.path.exists(fn):
		file1 = open(fn)
		x = json.loads(file1.read())
		file1.close()
		observation = Observation(**x)
		for i in range(len(observation.WorldStates)):
			worldState = WorldState(None, None, None, None, None, None)
			worldState.architect_Position = Position(**observation.WorldStates[i]["architect_Position"])
			worldState.builder_Position = Position(**observation.WorldStates[i]["builder_Position"])
			worldState.ChatHistory = observation.WorldStates[i]["ChatHistory"]
			worldState.Timestamp = observation.WorldStates[i]["Timestamp"]
			worldState.blocksInGrid = []
			for block in observation.WorldStates[i]["BlocksInGrid"]:
				worldState.blocksInGrid.append(BlockData(**block))
			worldState.Screenshots = ScreenshotData(**observation.WorldStates[i]["Screenshots"])
			observation.WorldStates[i] = worldState

		i = 1
		BUILDER_NAME = "Builder_B1"
		ARCHITECT_NAME = "Architect_A1"
		textFile = f"0 : {BUILDER_NAME} : Mission has started .\n"
		lastChat = [textFile]
		lastBlocksState = []
		for world in observation.WorldStates:
			if len(world.ChatHistory) > len(lastChat):
				lastChat = world.ChatHistory
				text = world.ChatHistory[-1].replace("<architect> ", f"{ARCHITECT_NAME} : ").replace("<builder> ", f"{BUILDER_NAME} : ")
				textFile = textFile + f"{i} : {text}\n"
				i = i + 1
    
			if len(world.blocksInGrid) != len(lastBlocksState):
				if len(world.blocksInGrid) < len(lastBlocksState):
					elements_retires = set(lastBlocksState) - set(world.blocksInGrid)
					for element in elements_retires:
						textFile = textFile + f"{i} : [Builder picks up a {element.Colour.lower()} block at X:{element.X} Y:{element.Y} Z:{element.Z}]\n"
				if len(world.blocksInGrid) > len(lastBlocksState):
					elements_ajoutes = set(world.blocksInGrid) - set(lastBlocksState)
					for element in elements_ajoutes:
						textFile = textFile + f"{i} : [Builder puts down a {element.Colour.lower()} block at X:{element.X} Y:{element.Y} Z:{element.Z}]\n"
				lastBlocksState = world.blocksInGrid
				i = i + 1

		f = open(sys.argv[1].replace('.json', "_simplified.txt"), "x")
		f.write(textFile)
		f.close()