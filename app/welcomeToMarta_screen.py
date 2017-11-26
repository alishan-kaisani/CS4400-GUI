import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen
import login_screen
import manageCards_screen
import tripHistory_screen
import backend

qtCreatorFile = "ui/welcomeToMarta.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class WelcomeToMartaFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.manageCardsLabel.mousePressEvent = self.ManageCards
		self.endTripLabel.mousePressEvent= self.EndTrip
		self.startTripLabel.mousePressEvent= self.StartTrip
		self.viewTripHistoryButton.clicked.connect(self.ViewTripHistory)
		self.logOutButton.clicked.connect(self.LogOut)
		self.breezeCardBox.currentIndexChanged.connect(self.UpdateBreezeCard)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.manageCardsLabel.mousePressEvent = self.ManageCards
		self.endTripLabel.mousePressEvent = self.EndTrip
		self.startTripLabel.mousePressEvent= self.StartTrip
		self.viewTripHistoryButton.clicked.connect(self.ViewTripHistory)
		self.logOutButton.clicked.connect(self.LogOut)
		self.PopulateBreezeCards()
		self.breezeCardBox.currentIndexChanged.connect(self.UpdateBreezeCard)
	def PopulateBreezeCards(self): 
		#backend function that returns a list of breezecard numbers
		cardList = backend.GetAllBreezeCardsOfPassenger()

		if (type(cardList) != list):
			self.error = "Error in Populating Breeze Cards - backend gave bad data"
			self.OpenError()
			return

		newList = []
		for card in cardList: 
			card = str(card)
			card = card[0:4] + " " + card[4:8] + " " + card[8:12] + " " + card[12:16]
			newList.append(card)
		self.breezeCardBox.addItems(newList)
		#self.UpdateBreezeCard()
	def UpdateBreezeCard(self): 
		cur_breezeCard = self.breezeCardBox.currentText()
		cur_breezeCard = cur_breezeCard.replace(" ","")

		details = backend.TripHistorySingleBreezecard(cur_breezeCard)
		#details is tuple of form (breezecardNum,value,username, fare, StartTime,StartsAt,EndsAt)
		
		if len(details) == 0:
			#this query only returns empty when this card hasn't been involved in a trip
			startList = []
			endList = []
			station_list = backend.PrettifyViewStations()
			
			#Fill in Start at Values
			for station in station_list:
				#if isTrain
				if ViewSingleStation(station[1])[4]: 
					item = station[0] + " -T-  $" + str(round(station[2],2))
				else:
					item = station[0] + "-B-  $" + str(round(station[2],2))
				startList.append(item)
			self.startAtBox.addItems(startList)
			
			#Fill in End at Values
			for station in station_list:
				item = station[0]
				endList.append(item)
			self.endingAtBox.addItems(endList)

			self.tripLabel.setText("No Trip In Progress")

			val = backend.BreezeCardMoney(cur_breezeCard)
			val = round(val,2)
			self.balanceAmount.setText("$" + val)
		elif len(details) > 0:
			val = details[1]
			val = round(val,2)
			self.balanceAmount.setText("$" + val)
			if (details[6] == None):
				#They're in a trip so display trip start & disable startTrip
				station = backend.ViewSingleStation(StartsAt)
				stationName = station[0]
				item = stationName + round(details[3],2)
				self.startAtBox.addItem(item)
				self.startAtBox.enabled = False

				self.startTripLabel.enabled = False
				
				self.tripLabel.setText("Trip in Progress")

				#pass in IsTrain to get the right type of stations to view
				station_list = backend.ViewAllTypeStations(station[4])

				for station in station_list:
					newList = []
					newList.append(station[0]) #stationName
				self.endAtBox.addItems(newList)
	def StartTrip(self, event): 
		if PassengerInTrip():
			self.error = "Passenger In Trip"
			self.OpenError()
			return

		cur_breezeCard = self.breezeCardBox.currentText()
		cur_breezeCard = cur_breezeCard.replace(" ","")

		cur_station = self.startAtBox.currentText()
		pieces = cur_station.split('$') #will split into  pieces, last with fare as decimal - 'x.xx'
		station_fare = float(pieces[-1])
		pieces = cur_station.split('-')
		isTrain = True
		if pieces[1] == "B":
			isTrain = False

		if BreezeCardMoney(cur_breezeCard) < station_fare:
			self.error = "Insufficient Funds"
			self.OpenError()
			return

		backend.startTrip(cur_breezeCard,cur_station,isTrain)

		self.error = "StartTrip Function Not Defined Yet"
		self.OpenError()
	def EndTrip(self, event): 
		self.error = "EndTrip Function Not Defined Yet"
		self.OpenError()
	def ViewTripHistory(self):
		self.frame = tripHistory_screen.TripHistoryFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()	
	def ManageCards(self, event): 
		self.frame = manageCards_screen.ManageCardsFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
	def LogOut(self): 
		backend.Logout()
		self.frame = login_screen.LoginFrame()
		self.frame.InitFromOtherFile(Ui_Frame) 
		self.frame.show()
		self.hide()
		self.success = "Logged Out Successfully"
		self.OpenSuccess()
	def OpenError(self):
		self.newframe = error_screen.ErrorFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.error
		self.newframe.UpdateText()
		self.newframe.show()
	def OpenSuccess(self):
		self.newframe = success_screen.SuccessFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.success;
		self.newframe.UpdateText()
		self.newframe.show()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = WelcomeToMartaFrame()
	window.show()
	sys.exit(app.exec_())