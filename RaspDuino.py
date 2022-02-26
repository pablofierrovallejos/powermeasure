import os 
import serial
import time
import requests
from datetime import date

today = date.today()
filename_his ="/var/www/html/power" + today.strftime("%Y%m%d")+ ".dat"
filename_his
today_ant = today
today_pos = today
fenergiainihoy =0.0
fpower = 0.0
iesprimera_ejecucion = 1
miarchivo_his = open(filename_his,"a")

shtml = "<html> <head>  <meta http-equiv='refresh' content='5'/> </head> <body>"

ser = serial.Serial('/dev/ttyACM0', 9600)
while 1: 
    today_pos = date.today()
    if today_ant!= today_pos:
        today_ant = today_pos
	print("Es un nuevo dia")
	miarchivo_his.close()
        filename_his = "/var/www/html/power" + today_pos.strftime("%Y%m%d") + ".dat"
        miarchivo_his = open(filename_his,"a")
        print("Abre nuevo archivo: " + filename_his)

    if(ser.in_waiting >0):
        ahora = time.strftime("%c")

        line = ser.readline()
	miarchivo_his.write(ahora + ";" + line)
        miarchivo_his.flush()

        miarchivo     = open("/var/www/html/pow.html","w" )  #Archivo con el ultimo reg   
        miarchivo.write(shtml + ahora + ";" + line + "</body></html>")  
        miarchivo.flush()
        miarchivo.close()


        lindata=line.split(";")
        print(lindata)
        
        if len(lindata)==7 :  #asegura que vengan 7 columnas de datos
            fenergia_acumulada = float(lindata[3].replace(" kWh",""))
            fpower             = float(lindata[2].replace(" W",""))
            if iesprimera_ejecucion == 1:
                 iesprimera_ejecucion = 0
                 fenergiainihoy = fenergia_acumulada
                 print("Es primera ejecucion")
              
  	    print("Energia acumulada: " + str(fenergia_acumulada))
 	    print("Energia hoy: " + str(fenergiainihoy))
            tmptote = str(fenergia_acumulada - fenergiainihoy)
            print("Energiagenerada hoy: " +  tmptote)
            print("Potencia Activa:  " + str(fpower))

            archivototalenergiahoy = open("/var/www/html/totenergiahoy.txt","w")
            archivototalenergiahoy.write(tmptote)
           

	    try:
           	 ploads = {"energyday":tmptote,"power":fpower } 
            	 r = requests.get("http://192.168.18.200/energy", params=ploads, timeout=10)
            	 #print(r.text)
		 r.raise_for_status()
            except requests.exceptions.RequestException as err:
	  	 print ("OOps: Something Else",err)
		 #os.system("shutdown /r /t 1")
	    except requests.exceptions.HTTPError as errh:
    		 print ("Http Error:",errh)
		 #os.system("shutdown /r /t 1")
	    except requests.exceptions.ConnectionError as errc:
   		 print ("Error Connecting:",errc)
		 #os.system("shutdown /r /t 1")
	    except requests.exceptions.Timeout as errt:
	         print ("Timeout Error:",errt)   
		 #os.system("shutdown /r /t 1")
