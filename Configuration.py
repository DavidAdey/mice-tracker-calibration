# -*- coding: utf-8 -*-

import Base
#import DataBase
import ROOT
import math

class ConfigurationReader:

        def __init__(self, campaign):

                #print "Reading" 
		self.campaign = campaign

        def loadData(self):
		pass
                #print "loading data"
		
	def loadSettings(self, runNumber):

		config = ConfigurationSettings()
		configFile = open(self.campaign.configFile,"r")
                fileLines = configFile.readlines()
                for line in fileLines:
			lineArray = line.rsplit(" ")
			#try:
			if (lineArray[0] != "!") and (int(lineArray[0]) == runNumber):
				#print "found run " + str(runNumber)
				runStr, biasStr, timeInjStr, discrimStr, timeCurStr, intWindowStr, tempStr, ledPeakLocsStr = lineArray
                        	bias = float(biasStr)
				vth = int(discrimStr)
				time = float(timeInjStr)
				intWidth = float(intWindowStr)
				config.addSettings(bias, vth, time, intWidth)
			#	if ((ledPeakLocsStr != "n\n") or (ledPeakLocsStr != "n")):
			#		peakFileName = "PeakLocations_" + ledPeakLocsStr + ".txt"
			#		peakReader = PeakLocationReader(peakFileName)
			#		peaks = peakReader.loadPeakLocations()
			#		config.addPeaks(peaks)				
			#elif (lineArray[0] != "!"):
			#	print "but didn't find " + str(runNumber)
			#else:
				#print "Failed if"
				#print lineArray
				##print lineArray[0]
				#print runNumber
			#	#returnConfig = config
		return config

"""
	def loadDBSettings(self, runNumber):
		dbManager = DataBase.DataBaseManager()
		bias = dbManager.getRunSetting(runNumber, "bias")
		vth = dbManager.getRunSetting(runNumber, "vth")
		time = 0 #dbManager.getRunSetting(runNumber, "")
		intWidth = 0
		configuration = ConfigurationSettings()
		configuration.addSettings(bias, vth, time, intWidth) 
		dbManager.disconnect()
		return configuration
"""
class ConfigurationSettings:


	def __init__(self):
		self.channelPeakLocations = []

	def addSettings(self, bias, vth, time, intWindow):

		self.bias = bias
		self.vTh = vth
		self.time = time
		self.integrationWindow = intWindow

	def addPeaks(self, peaks):
		self.channelPeakLocations = peaks	

	def getPeak(self, channel, peak):
		for peakLocation in self.channelPeakLocations:
			if (peakLocation.channel == channel):
				try:
					return peakLocation.peaks[peak]
				except:	
					return -1	
		return -1

	def getIntegrationWindow(self):
		return self.integrationWindow

	def getBias(self):
		return self.bias

	def getVTh(self):
		return self.vTh

	def getInjectTime(self):
		return self.time


class PeakLocation:
	def __init__(self, chan=-1, peaks=[]):
		self.channel = chan
		self.peaks = peaks


class PeakLocationReader:
	def __init__(self, file):
		file = file.replace("\n","")
		self.file = open(file,"r")


	def loadPeakLocations(self):
		peakLocations = []
		fileLines = self.file.readlines()
                for line in fileLines:
			peaks = [] 	
			lineArray = line.rsplit(" ")
			chanStr = ""
                        if (lineArray[0] != "!"):
				chanStr = lineArray[0]
				if (len(lineArray) > 1):
					#chanStr = lineArray[0]
					for peak in range(len(lineArray) - 1):
						peaks.append(float(lineArray[peak + 1]))	
				location = PeakLocation(int(chanStr),peaks)
				peakLocations.append(location)
		return peakLocations
