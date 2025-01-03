from collections import deque
from copy import deepcopy
import sys

# Kommentare gleich, bis auf vorgenommene Änderungen

def binaryOfHex(hexNum):
    sevenSegmentConversion = {
        "0": 0x7E,
        "1": 0x30,
        "2": 0x6D,
        "3": 0x79,
        "4": 0x33,
        "5": 0x5B,
        "6": 0x5F,
        "7": 0x70,
        "8": 0x7F,
        "9": 0x7B,
        "a": 0x77,
        "b": 0x1F,
        "c": 0x4E,
        "d": 0x3D,
        "e": 0x4F,
        "f": 0x47
        }
    return str(bin(sevenSegmentConversion[hexNum]))[2:]

def segmentsInNum(hexNum):
	binaryNum = binaryOfHex(hexNum)
	return sum([int(x) for x in binaryNum])

segments = {}
for hexNum in range(16):
	segments[hexNum] = segmentsInNum(hex(hexNum)[2:])

binary = {}
for hexNum in range(16):
	binary[hexNum] = binaryOfHex(hex(hexNum)[2:])

class Digit:
	
	def __init__(self, value, digitNum):
		self.value = value
		self.originalSegments = segments[int(value, 16)]
		self.originalBinary = binary[int(value, 16)]
		self.digitNum = digitNum
		self.possibleChanges = {}

	def constructTable(self): 
		rangeStart = 0
		if self.digitNum == 1:
			rangeStart = int(self.value, 16)
		for hexNum in range(rangeStart, 16):

			segmentChange = segments[hexNum] -  self.originalSegments

			change = segmentChange
			self.possibleChanges[hexNum] = change

def constructSubTrees(hexNum): 

	subTreeObjects = []
	cnt = 1

	for digit in hexNum: 
		digitObject = Digit(digit, cnt)
		digitObject.constructTable()
		subTreeObjects.append(digitObject)
		cnt += 1

	return subTreeObjects

def depthFirstSearch(subTree, subTrees):

	started = {}
	none = []

	stack = deque()
	stack.append((subTree, 0, []))

	while stack: 
		nextObject = stack.pop()

		subTree = nextObject[0]

		if subTree == "":
			if nextObject[1] == 0:
				strArray = [hex(x)[2:] for x in nextObject[2]]
				string = "".join(strArray)
				return string
			continue

		attributesId = ",".join([str(x) for x in [nextObject[1], subTree.digitNum]])

		if len(stack) != 0:
			nextAttributesId = ",".join([str(x) for x in [stack[len(stack)-1][1], stack[len(stack)-1][0].digitNum]])

		if attributesId in started:
			for ele in started[attributesId]:
				none.append(ele)
			del started[attributesId]

		if attributesId in none:
			continue

		if len(stack) != 0:
			if nextAttributesId in started:
				started[nextAttributesId].append(attributesId)
			else:
				started[nextAttributesId] = [attributesId]

		if subTree.digitNum <= len(subTrees):
			for newSubTree in subTree.possibleChanges: 

				newSegmentChange = nextObject[1] + subTree.possibleChanges[newSubTree]
				if subTree.digitNum == len(subTrees):
					if newSegmentChange != 0:
						continue

				newChosenNumbers = nextObject[2] + [newSubTree]

				if subTree.digitNum <= len(subTrees)-1:
					newSubTreeToAdd = deepcopy(subTrees[subTree.digitNum])
					newSubTreeToAdd.value = newSubTree
					stack.append((newSubTreeToAdd, newSegmentChange, newChosenNumbers))
				else:
					stack.append(("", newSegmentChange, newChosenNumbers))

def getData(text): 
	lines = text.strip().split("\n")
	hexNum = lines[0].lower()
	return hexNum

if __name__ == "__main__":
    in_file_name = sys.argv[1] 
    with open(in_file_name, "r") as f:
        text = f.read()
    
    out_file_name = in_file_name.replace(".txt", "_out.txt")
    with open(out_file_name, "w", encoding="utf-8") as f:
        hexNum = getData(text)
        subTrees = constructSubTrees(hexNum) 
        solution = depthFirstSearch(subTrees[0], subTrees)
        f.write(solution) 
