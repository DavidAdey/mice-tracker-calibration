#import MessageHandler

PATH = "./" 						# The location of the data files
BOARDS = 16						# Number of AFE boards to calibrate
BANKS = 4						# Number of DFPGAs in AFE
CHANNELS = 128						# Number of channels per DFPGA
MODULECHANNELS = 64					# Number of channels per AFPGA
TRIPCHANNELS = 32					# Number of channels per TriPt
MODULETRIPS = 2						# Number of TripTs per AFPGA
ADCRANGE = 0xFF						# 8bit range of ADCs
MIN_BIAS = 6.0						# Minimum allowed bias
MAX_BIAS = 8.0						# Maximum allowed bias
MAX_VTH = 255						# Maximum VTh
MIN_VTH = 0						# Minimum VTh
CASSETTES = [101, 102, 103, 104, 107, 109, 110, 111]	# Cassette IDs
#MESSAGE = MessageHandler.MessageHandler()		# Single message handler
