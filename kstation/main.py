
import io
import os
import sys
import requests
import subprocess
from datetime import date
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator


#config parameters 
HOST_URL = "http://127.0.0.1:8000"
API_URL =  "http://127.0.0.1:8000/api"
SCRIPTS_DIR = os.path.join(os.getcwd(),'scripts')
LOGS_DIR = os.path.join(os.getcwd(),'logs')


class Session():
    def __init__(self, token):
        self.__token__ = token
        self.user = None
        self.station = None
        self.product = None
        self.model = None
        self.stage = 0

    def getAuth(self):
        return {"Authorization": "Token "+self.__token__}

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
            for instrument in station['instrument_set']: 
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

    def populate(self):
        self.errorMessege.setText("")
        self.fullName.setText(self.session.user['first_name']+" "+self.session.user['last_name'])
        self.userName.setText(self.session.user['username'])
        self.email.setText(self.session.user['email'])
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
        self.populate()


class Run(QtWidgets.QDialog):
    def __init__(self, session):
        super(Run,self).__init__()
        loadUi("./ui/run.ui", self)
        self.session = session
        self.exitButton.clicked.connect(self.cancel)
        self.reloadButton.clicked.connect(self.reload)
        self.submitButton.clicked.connect(self.submit)
        self.runAllButton.clicked.connect(self.runAll)
        self.runSelButton.clicked.connect(self.runSelected)
        self.populate()
        
    def populate(self):
        self.testLogsWidget.clear()
        self.errorMessege.setText("")
        self.submitButton.setEnabled(False)
        self.progressBar.setValue(int(self.session.stage/4*100))
        self.stationTitle.setText(str(self.session.station['name']))
        self.productTitle.setText(str(self.session.product['name'])+" "+str(self.session.model['name']))
        self.fillInstrumentsTable()
        self.fillScriptsList()
        
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
        self.flushScripts()
        self.session.decrementStage()
        widget.removeWidget(widget.currentWidget())
        widget.currentWidget().update()

    def submit(self):
        self.session.incrementStage()
        widget.addWidget(Card(self.session))
        widget.setCurrentIndex(widget.currentIndex()+1)

    def reload(self):
        self.flushScripts()
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
        self.populate()

    def runAll(self):
        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setSelected(True)
        self.runSelected()

    def runSelected(self):
        self.flushScripts()
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
            self.submitButton.setEnabled(True)
        else:
            self.errorMessege.setText("No test was selected. Please select at least one to execute.")

    def downloadScript(self, script):
        response = requests.get(url=HOST_URL+script['file'])
        if response.status_code != 200:
            self.errorMessege.setText(str(response)+":"+str(response.url))
        else:
            filename = str(script['id'])+".py"
            filepath = os.path.join(SCRIPTS_DIR, filename)
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
            stdout = result.stdout.decode('utf-8').replace("\n","")
            stderr = result.stderr.decode('utf-8').replace("\n","")
            if len(stderr)>0:
                self.errorMessege.setText("Unexpected error occurred while executing the script.")
            else:
                log_string = 60*["."]
                log_string[0:len(script["name"])]= script["name"]
                log_string[-1*len(stdout):] = stdout
                item = QtWidgets.QListWidgetItem("".join(log_string), type=int(script["id"]))
                self.testLogsWidget.addItem(item)
                script["logpath"] = logPath
                script["status"] = stdout
        else:
            self.errorMessege.setText("Invalid filepath. Script was not downloaded.")
        
    def flushScripts(self):
        for f in os.listdir(SCRIPTS_DIR):
            os.remove(os.path.join(SCRIPTS_DIR, f))
        for f in os.listdir(LOGS_DIR):
            os.remove(os.path.join(LOGS_DIR, f))
        for script in self.session.model["scripts"]:
            if "filepath" in script:
                del(script["filepath"])
            if "logpath" in script:
                del(script["logpath"])
            if "requirements" in script:
                del(script["requirements"])

    
class Card(QtWidgets.QDialog):
    def __init__(self, session):
        super(Card,self).__init__()
        loadUi("./ui/card.ui", self)
        self.session = session
        reg_ex = QRegExp("^[A-Z|a-z][0-9]{6,7}$")
        validator = QRegExpValidator(reg_ex, self.serialInput)
        self.serialInput.setValidator(validator)
        self.exitButton.clicked.connect(self.cancel)
        self.submitButton.clicked.connect(self.getSerial)
        self.serialInput.textChanged.connect(self.validateSerial)
        self.populate()

    def populate(self):
        self.validateSerial()
        self.fillLogView()
        self.fillTestCardTable()
        self.fillInstrumentsTable()
        self.progressBar.setValue(int(self.session.stage/4*100))
              
    def fillLogView(self):
        for script in self.session.model["scripts"]:
            if "logpath" in script:
                with open(script['logpath'], 'r') as logfile:
                    logs = "".join(logfile.readlines())
                    self.logEditor.appendPlainText(logs)
   
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
    
    def validateSerial(self):
        if self.serialInput.hasAcceptableInput():
            self.errorMessege.setText("")
            self.submitButton.setEnabled(True)
        else:
            self.errorMessege.setText("Input a serial number before committing. (Ex: A123456)")
            self.submitButton.setEnabled(False)

    def getSerial(self):
        serialNumber = self.serialInput.text()
        data = {
            "serial_number": serialNumber,
            "product_id":self.session.product["id"],
            "model_id":self.session.model["id"],
        }
        response = requests.get(API_URL+'/card',headers=self.session.getAuth(),data=data)
        if 200<=response.status_code and response.status_code<=300: # success
            self.popup(serial = serialNumber, code = response.status_code, data=response.text)
        else: # fail
            self.errorMessege.setText(response.text)


    def postSerial(self, serial):
        files = {}
        for script in self.session.model['scripts']:
            logfile = open(script["logpath"], "rb")
            files["{}-{}".format(script['id'], script['status'])] = logfile
        data = {
            "serial_number": serial,
            "station_id":self.session.station["id"],
            "product_id": self.session.product["id"],
            "model_id":self.session.model["id"],
        }
        response = requests.post(API_URL+'/card',headers=self.session.getAuth(),data=data,files=files)
        if response.status_code == 201: # success
            self.errorMessege.setText(response.text)
        else: # fail
            self.errorMessege.setText(response.text)
    
    def popup(self, serial, code, data=None):
        self.msg = QtWidgets.QMessageBox()
        if code == 202: # ACCEPTED, overwrite 
            self.msg.setWindowTitle("Confirmation to submit...")
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setStandardButtons(QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Yes)
            self.msg.setDefaultButton(QtWidgets.QMessageBox.No)
            self.msg.setText("Serial Number {} is in database.".format(serial))
            self.msg.setInformativeText("Do you want to overwrite previous entry?")
            self.msg.setDetailedText(data)
            if self.msg.exec() == QtWidgets.QMessageBox.Yes:
                self.postSerial(serial)
        elif code == 204: # NO_CONTENT, create new 
            self.msg.setWindowTitle("Confirmation to submit...")
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setStandardButtons(QtWidgets.QMessageBox.No|QtWidgets.QMessageBox.Yes)
            self.msg.setDefaultButton(QtWidgets.QMessageBox.No)
            self.msg.setText("Serial Number {} is a new entry.".format(serial))
            self.msg.setInformativeText("Do you want to submit as a new entry?")
            if self.msg.exec() == QtWidgets.QMessageBox.Yes:
                self.postSerial(serial)
        elif code == 226: # IM_USED, new serial
            self.msg.setWindowTitle("Confirmation to submit...")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
            self.msg.setText("Serial Number {} is not available.".format(serial))
            self.msg.setInformativeText("Please input a different serial number and try again.")
            self.msg.setDetailedText(data)
            if self.msg.exec() == QtWidgets.QMessageBox.Ok:
                self.serialInput.setText(""),
            
            

    def cancel(self):
        self.session.decrementStage()
        widget.removeWidget(widget.currentWidget())
        widget.currentWidget().update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    widget.setFixedWidth(800)
    widget.setFixedHeight(600)
    widget.addWidget(Login())
    widget.show()
    app.exec()