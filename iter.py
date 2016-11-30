import mido_encodage as me
import os

def scanDir(directory=".",midiSample=[]):
	print("Sanning "+directory)
	for file in os.listdir(directory):
		if os.path.isdir(directory+"/"+file):
			scanDir(directory+"/"+file,midiSample)
		else:
			addMidiToList(directory+"/"+file,midiSample)
	print("Scanned "+directory)
	return midiSample

def addMidiToList(midiFile,midiList):
	print("Adding "+midiFile)
	try:
		channels,metas=me.parseMidi(midiFile)
		for channel in channels:
			midiList.append(channel)
	except:
		os.remove(midiFile)
		print(midiFile+" REMOVED")


if __name__ == "__main__":
	print("Scan a directory and add every channel of every MIDI file of this directory and its sub-directories to a list.")