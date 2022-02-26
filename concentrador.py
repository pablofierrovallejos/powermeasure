import time
from util import stringToFile
from util import eliminaEtiquetas
from util import generaDataScripGgph
from util import buildIniHtmlHeadScript
from util import buildGraphTableScript
from util import calculaConsumoMensual
from util import calculaConsumoMensualSinHtml
from util import calculaConsumoMensualTag
from datetime import date

def generaGraficoTotales(sConsumo, sGeneracion, sTotal, sTiempo):
    slin = ""
    slin = "<script type='text/javascript'>\n"
    slin = slin + " google.charts.load('current', {'packages':['bar']});\n"
    slin = slin + " google.charts.setOnLoadCallback(drawChart" + sTiempo+ ");\n"
    slin = slin + "     function drawChart" + sTiempo+"() {\n"
    slin = slin + "        var data = google.visualization.arrayToDataTable([\n"
    slin = slin + "          ['Total Energia " + sTiempo + "', 'Cons. Kwh', 'Generacion Kwh', 'Cons. de Red Kwh'],\n"
    slin = slin + "      ['" + sTiempo + "', " + sConsumo + ", " + sGeneracion + ", " + sTotal + "]   ]);\n"
    slin = slin + "       var options = {\n"
    slin = slin + "          chart: { title: 'Rendimiento " + sTiempo+ "',\n"
    slin = slin + "               subtitle: 'Grafico comparativo de consumo y generacion Energia Totales " + sTiempo+ "',\n"
    slin = slin + "          }};\n"
    slin = slin + "        var chart = new google.charts.Bar(document.getElementById('columnchart_material" + sTiempo + "'));\n"
    slin = slin + "    chart.draw(data, google.charts.Bar.convertOptions(options));\n"
    slin = slin + "      }\n"
    slin = slin + "</script>\n"
    slin = slin + "  <div id='columnchart_material" + sTiempo+ "' style='width: 500px; height: 350px;'></div>\n"
    return slin

def calculaConsumoSinHtml(sfilehis, sfilenow,formato):
   try:
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
      return   str(float(sline) - float(sfirstline) )

   except Exception as err:
      print("Algo ha pasadp...",err)
      return   "0"




def calculaConsumo(sfilehis, sfilenow,formato):
    slin =   calculaConsumoSinHtml(sfilehis, sfilenow,formato)
    return   "<b><FONT COLOR='red'>" + slin.replace(".",",") + " Kwh (dia)" + "</FONT></b>"

def calculaConsumo(sconsumo):
    return   "<b><FONT COLOR='red'>" + sconsumo.replace(".",",") + " Kwh (dia)" + "</FONT></b>"


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

   sconsumo1 = calculaConsumoSinHtml(file_his1, "/var/www/html/pow.html","FORMATO_A")  #Generacion Panel1
   sconsumo2 = calculaConsumoSinHtml(file_his2, "/var/www/html/pow2.html","FORMATO_B") #Consumo casa fondo
   sconsumo3 = calculaConsumoSinHtml(file_his3, "/var/www/html/pow3.html","FORMATO_C") #Consumo negocio
   sconsumo4 = calculaConsumoSinHtml(file_his4, "/var/www/html/pow4.html","FORMATO_C") #Generacion Panel2
   fEnerGeneradaDia  = float(sconsumo1) +  float(sconsumo4)
   fEnerConsumidaDia = float(sconsumo2) +  float(sconsumo3)
   fEnerTotalDia     = fEnerConsumidaDia - fEnerGeneradaDia

   sconsumo1Mes  = calculaConsumoMensualSinHtml("MEAS1")
   sconsumo2Mes  = calculaConsumoMensualSinHtml("MEAS2")
   sconsumo3Mes  = calculaConsumoMensualSinHtml("MEAS3")
   sconsumo4Mes  = calculaConsumoMensualSinHtml("MEAS4")
   fEnerGeneradaMes  = float(sconsumo1Mes) +  float(sconsumo4Mes)
   fEnerConsumidaMes = float(sconsumo2Mes) +  float(sconsumo3Mes)
   fEnerTotalMes     = fEnerConsumidaMes - fEnerGeneradaMes


   line1 = "<b><h3>(1)Panel Solar 1</b></h3>;" + eliminaEtiquetas(line1) +       calculaConsumo(sconsumo1) + ";"+ calculaConsumoMensualTag(sconsumo1Mes) + " Kwh/m (mes)"
   line4 = "<b><h3>(2)Panel Solar 2</b></h3>;" + eliminaEtiquetas(line4) + ";" + calculaConsumo(sconsumo4) + ";"+ calculaConsumoMensualTag(sconsumo4Mes) + " Kwh/m (mes)"
   line2 = "<b><h3>(4)Casa Fondo</b></h3>; "   + eliminaEtiquetas(line2) + ";" + calculaConsumo(sconsumo2) + ";"+ calculaConsumoMensualTag(sconsumo2Mes) + " Kwh/m (mes)"
   line3 = "<b><h3>(3)Negocio</b></h3>;  "     + eliminaEtiquetas(line3) + ";" + calculaConsumo(sconsumo3) + ";"+ calculaConsumoMensualTag(sconsumo3Mes) + " Kwh/m (mes)"

   #Pagina de graficos
   slinfileout = "<html><head>"
   slinfileout = slinfileout + buildIniHtmlHeadScript()
   slinfileout = slinfileout + buildGraphTableScript("drawBasic1",file_his1,"FORMATO_A","#228B22")
   slinfileout = slinfileout + buildGraphTableScript("drawBasic4",file_his4,"FORMATO_C","#228B22")
   slinfileout = slinfileout + buildGraphTableScript("drawBasic2",file_his2,"FORMATO_B","#FF0000")
   slinfileout = slinfileout + buildGraphTableScript("drawBasic3",file_his3,"FORMATO_C","#FF0000")


   sout = "  </head> 		            \n"
   sout = sout +  " <body>  	            \n"
   sout = sout +  "<hr>\n"
   sout = sout +  "<center><table border = '0' cellspacing='20'><tr>\n"
   sout = sout +  "    <td>" + generaGraficoTotales(str(fEnerConsumidaDia),str(fEnerGeneradaDia), str(fEnerTotalDia), "Hoy") + "</td>\n"
   sout = sout +  "    <td>" + generaGraficoTotales(str(fEnerConsumidaMes),str(fEnerGeneradaMes), str(fEnerTotalMes), "Mes")+ "</td>\n"
   sout = sout +  "</tr>\n"
   sout = sout +  "</table></center>\n"
   sout = sout +  "<hr>\n"
   sout = sout +  " <table border = '0'>   \n"
   sout = sout +  "	<tr><td>" + formateaTablaMeas1(line1)  + "</td><td><div id='chart_divdrawBasic1'  style='width: 1200px; height: 350px'></div></td></tr> \n"
   sout = sout +  "     <tr><td>" + formateaTablaMeas1(line4)  + "</td><td><div id='chart_divdrawBasic4'  style='width: 1200px; height: 350px'></div></td></tr> \n"
   sout = sout +  "     <tr><td>" + formateaTablaMeas1(line3)  + "</td><td><div id='chart_divdrawBasic3'  style='width: 1200px; height: 350px'></div></td></tr> \n"
   sout = sout +  "     <tr><td>" + formateaTablaMeas1(line2)  + "</td><td><div id='chart_divdrawBasic2'  style='width: 1200px; height: 350px'></div></td></tr> \n"
   sout = sout +  "  </table> \n"
   sout = sout +  "</body>    \n"
   sout = sout +  "</html>    \n"

   slinfileout = slinfileout + sout
   stringToFile(slinfileout)

   time.sleep(300) #actualiza cada 5 min
