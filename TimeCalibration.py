
import math
import ROOT
import Base
import Configuration
import Globals

from array import array
from datetime import date


def solveLine(slope, offset, y):
	return (y - offset)/slope

class ChannelTDC:

	def __init__(self):

		print "Calib"
		self.board = -1
		self.bank = -1
		self.channel = -1
		self.injectTimes = array("d")
		self.iBTs = array("d") # Array for the level of current on the TAC - affects TDC slope
		self.tdcPeaks = array("d")
		self.numPoints = 0

	def setLocation(self, board, bank, channel):

		self.board = board
		self.bank = bank
		self.channel = channel

	def addChannel(self, channel, time, ibt=0):

		fitInfo = self.fitTdcPeak(channel)
		self.addTdcPeak(time, fitInfo)
		self.iBTs.append(ibt)

	def fitTdcPeak(self, channel):

		spectrum = ROOT.TSpectrum()
		numFoundPeaks = spectrum.Search(channel.tdcHist,2,"", 0.01 )
		if (numFoundPeaks == 1):
			peaks = spectrum.GetPositionX()
			tdcPeak = peaks[0]
			return tdcPeak
		else:
			print "More or less than one peak found - defaulting to TDC mean"
			tdcPeak = channel.tdcHist.GetMean()
			return tdcPeak

	def addTdcPeak(self, injectTDC, peak):

		self.numPoints += 1
		self.injectTimes.append(injectTDC)
		self.tdcPeaks.append(peak)

	def makeSaturationGraph(self):

		saturated = 0
		tdcs = array('f')
		ibts = array('f')
		for peak in range(len(self.tdcPeaks)):
			if (self.tdcPeaks[peak] < 255):
				tdcs.append(self.tdcPeaks[peak]
				ibts.append(self.iBTs[peak]
			else:
				saturated += 1
		
		self.saturationGraph = ROOT.TGraph(len(ibts), ibts, tdcs)

	def makeGraph(self):

		try:
			self.graph = ROOT.TGraph(self.numPoints, self.injectTimes, self.tdcPeaks)
			name = str(self.board) + "-" + str(self.bank) + "-" + str(self.channel) + "-TDCGraph" 
			self.graph.SetName(name)
			self.graph.Write()
		except:
			try:
				print self.numPoints
			except:
				print "bad num points"
			try:
				print len(self.injectTimes)
			except:
				print "bad inject times"
			try:
				print len(self.tdcPeaks)
			except:
				print "bad peaks"


class TimeCalibrator:

	def __init__(self):

		print "Galifray? Meh."
		self.chanTDCs = []
		self.ibtCalibration = CalibrationTypes.IBTCalibration()

	def setup(self):

		for board in range(Globals.BOARDS):
			for bank in range(Globals.BANKS):
				for channel in range(Globals.CHANNELS):
					chanTDC = ChannelTDC()
					chanTDC.setLocation(board, bank, channel)
					self.chanTDCs.append(chanTDC)

	def loadDataCampaign(self, campaign):

		self.dataCampaign = campaign
                configuration = Configuration.ConfigurationReader(campaign)
		i = 0
                for run in self.dataCampaign.runs:
                        print "Looking at run " + str(run.runNumber)
                        settings = configuration.loadSettings(run.runNumber)
                        injectTDC = (settings.getIntegrationWindow() - settings.getInjectTDC())
			run.setup()
			readeri = Base.DATEReader(self.dataCampaign.fileNames[i])
			print "Starting to analyse file:"
                        print self.dataCampaign.fileNames[i]
                        readeri.readBinary(run)

			for channel in run.channelRuns:
				uniqueId = channel.uniqueChan
				self.chanTDCs[uniqueId].addChannel(channel, injectTDC)
			i += 1

	def findIBTLimits(self):

		for timeCircuit in self.chanTDCs:
			timeCircuit.makeSaturationGraph()
			timeCircuit.saturationGraph.Fit("pol1")
			fit = timeCircuit.saturationGraph.GetFunction("pol1")	
			slope = fit.GetParameter(1)
			offset = fit.GetParameter(0)
			saturated = timeCircuit.numSaturatedPoints
			limit = solveLine(slope, offset, 255,0)
			self.findTriptObject(timeCircuit.board, timeCircuit.bank, timeCircuit.channel).addIBTLimit(limit)
			
	def findIBTCalibration(self):

		for tript in self.triptObjects:
			ibt = tript.getOptimumIBT()
			self.ibtCalibration.addIBTValue(tript.board, tript.module, tript.tript, ibt)

	def writeIBTCalibration(self):

		dbManager = DataBase.DataBaseManager()
		dbManager.writeIBTCalibration(self.ibtCalibration)

	def findTDCCalibration(self):

		today = date.today()
		self.calibFile = open("TDC-Calib.txt","w")
		for timeCircuit in self.chanTDCs:
			timeCircuit.makeGraph()
			timeCircuit.graph.Fit("pol1")
			fit = timeCircuit.graph.GetFunction("pol1")
			slope = fit.GetParameter(1)
			pedestal = fit.GetParameter(0)
			self.calibration.addTDCEntry(timeCircuit.board, timeCircuit.bank, timeCircuit.channel, pedestal, slope)
			#string = str(timeCircuit.board) + " " + str(timeCircuit.bank) + " " + str(timeCircuit.channel) + " "
			#string += str(pedestal) + " " + str(slope) + "\n"
			#self.calibFile.write(string)


	def findTriptObject(self, board, bank, channel):

		for object in self.triptObjects:
			module = (bank*2) + (channel/Globals.MODULECHANNELS)
			tript = ((channel+1) / Globals.TRIPCHANNELS) % Globals.MODULETRIPS
			if (board == object.board and module == object.module and tript == object.tript):
				return object

class TriPtObject(object):

	def __init__(self, board, bank, channel):

		self.limits = []
		self.board = board
		self.module = (bank*2) + (channel/Globals.MODULECHANNELS)
		self.tripId = ((channel+1) / Globals.TRIPCHANNELS) % Globals.MODULETRIPS
		
	def addIBTLimit(self, limit):

		self.limits.append(limit)

	def findOptimumIBT(self):

		self.limits.sort()
		return self.limits[0]	
