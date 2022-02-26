from datetime import date

def calculaConsumoMensualTag(sconsumo):
    return "<b>" + sconsumo.replace(".",",") + "</b>"

def calculaConsumoMensual(stipomeas):
    sout = calculaConsumoMensualSinHtml(stipomeas)
    sout =  "<b>" + sout.replace(".",",") + "</b>"
    return sout

def calculaConsumoMensualSinHtml(stipomeas):
    today = date.today()
    shoy = today.strftime("%Y%m%d") 
    sanmes = shoy[0:6]
    sdateini = sanmes + "01"  
    
    file_his1 = ""
    file_now = ""
    if stipomeas == "MEAS1":
       file_his1 ="/var/www/html/power1_" + sdateini + ".dat"                  #<---file historico meas
       file_now =  "/var/www/html/pow.html"                                    #<----file now meas
    if stipomeas == "MEAS2":
       file_his1 ="/var/www/html/power2_" + sdateini + ".dat"                  #<---file historico meas
       file_now =  "/var/www/html/pow2.html"                                   #<----file now meas
    if stipomeas == "MEAS3":
       file_his1 ="/var/www/html/power3_" + sdateini + ".dat"                  #<---file historico meas
       file_now =  "/var/www/html/pow3.html"                                   #<----file now meas
    if stipomeas == "MEAS4":
       file_his1 ="/var/www/html/power4_" + sdateini + ".dat"                  #<---file historico meas
       file_now =  "/var/www/html/pow4.html"                                   #<----file now meas
 
    file = open(file_his1,"r")
    slin = file.readline()
    print("filehis:" + slin) 
    llin = slin.split(";")
    
    consumo_inicial = llin[4].replace(" kWh","")
    if stipomeas == "MEAS2" or stipomeas == "MEAS3" or stipomeas == "MEAS4":
       consumo_inicial = llin[5].replace(" kWh","").replace("Energy:","").replace("energy:","")
    print("Medicion inicial al " + sdateini + ": " +  consumo_inicial + " Kwh/m.")
    file.close()

    filen = open (file_now,"r")
    slin = filen.readline()
    print("filenow:" + slin)
    llin = slin.split(";")
    consumo_final = llin[4].replace(" kWh","")
    if stipomeas == "MEAS2" or stipomeas == "MEAS3" or stipomeas == "MEAS4":
       consumo_final = llin[5].replace("Energy:","").replace("</body></html>","").replace("energy:","")
    print("Medicion final al " + shoy + ": " +  consumo_final + " Kwh/m.")
    filen.close()
    
    fconsumo_final = float(  consumo_final  )
    fconsumo_inicial =  float(  consumo_inicial  )
    if stipomeas == "MEAS3" or stipomeas == "MEAS4":
       fconsumo_final = fconsumo_final/1000
       fconsumo_inicial = fconsumo_inicial/1000

    print("Resta: "  +  str(fconsumo_final) + " - " + str(fconsumo_inicial) )
    consumo_calc =  str(    fconsumo_final   -  fconsumo_inicial    )
    print("Consumo mensual: " + consumo_calc  + " Kwh/m")
    print("========================================================")
    return consumo_calc

def filtraColumnasDataInput(listinput, icol1,formatoInput):
    loutput = []
    contador = 0
    for x in  range(0, len(listinput)):
      slin = listinput[x].split(";")
      shora = slin[icol1]
      shora = shora[11:19]
      sHH   = shora[0:2]
      smagnitud =  ""
      if formatoInput == "FORMATO_A":
         smagnitud =  slin[3] 
         smagnitud = smagnitud[0:(len(smagnitud)-5)]

      if formatoInput == "FORMATO_B":
         smagnitud =  slin[4].strip()
         smagnitud = smagnitud[6:(len(smagnitud)-3)]
         if smagnitud == "":
            smagnitud = "0"


      if formatoInput == "FORMATO_C":
         smagnitud =  slin[4].strip()
         smagnitud = smagnitud[6:(len(smagnitud)-2)]
         if smagnitud == "":
            smagnitud = "0"

      if(contador == 0):
         if( float(smagnitud) < 4999): 
            loutput.append("[{v: [" + shora.replace(":",",") + "],  f: '" + shora + " hrs.'}," + smagnitud + "],")
      contador = contador + 1

      if(contador == 2):
         contador = 0   #cuenta hasta 15 y resetea
    return loutput

def generaDataScripGgph(sfileinput_his,formatoInput):
   	lista = []
   	try:
       		sfile = open(sfileinput_his, "r")
       		listinput = sfile.readlines()
       		lista = filtraColumnasDataInput(listinput,0 , formatoInput)
    	except Exception as err:
       		print("Algo ha pasadp..." + sfileinput_his ,err)
    	return lista

def eliminaEtiquetas(line1):
        line1 = line1.replace("<html> <head>  <meta http-equiv='refresh' content='5'/> </head> <body>","")
        line1 = line1.replace("</body></html>","")
        line1 = line1.replace(".00","").replace(".",",")
        return line1

def stringToFile(sdata):
        miarchivo     = open("/var/www/html/concentrador.html","w" ) 
        miarchivo.write(sdata)
        miarchivo.flush()
        miarchivo.close()


def buildIniHtmlHeadScript():
        sout = ""
        sout = sout + "   <script type='text/javascript'> \n"
        sout = sout + "    function changeScreenSize() {    window.resizeTo(screen.width-300,screen.height-500)           } \n"
        sout = sout + "    function openWin() {                 myWindow = window.open('', '', 'width=100, height=100');  } \n"
        sout = sout + "    function resizeWin() {                       myWindow.resizeTo(250, 250);  myWindow.focus();   } \n"
        sout = sout + "    function closeBrowserWin(){      window.open('','_self','');    window.close();            } \n"
        sout = sout + "    function actualizar(){location.reload(true);}     setInterval('actualizar()',150000);         \n"
        sout = sout + "   </script>                                                                                     \n"
        sout = sout + "   <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>       \n"
        return sout

def buildGraphTableScript(snombreFuncion,sfileinput_his, formatoInput,scolor):
        sout = ""
        sout = sout + "   <script type='text/javascript'>                                        \n"
        sout = sout + "      google.charts.load('current', {packages: ['corechart', 'bar']});    \n"
        sout = sout + "      google.charts.setOnLoadCallback(" + snombreFuncion + ");            \n"
        sout = sout + "      function " + snombreFuncion + "() {                                 \n"
        sout = sout + "          var data = new google.visualization.DataTable();                \n"
        sout = sout + "          data.addColumn('timeofday', 'Time of Day');                     \n"
        sout = sout + "          data.addColumn('number', 'Total Watts.');                       \n"
        sout = sout + "          data.addRows([                       "
        lista = generaDataScripGgph(sfileinput_his,formatoInput)
        for x in range(0,len(lista)):
                 sout = sout +  lista[x] + "\n"
        sout = sout + "          ]);                                   \n"
        sout = sout + "          var options = { title: 'Potencia Watts.', colors: ['" + scolor+"'],  hAxis: { title: 'Hora', format: 'h:mm a', "
        sout = sout + "          viewWindow: { min: [00, 00, 00],  max: [24, 00, 00]  }}, "
        sout = sout + "              vAxis: {  title: 'Potencia'  },"
        sout = sout + "              explorer: {  actions: ['dragToZoom', 'rightClickToReset'],   "
        sout = sout + "                    axis: 'horizontal',  keepInBounds: true,   maxZoomIn: 16.0},"
        sout = sout + "          };"


        sout = sout + "          var chart = new google.visualization.LineChart(document.getElementById('chart_div" + snombreFuncion+ "')); \n"
        sout = sout + "          chart.draw(data, options);           \n"
        sout = sout + "  }        \n"
        sout = sout + " </script>                                     \n"
        return sout
