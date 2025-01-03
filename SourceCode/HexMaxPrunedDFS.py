from collections import deque # Modul, für die Nutzung des erweiterten Datentyp deque
from copy import deepcopy # Modul, für das Kopieren von Objekte und Listen ohne Referenzen
import sys # Modul, für den Zugriff auf das Terminal

def binaryOfHex(hexNum): # Funktion, zur Bestimmung der binären Siebensegmentkodierung einer Hexzahl
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

def segmentsInNum(hexNum): # Funktion, zur Bestimmung der verwendeten Segmente in der Siebensegmentdarstellung einer Hexzahl
	binaryNum = binaryOfHex(hexNum)
	return sum([int(x) for x in binaryNum])

segments = {} # hashmap, zum Nachschlagen der verwendeten Segmente
for hexNum in range(16):
	segments[hexNum] = segmentsInNum(hex(hexNum)[2:])

binary = {}
for hexNum in range(16): # hashmap, zum Nachschlagen der Binärkodierung
	binary[hexNum] = binaryOfHex(hex(hexNum)[2:])

class Digit: # Klassen, zum Abbilden einer einzelnen Ziffer
	
	def __init__(self, value, digitNum): # Definition der Attribute einer Ziffer
		self.value = value # Zahlenwert
		self.originalSegments = segments[int(value, 16)] # verwendete Segmente
		self.originalBinary = binary[int(value, 16)] # Binärkodierung
		self.digitNum = digitNum # Stelle der Ziffer in der Zahl
		self.possibleChanges = {} # hashmap, zum Nachschlagen möglicher Änderungen dieser Ziffer und deren Segmentzahländerungen und Umlegungen
		self.bestPossibleList = {} # hashmap, zur Darstellung der minimalen Umlegungen nötig, um eine Segmentzahländerung zu erreichen, bei noch n - digitNum übrigen Ziffern

	def constructTable(self): # Funktion, zur Erstellung der possibleChanges hashmap
		rangeStart = 0
		if self.digitNum == 1:
			rangeStart = int(self.value, 16)
		for hexNum in range(rangeStart, 16): # Iteration über alle Hexzahl (0 bis 15)

			segmentChange = segments[hexNum] -  self.originalSegments

			xorDiff = bin(int(binary[hexNum], 2) ^ int(self.originalBinary, 2))[2:]
			sumAcross = sum([int(x) for x in xorDiff])
			swapChange = (sumAcross + segmentChange) / 2

			change = (segmentChange, swapChange)
			self.possibleChanges[hexNum] = change

def constructSubTrees(hexNum): # Funktion, zur Erstellung der Objekte pro Ziffer

	subTreeObjects = []
	cnt = 1

	for digit in hexNum: # Iteration über alle Ziffern der Eingabezahl
		digitObject = Digit(digit, cnt)
		digitObject.constructTable()
		subTreeObjects.append(digitObject)
		cnt += 1

	return subTreeObjects

def constructLists(subTrees): # Funktion, zur Erstellung der bestPossibleList hashmap
	bestSoFar = {}
	for subTree in subTrees[::-1]: # Iteration über alle erstellten Ziffernobjekte, um diese zu aktualisieren
		best = {}
		for changes in subTree.possibleChanges.values(): # Iteration über alle möglichen Änderungen einer Ziffer, um Minimen zu ermitteln
			if changes[0] in best:
				if changes[1] < best[changes[0]]:
					best[changes[0]] = changes[1]
			else:
				best[changes[0]] = changes[1]
		tempBestSoFar = {}
		for segChange in best: # Iteration über die hashmap zur Darstellung der minimalen Umlegungen nötig, um eine Segmentzahländerung zu erreichen, bei dieser Ziffer
			if bestSoFar != {}:
				for otherSegChange in bestSoFar: # Iteration über die hashmap zur Darstellung der minimalen Umlegungen nötig, um eine Segmentzahländerung zu erreichen, bei den in der Eingabezahl noch nachfolgenden Ziffern zusammen, wird aktualisiert, um die jetzige Ziffer zu beinhalten
					if segChange + otherSegChange in tempBestSoFar:
						if best[segChange] + bestSoFar[otherSegChange] < tempBestSoFar[segChange+otherSegChange]:
							tempBestSoFar[segChange+otherSegChange] = best[segChange] + bestSoFar[otherSegChange]
					else:
						tempBestSoFar[segChange+otherSegChange] = best[segChange] + bestSoFar[otherSegChange]
			else:
				bestSoFar = best
		bestSoFar = tempBestSoFar
		tempBestSoFar = {}
		subTree.bestPossibleList = bestSoFar
	return subTrees # Rückgabe der aktualisierten Ziffernobjekte

def depthFirstSearch(subTree, subTrees, swaps): # Funktion zum Ausführen einer Tiefensuche auf dynamisch erzeugten Bäumen

	started = {}
	none = []

	stack = deque()
	stack.append((subTree, (0, 0), []))

	while stack: # Iteration über den sich ständig verändernden Callstack
		nextObject = stack.pop()

		subTree = nextObject[0]

		if subTree == "": # Prüfung, ob noch Ziffern übrig sind
			if nextObject[1][0] == 0 and nextObject[1][1] <= swaps: # Prüfung, ob die Lösung valide ist
				strArray = [hex(x)[2:] for x in nextObject[2]]
				string = "".join(strArray)
				return string
			continue

		attributesId = ",".join([str(x) for x in [nextObject[1], subTree.digitNum]]) # Erstellung einer eindeutigen Identifikation dieser Stelle im Baum, um eine Memoization dieser iterativen Lösung zu ermöglichen

		if len(stack) != 0:
			nextAttributesId = ",".join([str(x) for x in [stack[len(stack)-1][1], stack[len(stack)-1][0].digitNum]]) # Erstellung einer eindeutigen Identifikation des derzeitig nachfolgenden Elements im Callsatck, auch um Memoisation zu ermöglichen

		if attributesId in started: # Prüfung, ob der ein vorher begonnener Teilbaum bereits vollständig "umrundet" wurde, ohne Lösung
			for ele in started[attributesId]:
				none.append(ele)
			del started[attributesId]

		if attributesId in none: # Verwendung der Memoisation, Abbrechung wenn bekannt ist, dass dieser Pfad zu keinem Ergebnis führt
			continue

		if len(stack) != 0: # Prüfung, ob auch eine Memoisation dieses Teilbaums noch möglich ist
			if nextAttributesId in started:
				started[nextAttributesId].append(attributesId)
			else:
				started[nextAttributesId] = [attributesId]

		if subTree.digitNum <= len(subTrees): # Prüfung, ob dieser Pfad noch weiter geht
			for newSubTree in subTree.possibleChanges: # Erstellung neuer Callsatckelemente für jede weitere Änderungsmöglichkeit, mit Prüfungen, ob diese zu validen Ergebnissen führen könnten

				newSegmentChange = nextObject[1][0] + subTree.possibleChanges[newSubTree][0]
				if subTree.digitNum == len(subTrees):
					if newSegmentChange != 0:
						continue

				newSwapChange = nextObject[1][1] + subTree.possibleChanges[newSubTree][1]
				if newSwapChange > swaps:
					continue
				if newSwapChange == swaps and newSegmentChange != 0:
					continue

				if -1 * newSegmentChange not in subTree.bestPossibleList:
					continue
				else:
					if newSwapChange + subTree.bestPossibleList[-1 * newSegmentChange] > swaps:
						continue

				newChosenNumbers = nextObject[2] + [newSubTree]

				if subTree.digitNum <= len(subTrees)-1:
					newSubTreeToAdd = deepcopy(subTrees[subTree.digitNum])
					newSubTreeToAdd.value = newSubTree
					stack.append((newSubTreeToAdd, (newSegmentChange, newSwapChange), newChosenNumbers))
				else:
					stack.append(("", (newSegmentChange, newSwapChange), newChosenNumbers))

def display(num): # Funktion, zur Abbildung einer binäre Siebensegmentkodierung
	start = 0
	end = 7
	parts = []
	rangeEnd = len(num)/7
	for _ in range(int(rangeEnd)):
		parts.append(num[start:end])
		start += 7
		end += 7
	for digit in parts:
		print("\n")
		if digit[0] == "1":
			print("---")
		if digit[5] == "1":
			print("| ", end="")
		else:
			print("  ", end="")
		if digit[1] == "1":
			print("|", end="")
		if digit[6] == "1":
			print("\n---")
		else:
			print("\n")
		if digit[4] == "1":
			print("| ", end="")
		else:
			print("  ", end="")
		if digit[2] == "1":
			print("|", end="")
		if digit[3] == "1":
			print("\n---")
	print("\n")
	print("\n======")

def elaborateConversion(frm, to): # Funktion, zur Abbildung des Übergangs von Eingabezahl zur Ausgabezahl
	changingNum = ""
	str1 = ""
	str2 = ""
	for idx, digits in enumerate(zip(frm, to)):
		bin1 = binaryOfHex(digits[0])
		while len(bin1) != 7:
			bin1 = "0" + bin1
		bin2 = binaryOfHex(digits[1])
		while len(bin2) != 7:
			bin2 = "0" + bin2
		str1 += bin1
		str2 += bin2
	display(str1)
	changingNum = str1

	for idx in range(len(changingNum)):
		digitsInBin = (changingNum[idx], str2[idx])
		if digitsInBin[0] != digitsInBin[1]:
	
			changingNum = list(changingNum)
			changingNum[idx] = digitsInBin[1]
			changingNum = "".join(changingNum)

			for idx2, digit in enumerate(changingNum):
				if idx2 > idx:
					if digit == digitsInBin[1] and str2[idx2] != digitsInBin[1]:
						changingNum = list(changingNum)
						changingNum[idx2] = digitsInBin[0]
						changingNum = "".join(changingNum)
						break
			display(changingNum)


def getData(text): # Funktion, zur sinnvollen Speicherung des Datensatzes in Variablen
	lines = text.strip().split("\n")
	hexNum = lines[0].lower()
	swaps = int(lines[1])
	return hexNum, swaps

if __name__ == "__main__":
    in_file_name = sys.argv[1] # Datei einlesen
    with open(in_file_name, "r") as f:
        text = f.read()
    
    out_file_name = in_file_name.replace(".txt", "_out.txt") # Ergebnis in Outputdatei schreiben
    with open(out_file_name, "w", encoding="utf-8") as f:
        hexNum, swaps = getData(text)
        subTrees = constructSubTrees(hexNum) # Aufrufen der entsprechenden Lösungsfunktionen ...
        subTrees = constructLists(subTrees)
        solution = depthFirstSearch(subTrees[0], subTrees, swaps)
        f.write(solution) 
        elaborateConversion(hexNum, solution)
