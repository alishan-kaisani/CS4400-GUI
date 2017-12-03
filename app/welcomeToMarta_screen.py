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
		self.refreshButton.clicked.connect(self.Refresh)
		self.PopulateBreezeCards()
		self.breezeCardBox.currentIndexChanged.connect(self.UpdateBreezeCard)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.manageCardsLabel.mousePressEvent = self.ManageCards
		self.endTripLabel.mousePressEvent = self.EndTrip
		self.startTripLabel.mousePressEvent= self.StartTrip
		self.viewTripHistoryButton.clicked.connect(self.ViewTripHistory)
		self.logOutButton.clicked.connect(self.LogOut)
		self.refreshButton.clicked.connect(self.Refresh)
		self.PopulateBreezeCards()
		self.breezeCardBox.currentIndexChanged.connect(self.UpdateBreezeCard)
	def Refresh(self):
		self.UpdateView();
		return
	def UpdateView(self):
		self.hide()
		self.UpdateBreezeCard()
		self.show()
		return
	def PopulateBreezeCards(self): 
		#backend function that returns a list of breezecard numbers
		cardList = backend.GetAllBreezeCardsOfPassenger()
		self.breezeCardBox.clear()

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
		self.UpdateBreezeCard()
	def UpdateBreezeCard(self): 
		cur_breezeCard = self.breezeCardBox.currentText()
		cur_breezeCard = cur_breezeCard.replace(" ","")

		if backend.IsSuspended(cur_breezeCard):
			self.balanceAmount.setText("Card Suspended")
			self.endingAtBox.setEnabled(False)
			self.startAtBox.setEnabled(False)
			self.startTripLabel.setStyleSheet("color:red")
			self.endTripLabel.setStyleSheet("color:red")
			self.tripLabel.setStyleSheet("color:red")
			self.tripLabel.setText("Suspended card can't start trip")
			return

		val = backend.BreezeCardMoney(cur_breezeCard)
		self.balanceAmount.setText('$ {:0.2f}'.format(val))

		if backend.PassengerInTrip():
			if cur_breezeCard != backend.BreezecardForTrip():
				print('bad')
				self.endingAtBox.setEnabled(False)
				self.startAtBox.setEnabled(False)
				self.startTripLabel.setStyleSheet("color:red")
				self.endTripLabel.setStyleSheet("color:red")
				self.tripLabel.setStyleSheet("color:red")
				self.tripLabel.setText("Trip in Progress")
				return

		self.startAtBox.clear()
		self.endingAtBox.clear()

		details = backend.TripHistorySingleBreezecard(cur_breezeCard)
		#details is tuple of form (breezecardNum,value,username, fare, StartTime,StartsAt,EndsAt)
		
		if not backend.PassengerInTrip():
			#this occurs when the passenger is not in a trip
			startList = []
			endList = []
			station_list = backend.PrettifyViewStations()
			
			#Fill in Start at Values
			for station in station_list:
				item = ('{} - {} - ${:0.2f}'.format(station[1],station[0],station[2]))
				startList.append(item)
			self.startAtBox.addItems(startList)
			
			#Fill in End at Values
			for station in station_list:
				item = ('{} - {}'.format(station[1],station[0]))
				endList.append(item)
			self.endingAtBox.addItems(endList)

			self.startAtBox.setEnabled(True)
			self.startTripLabel.setStyleSheet("color:rgb(57, 140, 78)")
			self.tripLabel.setText("No Trip In Progress")

			val = backend.BreezeCardMoney(cur_breezeCard)
			self.balanceAmount.setText("$ {:0.2f}".format(val))
		else:
			trip_detail = details[0]
			val = float(trip_detail[1])
			self.balanceAmount.setText("$ {:0.2f}".format(val))
			if (trip_detail[6] == None):
				#They're in a trip so display trip start & disable startTrip
				station = backend.ViewSingleStation(trip_detail[5])
				item = ('{} - {}'.format(station[1],station[0]))
				self.startAtBox.addItem(item)
				self.startAtBox.setEnabled(False)
				self.endingAtBox.setEnabled(True)

				self.startTripLabel.setStyleSheet("color:red")
				self.endTripLabel.setStyleSheet("color:rgb(57,140,78)")
				self.tripLabel.setStyleSheet("color:rgb(57,140,78)")
				
				self.tripLabel.setText("Trip in Progress")

				if station[4]:
					#if IsTrain
					station_list = backend.ViewAllTrainStations()
				else:
					station_list = backend.ViewAllBusStations()

				newList = []
				for station in station_list:
					newList.append("{} - {}".format(station[1],station[0]) )#stationName
				self.endingAtBox.addItems(newList)
	def StartTrip(self, event): 
		cur_breezeCard = self.breezeCardBox.currentText()
		cur_breezeCard = cur_breezeCard.replace(" ","")

		if backend.IsSuspended(cur_breezeCard):
			self.error = "Suspeneded Card can't start trip"
			self.OpenError()
			return		

		if backend.PassengerInTrip():
			self.error = "Passenger In Trip"
			self.OpenError()
			return

		cur_breezeCard = self.breezeCardBox.currentText()
		cur_breezeCard = cur_breezeCard.replace(" ","")

		cur_station = self.startAtBox.currentText()
		pieces = cur_station.split('-') #will split into  pieces, last with fare as decimal - 'x.xx'
		station_stopId = pieces[0][:-1]
		data = backend.ViewSingleStation(station_stopId)

		station_fare = data[2]
		isTrain = data[4]

		if backend.BreezeCardMoney(cur_breezeCard) < station_fare:
			self.error = "Insufficient Funds"
			self.OpenError()
			return

		res = -1
		res = backend.StartTrip(cur_breezeCard,station_stopId)
		
		if res == 1:
			self.UpdateView()
			self.success = "Trip Started!"
			self.OpenSuccess()
		elif res == -1:
			self.error = "Error in Starting Trip"
			self.OpenError()
			return
		else: 
			self.error = "Unkown Error:\n" + str(res)
			self.OpenError()
			return
	def EndTrip(self, event): 
		cur_breezeCard = self.breezeCardBox.currentText()
		cur_breezeCard = cur_breezeCard.replace(" ","")

		if backend.IsSuspended(cur_breezeCard):
			self.error = "Suspeneded Card can't end trip"
			self.OpenError()
			return		

		if not backend.PassengerInTrip():
			self.error = "Passenger Not In Trip"
			self.OpenError()
			return

		end_station = self.endingAtBox.currentText()
		pieces = end_station.split('-') #will split into  pieces, last with fare as decimal - 'x.xx'
		station_stopId = pieces[0][:-1]

		res = -1
		res = backend.EndTrip(cur_breezeCard,station_stopId)
		
		if res == 1:
			self.UpdateView()
			self.success = "Trip Ended!"
			self.OpenSuccess()
		elif res == -1:
			self.error = "Error in Ending Trip"
			self.OpenError()
			return
		else: 
			self.error = "Unkown Error:\n" + str(res)
			self.OpenError()
			return
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