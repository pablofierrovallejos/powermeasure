import time
import requests
from datetime import date

today = date.today()
filename_his ="/var/www/html/power4_" + today.strftime("%Y%m%d")+ ".dat"
filename_his
today_ant = today
today_pos = today
fenergiainihoy =0.0
fpower = 0.0
iesprimera_ejecucion = 1
miarchivo_his = open(filename_his,"a")

shtml = "<html> <head>  <meta http-equiv='refresh' content='5'/> </head> <body>"

while 1: 
    today_pos = date.today()
    if today_ant!= today_pos:
        today_ant = today_pos
	print("Es un nuevo dia")
	miarchivo_his.close()
	filename_his = "/var/www/html/power4_" + today_pos.strftime("%Y%m%d") + ".dat"
	miarchivo_his = open(filename_his,"a")
	print("Abre nuevo archivo: " + filename_his)

    ahora = time.strftime("%c")
		
    try:
        tmptote=0
        fpower=0
 	ploads = {"energyday":tmptote,"power":fpower } 
        r = requests.get("http://192.168.18.206/", timeout=15)
        time.sleep(10)
	line = r.text
        if not line:
            line = " "

        if len(line) > 0:
           line = line.replace(" ","")
           line = line.replace("html","")
           line = line.replace("head","")
           line = line.replace("title","")
	   line = line.replace("body","")
	   line = line.replace("h1","")	
	   line = line.replace("<>","")	
	   line = line.replace("</>","")
	   line = line.replace("<metahttp-equiv='refresh'content='10'/>","")
	   line = line.replace("ESP8266meas2","")
	   line = line.replace("ESP8266servermeas2.","")
           line = line.replace("ESP32ESP32<p>","")
           line = line.replace("<p>",";")
           line = line.replace("</p>","")

	r.raise_for_status()
    except requests.exceptions.RequestException as err:
	print ("OOps: Something Else",err)
    except requests.exceptions.HTTPError as errh:
	print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
	print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
	print ("Timeout Error:",errt)   

			 
    #if len(line) > 0:
    try: 
        #miarchivo_his.write(ahora + ";" + line + "\n" )
        #miarchivo_his.flush()

       # miarchivo     = open("/var/www/html/pow3.html","w" )  #Archivo con el ultimo reg   
       # miarchivo.write(shtml + ahora + ";" + line + "</body></html>")  
       # miarchivo.flush()
       # miarchivo.close()


        lindata=line.split(";")
        print(lindata)
        print(len(lindata))

        if len(lindata)==5 :  #asegura que vengan 7 columnas de datos
           print(lindata[4])
           print(lindata[3])
           fenergia_acumulada = float(lindata[4].replace("Energy:",""))
           fpower             = float(lindata[3].replace("Power:",""))
           if fenergia_acumulada > 0:
               miarchivo_his.write(ahora + ";" + line + "\n" )
               miarchivo_his.flush()

               miarchivo     = open("/var/www/html/pow4.html","w" )  #Archivo con el ultimo reg
               miarchivo.write(shtml + ahora + ";" + line + "</body></html>")
               miarchivo.flush()
               miarchivo.close()


           if iesprimera_ejecucion == 1:
                iesprimera_ejecucion = 0
                fenergiainihoy = fenergia_acumulada
                print("Es primera ejecucion")
              
	        print("Energia acumulada: " + str(fenergia_acumulada))
	        print("Energia hoy: " + str(fenergiainihoy))
                tmptote = str(fenergia_acumulada - fenergiainihoy)
                print("Energiagenerada hoy: " +  tmptote)
                print("Potencia Activa:  " + str(fpower))

                archivototalenergiahoy = open("/var/www/html/totenergiahoy4.txt","w")
                archivototalenergiahoy.write(tmptote)

    except Exception as err:
        print("Line no definido...")     
        print("Algo ha pasadp...",err) 
