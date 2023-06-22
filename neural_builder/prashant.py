"""
Functions from original minecraft models
code written by Prashant
"""
# import sys, os, re, json, argparse, random, nltk, torch, pickle, numpy as np, copy, git, csv
# from glob import glob
# from datetime import datetime
# from os.path import join, isdir
# import xml.etree.ElementTree as ET
# from torch.autograd import Variable
# from sklearn.model_selection import train_test_split as tt_split

import numpy as np
import re
import nltk
# from nltk.tokenize import wordpunct_tokenize

# bounds of the build region
x_min = -5
x_max = 5
y_min = 1
y_max = 9
z_min = -5
z_max = 5 # TODO: Obtain from other repo
x_range = x_max - x_min + 1
y_range = y_max - y_min + 1
z_range = z_max - z_min + 1


def get_perspective_coordinates(x, y, z, yaw, pitch):
	# construct vector
	v = np.matrix('{}; {}; {}'.format(x, y, z))

	# construct yaw rotation matrix
	theta_yaw = np.radians(-1 * yaw)
	c, s = np.cos(theta_yaw), np.sin(theta_yaw)
	R_yaw = np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(c, 0, -s, 0, 1, 0, s, 0, c))

	# multiply
	v_new = R_yaw * v

	# construct pitch rotation matrix
	theta_pitch = np.radians(pitch)
	c, s = np.cos(theta_pitch), np.sin(theta_pitch)
	R_pitch = np.matrix('{} {} {}; {} {} {}; {} {} {}'.format(1, 0, 0, 0, c, s, 0, -s, c))

	# multiply
	v_final = R_pitch * v_new
	x_final = v_final.item(0)
	y_final = v_final.item(1)
	z_final = v_final.item(2)
	return (x_final, y_final, z_final)

vf = np.vectorize(get_perspective_coordinates)

def get_perspective_coord_repr(builder_position):
	# print(builder_position)
	bx = builder_position["x"]
	by = builder_position["y"]
	bz = builder_position["z"]
	yaw = builder_position["yaw"]
	pitch = builder_position["pitch"]

	perspective_coords = np.zeros((3, x_range, y_range, z_range))
	for x in range(x_range):
		for y in range(y_range):
			for z in range(z_range):
				xm, ym, zm = x-bx, y-by, z-bz
				perspective_coords[0][x][y][z] = xm
				perspective_coords[1][x][y][z] = ym
				perspective_coords[2][x][y][z] = zm

    
	px, py, pz = vf(perspective_coords[0], perspective_coords[1], perspective_coords[2], yaw, pitch)
    
	return np.stack([px, py, pz])

class BuilderActionExample():
	def __init__(self, action, built_config, prev_config, action_history):
		self.action = action # of type BuilderAction or None
		self.built_config = built_config
		self.prev_config = prev_config
		self.action_history = action_history

	def is_action(self):
		return isinstance(self.action, BuilderAction)

	def is_stop_token(self):
		return self.action == None

	def __eq__(self, other):
		if not isinstance(other, BuilderActionExample):
			# don't attempt to compare against unrelated types
			return NotImplemented

		return self.action == other.action and self.built_config == other.built_config \
			and self.prev_config == other.prev_config and self.action_history == other.action_history
	
class BuilderAction():
    """ Class representing a builder's action. """
    def __init__(self, block_x, block_y, block_z, block_type,
        action_type, weight=None):
        """
        Args:
            block_x (int): x-coordinate of block involved in action.
            block_y (int): y-coordinate of block involved in action.
            block_z (int) z-coordinate of block involved in action.
            block_type (string): block type (i.e., color).
            action_type (string): either "pickup" or "putdown".
        """
        assert action_type in ["putdown", "pickup"]

        self.action_type = "placement" if action_type == "putdown" else "removal"  
        self.block = {
            "x": block_x,
            "y": block_y,
            "z": block_z,
            "type": block_type
        }
        self.weight = weight
	
    def get_action(self):
        return str(self.action_type)
	
    def get_coords(self):
        return((str(self.block["type"]), str(self.block["x"]), str(self.block["y"]), str(self.block["z"])))
        
    def print(self):
        print("action type: " + str(self.action_type))
        print("x: " + str(self.block["x"]))
        print("y: " + str(self.block["y"]))
        print("z: " + str(self.block["z"]))
        print("type: " + str(self.block["type"]))
        print("weight: " + str(self.weight))

    def __eq__(self, other):
        if not isinstance(other, BuilderAction):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.action_type == other.action_type and self.block == other.block \
            and self.weight == other.weight


def tokenize(utterance):
	#take out quotes -- added to handle errors with 
	#log matches
	utterance.replace('"', '')
	utterance = re.sub('"', '', utterance)

	tokens = utterance.split()
	fixed = ""

	modified_tokens = set()
	for token in tokens:
		original = token

		# fix *word
		if len(token) > 1 and token[0] == '*':
			token = '* '+token[1:]

		# fix word*
		elif len(token) > 1 and token[-1] == '*' and token[-2] != '*':
			token = token[:-1]+' *'

		# fix word..
		if len(token) > 2 and token[-3] is not '.' and ''.join(token[-2:]) == '..':
			token = token[:-2]+' ..'

		# split axb(xc) to a x b (x c)
		if len(token) > 2:
			m = re.match("([\s\S]*\d+)x(\d+[\s\S]*)", token)
			while m:
				token = m.groups()[0]+' x '+m.groups()[1]
				m = re.match("([\s\S]*\d+)x(\d+[\s\S]*)", token)

		if original != token:
			modified_tokens.add(original+' -> '+token)

		fixed += token+' '

	return nltk.tokenize.word_tokenize(fixed.strip()), modified_tokens