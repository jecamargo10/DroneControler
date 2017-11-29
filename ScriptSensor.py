# -*- coding: utf-8 -*-
import json
import requests
import time
import RPi.GPIO as GPIO    
import time 

headersAll = {'content-type':'application/json'}
hostDir = "192.168.42.91"
portNum = "4000"
appId = "myApp"

GPIO.setmode(GPIO.BCM)     
PTO_TRIGGER = 25          
PTO_ECHO    = 7           
GPIO.setup(PTO_TRIGGER,GPIO.OUT)
GPIO.setup(PTO_ECHO,GPIO.IN)      
GPIO.output(PTO_TRIGGER,False)    
ubicacion = "4.601613°N,74.065173°W"

def pushData(data):
        print "####Pushing data"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications/myApp/containers/cont1/contentInstances'
        dataI = json.dumps({"sensor":data})
        r = requests.post(url, headers = headersAll, data = dataI)
        print "####Pushing data: " + r.content
        return

def register():
        print "####Register App"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications'
        dataI = json.dumps({"application":{"appId":str(appId)}})
        r = requests.post(url, headers = headersAll, data = dataI)
        print r.content
        return

def unregister():
        print "####Unregister App"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications/'+appId
        r = requests.delete(url, headers = headersAll)
        print r.content
        return

def createContainer():
        print "####Creating Containter"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications/'+appId+'/containers'
        dataI = json.dumps({
  "container": {
    "id": "cont1",
    "accessRightID": "/m2m/applications/"+appId+"/accessRights/ar1"
  }
})
        r = requests.post(url, headers = headersAll, data = dataI)
        print r.content
        return

def createRights():
        print "####Creating Rights"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications/'+appId+'/accessRights'
        dataI = json.dumps({"accessRight": {
    "id": "ar1",
    "selfPermissions": {"permission": [{
      "id": appId,
      "permissionFlags": {
        "flag": ["READ", "WRITE", "CREATE", "DELETE"]
      },
      "permissionHolders": {
        "applicationIDs": {"applicationID": [appId]}
      }
    }, {
      "id": "otherApss",
      "permissionFlags": {
        "flag": ["READ"]
      },
      "permissionHolders": {
        "applicationIDs": {"applicationID": ["na1"]}
      }
    }]},
    "permissions": {"permission": [{
      "id": appId,
      "permissionFlags": {
        "flag": ["READ", "WRITE", "CREATE", "DELETE"]
      },
      "permissionHolders": {
       "applicationIDs": {"applicationID": [appId]}
      }
    }, {
      "id": "otherApss",
      "permissionFlags": {
        "flag": ["READ"]
      },
      "permissionHolders": {
        "applicationIDs": {"applicationID": ["na1"]}
      }
    }]}
  }
})
        r = requests.post(url, headers = headersAll, data = dataI)
        print r.content
        return

def updateRights():
        print "####Update Rights"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications/'+appId+'/accessRightID'
        dataI = json.dumps({"accessRightID": '/m2m/applications/'+appId+'/accessRights/ar1'})
        r = requests.put(url, headers = headersAll, data = dataI)
        print r.content
        return

def updateSearchStrings():
        print "####Update Search Strings"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications/'+appId+'/searchStrings'
        dataI = json.dumps({"searchStrings": {"searchString": ["ga", "temperature"]}})
        r = requests.put(url, headers = headersAll, data = dataI)
        print r.content
        return

def subscribe():
        print "####Subscribe"
        url = 'http://'+hostDir+':'+portNum+'/m2m/applications/'+appId+'/containers/cont1/contentInstances/subscriptions'
        dataI = json.dumps({
  "subscription": {
    "contact": "http://169.254.1.3:9999",
    "filterCriteria": {
      "sizeUntil": 30
    }
  }
})
        r = requests.post(url, headers = headersAll, data = dataI)
        print r.content
        return

def main():
       
        register()
        createRights()
        updateRights()
        updateSearchStrings()
        createContainer()
        pushData("SeIniciaTomaDeDatos")
        i=0
        try:
            while True:     
                GPIO.output(PTO_TRIGGER,True)   
                time.sleep(0.00001)             
                GPIO.output(PTO_TRIGGER,False)  
                inicio = time.time()             
                while GPIO.input(PTO_ECHO)==0:  
                    inicio = time.time()         
                while GPIO.input(PTO_ECHO)==1:  
                    fin = time.time()           
                tiempo = fin-inicio             
                distancia = (tiempo * 34300)/2   
                print distancia
                if distancia<10:
                        pushData("Sensor 1")
                time.sleep(3)                    
        except KeyboardInterrupt:                
            GPIO.cleanup()  
        unregister()
        exit(0)
if __name__ == '__main__':
        main()
