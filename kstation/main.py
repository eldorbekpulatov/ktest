import os
import sys
import requests
import subprocess
from datetime import date
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi


#config parameters 
HOST_URL = "http://127.0.0.1:8000"
API_URL =  "http://127.0.0.1:8000/api"
DOWNLOAD_DIR = os.path.join(os.getcwd(),'downloads')
LOGS_DIR = os.path.join(os.getcwd(),'logs')



class Session():
    def __init__(self, token):
        self.__token = token
        self.user = None
        self.station = None
        self.product = None
        self.model = None
        self.stage = 0

    def getAuth(self):
        return {"Authorization": "Token "+self.__token}
 
    def incrementStage(self):
        self.stage += 1
        self.__cleanse__()
    
    def decrementStage(self):
        self.stage -= 1
        self.__cleanse__()

    def setUser(self, user):
        if user:
            pass
        self.user = user
        
    def setStation(self, station):
        if station:
            instruments_parsed = {'dvm':[],'osc':[],'eload':[],'rctrl':[],'actrl':[]}  
            for instrument in station['instruments']: 
                if instrument['type'] in instruments_parsed:
                    instruments_parsed[instrument['type']].append(instrument)
                else:
                    instruments_parsed[instrument['type']]= [instrument]
            station['instruments'] = instruments_parsed
        self.station = station

    def setProduct(self, product):
        if product:
            pass
        self.product = product

    def setModel(self, model):
        if model:
            pass
        self.model = model
    
    def __cleanse__(self):
        if self.stage == 0:
            self.station = None
            self.product = None
            self.model = None
        elif self.stage == 1:
            self.product = None
            self.model = None
        elif self.stage == 2:
            self.model = None
            
    
class Login(QtWidgets.QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("./ui/login.ui", self)
        self.loginButton.clicked.connect(self.authenticate)
        
    def authenticate(self):
        username = self.userNameInput.text()
        password = self.passwordInput.text()
        data = {"username":username, "password":password}
        response = requests.post(API_URL+'/login', data=data)
        
        if response.status_code != 200:
            self.errorMessege.setText(response.text)
        else:
            self.errorMessege.setText("")
            s = Session(response.json()["token"])
            widget.addWidget(Index(s))
            widget.setCurrentIndex(widget.currentIndex()+1)
        self.passwordInput.setText("") 
        

class Index(QtWidgets.QDialog):
    def __init__(self, session):
        super(Index,self).__init__()
        loadUi("./ui/index.ui", self)
        self.session = session
        self.signoutButton.clicked.connect(self.unauthenticate)
        self.nextButton.clicked.connect(self.nextStep)
        self.prevButton.clicked.connect(self.prevStep)
        self.update()

    def populateInformation(self):
        self.fullName.setText(self.session.user['first_name']+" "+self.session.user['last_name'])
        self.userName.setText(self.session.user['username'])
        self.email.setText(self.session.user['email'])
        self.errorMessege.setText("")
        self.progressBar.setValue(int(self.session.stage/4*100))
        if self.listWidget.count() > 0:
            self.listWidget.setCurrentRow(0)

    def unauthenticate(self):
        widget.removeWidget(widget.currentWidget())
        del(self.session)

    def nextStep(self):
        if self.listWidget.currentItem() is None:
            self.errorMessege.setText("Please select an item.")
        else:
            self.session.incrementStage()
            self.update()         

    def prevStep(self):
        self.session.decrementStage()
        self.update()

    def setUser(self):
        response = requests.get(url=API_URL+"/stations",headers=self.session.getAuth())
        if response.status_code != 200:
            self.errorMessege.setText(response.text)
        else:
            self.listWidget.clear() # flush the list widget
            self.session.setUser(response.json()['user'])
            for station in response.json()['stations']:
                item = QtWidgets.QListWidgetItem(str(station['name']),type=int(station["id"]))
                self.listWidget.addItem(item)

    def setStation(self):
        if self.session.station:
            ID = self.session.station['id']
        else:
            ID = self.listWidget.currentItem().type()
        response = requests.get(url=API_URL+"/products",data={'id':ID},headers=self.session.getAuth())
        if response.status_code != 200:
            self.errorMessege.setText(response.text)
        else:
            self.listWidget.clear() # flush the list Widget
            self.session.setStation(response.json()['station'])
            for product in response.json()['products']:
                item = QtWidgets.QListWidgetItem(str(product['name']),type=int(product["id"]))
                self.listWidget.addItem(item)
   
    def setProduct(self):
        if self.session.product:
            ID = self.session.product['id']
        else:
            ID = self.listWidget.currentItem().type()
        response = requests.get(url=API_URL+"/models",data={'id':ID},headers=self.session.getAuth())
        if response.status_code != 200:
            self.errorMessege.setText(response.text)
        else:
            self.listWidget.clear()  
            self.session.setProduct(response.json()['product'])  
            for model in response.json()['models']:
                item = QtWidgets.QListWidgetItem(str(model['name']),type=int(model["id"]))
                self.listWidget.addItem(item)
            
    def setModel(self):
        if self.session.model:
            ID = self.session.product['id']
        else:
            ID = self.listWidget.currentItem().type()
        response = requests.get(url=API_URL+"/scripts",data={'id':ID},headers=self.session.getAuth())
        if response.status_code != 200:
            self.errorMessege.setText(response.text)
        else:
            self.session.setModel(response.json()["model"])
    
    def update(self):
        if self.session.stage == 0:
            self.setUser()
            self.apiBox.setTitle("Select a station")
            self.nextButton.setText("Next: Select Product")
            self.prevButton.setText("Back: None")
            self.nextButton.setEnabled(True)
            self.prevButton.setEnabled(False)     
        elif self.session.stage == 1:
            self.setStation()
            self.apiBox.setTitle("Select a product")
            self.nextButton.setText("Next: Select Model")
            self.prevButton.setText("Back: Select Station")
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)
        elif self.session.stage == 2:
            self.setProduct()
            self.apiBox.setTitle("Select a model")
            self.nextButton.setText("Next: Start Testing")
            self.prevButton.setText("Back: Select Product")
            self.nextButton.setEnabled(True)
            self.prevButton.setEnabled(True)
        elif self.session.stage == 3:
            self.setModel()
            widget.addWidget(Run(self.session))
            widget.setCurrentIndex(widget.currentIndex()+1)
        self.populateInformation()


class Run(QtWidgets.QDialog):
    def __init__(self, session):
        super(Run,self).__init__()
        loadUi("./ui/run.ui", self)
        self.session = session
        self.exitButton.clicked.connect(self.cancel)
        self.reloadButton.clicked.connect(self.reload)
        self.submitButton.clicked.connect(self.submit)
        self.runAllButton.clicked.connect(self.runAll)
        self.runSelectedButton.clicked.connect(self.runSelected)
        self.populateInformation()
    
    def populateInformation(self):
        self.testLogsWidget.clear()
        self.errorMessege.setText("")
        self.stationTitle.setText(str(self.session.station['name']))
        self.productTitle.setText(str(self.session.product['name'])+" "+str(self.session.model['name']))
        self.fillInstrumentsTable()
        self.fillScriptsList()
        self.progressBar.setValue(int(self.session.stage/4*100))

    def fillInstrumentsTable(self):
        key = 'name'  # populate instrument table based on key
        dvmString = [ dvm[key] for dvm in self.session.station['instruments']['dvm'] ]
        oscString = [ osc[key] for osc in self.session.station['instruments']['osc'] ]
        relayString = [ relay[key] for relay in self.session.station['instruments']['rctrl'] ]
        analogString = [ analog[key] for analog in self.session.station['instruments']['actrl'] ]
        eloadString = [ elaod[key] for elaod in self.session.station['instruments']['eload'] ]
        self.instrumentTable.setItem(0, 0, QtWidgets.QTableWidgetItem(','.join(dvmString)))
        self.instrumentTable.setItem(1, 0, QtWidgets.QTableWidgetItem(','.join(oscString)))
        self.instrumentTable.setItem(2, 0, QtWidgets.QTableWidgetItem(','.join(relayString)))
        self.instrumentTable.setItem(3, 0, QtWidgets.QTableWidgetItem(','.join(eloadString)))
        self.instrumentTable.setItem(4, 0, QtWidgets.QTableWidgetItem(','.join(analogString)))

    def fillScriptsList(self):
        self.listWidget.clear()
        for script in self.session.model['scripts']:
            item = QtWidgets.QListWidgetItem(str(script['name']),type=int(script["id"]))
            self.listWidget.addItem(item)
        if len(self.session.model['scripts']) > 0:
            self.listWidget.setCurrentRow(0)

    def cancel(self):
        self.session.decrementStage()
        widget.removeWidget(widget.currentWidget())
        widget.currentWidget().update()

    def submit(self):
        self.session.incrementStage()
        widget.addWidget(Card(self.session))
        widget.setCurrentIndex(widget.currentIndex()+1)

    def reload(self):
        data = {
            'station_id':self.session.station['id'],
            'product_id':self.session.product['id'],
            'model_id':self.session.model['id'], 
        }
        response = requests.get(url=API_URL+"/reload",headers=self.session.getAuth(),data=data)
        if response.status_code != 200:
            self.errorMessege.setText(response.text)
        else:
            self.session.setStation(response.json()['station'])
            self.session.setProduct(response.json()['product'])
            self.session.setModel(response.json()['model'])
        self.populateInformation()

    def runAll(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setSelected(True)
        self.runSelected()

    def runSelected(self):
        self.testLogsWidget.clear()
        self.errorMessege.setText("")
        if len(self.listWidget.selectedItems()) > 0:
            scriptDatas = self.session.model['scripts']
            scriptItems = [self.listWidget.item(i) for i in range(self.listWidget.count())]
            for script in zip(scriptItems, scriptDatas):
                if script[0] in self.listWidget.selectedItems():
                    self.downloadScript(script[1])
                    self.validateScript(script[1])  
                    self.executeScript(script[1])
                    # self.flushScript(script[1])
        else:
            self.errorMessege.setText("No test was selected. Please select at least one to execute.")

    def downloadScript(self, script):
        response = requests.get(url=HOST_URL+script['file'])
        if response.status_code != 200:
            self.errorMessege.setText(str(response)+":"+str(response.url))
        else:
            _, filename = os.path.split(script['file'])
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, 'w') as file:
                file.write(response.text)
            script['filepath'] = filepath

    def validateScript(self, script):
        requirements = []
        valid = {'dvm':False, 'osc':False, 'rctrl':False, 'actrl':False, 'eload':False}
        for k, v in valid.items():
            if script[k] <= len(self.session.station['instruments'][k]):
                requirements.extend(self.session.station['instruments'][k][:script[k]])
                valid[k] = True
        script["requirements"] = requirements
        return all(valid.values())

    def executeScript(self, script):
        logPath = os.path.join(LOGS_DIR, str(script["id"])+".log")
        cmd = ['python', script['filepath'], logPath]
        for instrument in script['requirements']:
            if instrument['type'] == 'dvm':
                cmd.append("-d"+instrument['resourceID'])
            elif instrument['type'] == 'osc':
                cmd.append("-o"+instrument['resourceID'])
            elif instrument['type'] == 'rctrl':
                cmd.append("-r"+instrument['resourceID'])
            elif instrument['type'] == 'actrl':
                cmd.append("-a"+instrument['resourceID'])
            elif instrument['type'] == 'eload':
                cmd.append("-e"+instrument['resourceID'])

        if os.path.exists(script['filepath']):
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout = result.stdout.decode('utf-8')
            stderr = result.stderr.decode('utf-8')
            if len(stderr)>0:
                self.errorMessege.setText("Unexpected error occurred while executing the script.")
            else:
                item = QtWidgets.QListWidgetItem(stdout, type=int(script["id"]))
                self.testLogsWidget.addItem(item)
                script["logpath"] = logPath
        else:
            self.errorMessege.setText("Invalid filepath. Script was not downloaded.")

    def flushScript(self, script):
        if os.path.exists(script['filepath']):
            os.remove(script['filepath'])
        if os.path.exists(script['logpath']):
            os.remove(script['logpath'])
        del(script["filepath"])
        del(script["requirements"])
        del(script["logpath"])
        

class Card(QtWidgets.QDialog):
    def __init__(self, session):
        super(Card,self).__init__()
        loadUi("./ui/card.ui", self)
        self.session = session
        self.exitButton.clicked.connect(self.cancel)
        self.submitButton.clicked.connect(self.submit)
        self.populateInformation()

    def populateInformation(self):
        self.errorMessege.setText("")
        self.fillTestCardTable()
        self.fillInstrumentsTable()
        self.progressBar.setValue(int(self.session.stage/4*100))

    def fillTestCardTable(self):
        station_name = self.session.station['name']
        product_name = self.session.product['name']
        user_name = self.session.user['first_name']+" "+self.session.user['last_name']
        model_name = self.session.model['name']
        date_string = date.today().strftime("%m/%d/%Y")
        time_string = datetime.now().strftime("%H:%M:%S %p")
        self.testCardTable.setItem(0, 0, QtWidgets.QTableWidgetItem(station_name))
        self.testCardTable.setItem(1, 0, QtWidgets.QTableWidgetItem(product_name))
        self.testCardTable.setItem(2, 0, QtWidgets.QTableWidgetItem(model_name))
        self.testCardTable.setItem(3, 0, QtWidgets.QTableWidgetItem(user_name))
        self.testCardTable.setItem(4, 0, QtWidgets.QTableWidgetItem(date_string))
        self.testCardTable.setItem(5, 0, QtWidgets.QTableWidgetItem(time_string))

    def fillInstrumentsTable(self):
        key = 'name' # populate instrument table based on key
        dvmString = [ dvm[key] for dvm in self.session.station['instruments']['dvm'] ]
        oscString = [ osc[key] for osc in self.session.station['instruments']['osc'] ]
        relayString = [ relay[key] for relay in self.session.station['instruments']['rctrl'] ]
        analogString = [ analog[key] for analog in self.session.station['instruments']['actrl'] ]
        eloadString = [ elaod[key] for elaod in self.session.station['instruments']['eload'] ]
        self.instrumentTable.setItem(0, 0, QtWidgets.QTableWidgetItem(','.join(dvmString)))
        self.instrumentTable.setItem(1, 0, QtWidgets.QTableWidgetItem(','.join(oscString)))
        self.instrumentTable.setItem(2, 0, QtWidgets.QTableWidgetItem(','.join(relayString)))
        self.instrumentTable.setItem(3, 0, QtWidgets.QTableWidgetItem(','.join(eloadString)))
        self.instrumentTable.setItem(4, 0, QtWidgets.QTableWidgetItem(','.join(analogString)))

    def cancel(self):
        self.session.decrementStage()
        widget.removeWidget(widget.currentWidget())
        widget.currentWidget().update()
    
    def submit(self):
        serialNumber = self.serialNumber.text()
        

        data = {
            "serial_number":serialNumber,
            "station_id":self.session.station["id"],
            "product_id": self.session.product["id"],
            "model_id":self.session.model["id"],
            "log_file":"hello"
            }
        response = requests.post(API_URL+'/card', headers=self.session.getAuth(), data=data)

        if response.status_code != 200:
            self.errorMessege.setText(response.text)
        else:
            self.errorMessege.setText("")




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setFixedWidth(800)
    widget.setFixedHeight(600)
    widget.addWidget(Login())
    widget.show()
    app.exec()