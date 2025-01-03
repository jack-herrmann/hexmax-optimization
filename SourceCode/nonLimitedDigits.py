from collections import deque
from copy import deepcopy
import sys

# Kommentare prinzipiell gleich zum Original, außer an explizit kommentierten Stellen


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

			xorDiff = bin(int(binary[hexNum], 2) ^ int(self.originalBinary, 2))[2:]
			sumAcross = sum([int(x) for x in xorDiff])
			swapChange = (sumAcross + segmentChange) / 2

			change = (segmentChange, swapChange)
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

def depthFirstSearch(subTree, subTrees, swaps):

	currentBest = (1, "") # Variable, um die aktuell beste Möglichkeit mit der höchsten Zahl an "verlegten" Segmenten

	started = {}
	none = []

	stack = deque()
	stack.append((subTree, (0, 0), []))

	while stack: 
		nextObject = stack.pop()

		subTree = nextObject[0]

		if subTree == "": # Ermittlung und Aktualisierung der currentBestvariable ...
			maybe = 0
			if nextObject[1][0] < 0:
				maybe = abs(nextObject[1][0])
			if nextObject[1][0] != -1 and (nextObject[1][1] + maybe) <= swaps:

				if currentBest[0] > nextObject[1][0]:
					strArray = [hex(x)[2:] for x in nextObject[2]]
					string = "".join(strArray)
					currentBest = (nextObject[1][0], string)
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

				newSegmentChange = nextObject[1][0] + subTree.possibleChanges[newSubTree][0]

				newSwapChange = nextObject[1][1] + subTree.possibleChanges[newSubTree][1]
				if newSwapChange > swaps:
					continue

				newChosenNumbers = nextObject[2] + [newSubTree]

				if subTree.digitNum <= len(subTrees)-1:
					newSubTreeToAdd = deepcopy(subTrees[subTree.digitNum])
					newSubTreeToAdd.value = newSubTree
					stack.append((newSubTreeToAdd, (newSegmentChange, newSwapChange), newChosenNumbers))
				else:
					stack.append(("", (newSegmentChange, newSwapChange), newChosenNumbers))

	return currentBest

def getData(text):
	lines = text.strip().split("\n")
	hexNum = lines[0].lower()
	swaps = int(lines[1])
	return hexNum, swaps

if __name__ == "__main__":
    in_file_name = sys.argv[1]
    with open(in_file_name, "r") as f:
        text = f.read()
    
    out_file_name = in_file_name.replace(".txt", "_out.txt")
    with open(out_file_name, "w", encoding="utf-8") as f:
        hexNum, swaps = getData(text)
        subTrees = constructSubTrees(hexNum)
        currentBest = depthFirstSearch(subTrees[0], subTrees, swaps)

        if abs(currentBest[0]) % 2 == 0: # Verwendung der Entfernten Segmente, um Ziffern zu ergänzen
			sol = "".join(["1" for _ in range(int(abs(currentBest[0]) / 2))]) + currentBest[1]
		else:
			sol = "7" + "".join(["1" for _ in range(int((abs(currentBest[0]) - 3) / 2))]) + currentBest[1]

        f.write(sol) 
