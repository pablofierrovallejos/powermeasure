import time
from util import stringToFile
from util import eliminaEtiquetas
from util import generaDataScripGgph
from util import buildIniHtmlHeadScript
from util import buildGraphTableScript
from util import calculaConsumoMensual
from datetime import date

def calculaConsumo(sfilehis, sfilenow,formato):
    filehis = open(sfilehis,"r")
    sfirstline = filehis.readline()
    print(sfirstline)
    filehis.close()
    lfirstline = sfirstline.split(";")
    if formato == "FORMATO_A":
       sfirstline = lfirstline[4].replace(" kWh","")
    if formato == "FORMATO_B":
       sfirstline = lfirstline[5].replace("energy:","")
    if formato == "FORMATO_C":
       sfirstline = lfirstline[5].replace("Energy:","").replace("</body></html>","")
       sfirstline = str(float(sfirstline)/1000)


    filenow = open(sfilenow,"r")
    sline = filenow.readline()
    print(sline)
    filenow.close();
    lline = sline.split(";")
    if formato == "FORMATO_A":
       sline = lline[4].replace(" kWh","")
    if formato == "FORMATO_B":
       sline = lline[5].replace("energy:","")
    if formato == "FORMATO_C":
       sline = lline[5].replace("Energy:","").replace("</body></html>","")
       sline = str(float(sline)/1000)

    #return  sline + "-" + sfirstline  + "=" + str(float(sline) - float(sfirstline) ) + " Kwh"
    return   "<b><FONT COLOR='red'>" + str(float(sline) - float(sfirstline) ).replace(".0","").replace(".",",") + " Kwh (dia)" + "</FONT></b>"

def formateaTablaMeas1(slin):
    lindata=slin.split(";")
    stabla = ""
    stabla = stabla +"<table border =1><tr>\n"
    for x in range(0,len(lindata)):
        stabla = stabla  + "<tr><td>" + lindata[x] + "</td></td>\n"
    stabla = stabla + "</table><p>\n"
    return stabla   



#MAIN
today = date.today()
file_his1 ="/var/www/html/power1_" + today.strftime("%Y%m%d")+ ".dat"
file_his2 ="/var/www/html/power2_" + today.strftime("%Y%m%d")+ ".dat"
file_his3 ="/var/www/html/power3_" + today.strftime("%Y%m%d")+ ".dat"
file_his4 ="/var/www/html/power4_" + today.strftime("%Y%m%d")+ ".dat"

while 1:
   miarchivo1 = open("/var/www/html/pow.html","r")
   miarchivo2 = open("/var/www/html/pow2.html","r")
   miarchivo3 = open("/var/www/html/pow3.html","r")
   miarchivo4 = open("/var/www/html/pow4.html","r")

   line1 = miarchivo1.readline()
   line2 = miarchivo2.readline()
   line3 = miarchivo3.readline()
   line4 = miarchivo4.readline()

   line1 = "<b>Med Panel Solar1</b>;     " + eliminaEtiquetas(line1) + calculaConsumo(file_his1, "/var/www/html/pow.html","FORMATO_A") + ";" + calculaConsumoMensual("MEAS1") + " Kwh/m (mes)"
   line2 = "<b>Med Cons. Casa Fondo</b>; " + eliminaEtiquetas(line2) + ";" + calculaConsumo(file_his2, "/var/www/html/pow2.html","FORMATO_B")  +";"+ calculaConsumoMensual("MEAS2") + " Kwh/m (mes)"
   line3 = "<b>Med Cons. Casa Neg.</b>;  " + eliminaEtiquetas(line3) + ";" + calculaConsumo(file_his3, "/var/www/html/pow3.html","FORMATO_C")  +";"+ calculaConsumoMensual("MEAS3")  + " Kwh/m (mes)"
   line4 = "<b>Med Cons. Casa Centro</b>;" + eliminaEtiquetas(line4) + ";" + calculaConsumo(file_his4, "/var/www/html/pow4.html","FORMATO_C")  +";"+ calculaConsumoMensual("MEAS4")  + " Kwh/m (mes)"

   #Pagina de graficos
   slinfileout = "<html><head>"
   slinfileout = slinfileout + buildIniHtmlHeadScript()
   slinfileout = slinfileout + buildGraphTableScript("drawBasic1",file_his1,"FORMATO_A")
   slinfileout = slinfileout + buildGraphTableScript("drawBasic2",file_his2,"FORMATO_B")
   slinfileout = slinfileout + buildGraphTableScript("drawBasic3",file_his3,"FORMATO_C")
   slinfileout = slinfileout + buildGraphTableScript("drawBasic4",file_his4,"FORMATO_C")


   sout = "  </head> 		            \n"
   sout = sout +  " <body>  	            \n"
   sout = sout +  "  <table border = '0'>   \n"
   sout = sout +  "	<tr><td>" + formateaTablaMeas1(line1)  + "</td><td><div id='chart_divdrawBasic1'  style='width: 1350px; height: 350px'></div></td></tr> \n"
   sout = sout +  "     <tr><td>" + formateaTablaMeas1(line2)  + "</td><td><div id='chart_divdrawBasic2'  style='width: 1350px; height: 350px'></div></td></tr> \n"
   sout = sout +  "     <tr><td>" + formateaTablaMeas1(line3)  + "</td><td><div id='chart_divdrawBasic3'  style='width: 1350px; height: 350px'></div></td></tr> \n"
   sout = sout +  "     <tr><td>" + formateaTablaMeas1(line4)  + "</td><td><div id='chart_divdrawBasic4'  style='width: 1350px; height: 350px'></div></td></tr> \n"
   sout = sout +  "  </table> \n"
   sout = sout +  "</body>    \n"
   sout = sout +  "</html>    \n"

   slinfileout = slinfileout + sout
   stringToFile(slinfileout)

   time.sleep(300) #actualiza cada 5 min
