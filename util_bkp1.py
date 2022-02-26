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
         loutput.append("[{v: [" + shora.replace(":",",") + "],  f: '" + shora + " hrs.'}," + smagnitud + "],")
      contador = contador + 1

      if(contador == 15):
         contador = 0   #cuenta hasta 3 y resetea
    return loutput

def generaDataScripGgph(sfileinput_his,formatoInput):
    sfile = open(sfileinput_his, "r")
    listinput = sfile.readlines()
    lista = []
    
    lista = filtraColumnasDataInput(listinput,0 , formatoInput)

    for x in  range(0, len(lista)):
      print(lista[x])
    return lista

def eliminaEtiquetas(line1):
        line1 = line1.replace("<html> <head>  <meta http-equiv='refresh' content='5'/> </head> <body>","")
        line1 = line1.replace("</body></html>","")
        return line1

def stringToFile(sdata):
        miarchivo     = open("/var/www/html/concentrador.html","w" ) 
        miarchivo.write(sdata)
        miarchivo.flush()
        miarchivo.close()

def generaHtmlMain():
        sout = ""
	sout = sout + "<html><head>"
	sout = sout + "   <script type='text/javascript'>"
	sout = sout + "	   function changeScreenSize() {    window.resizeTo(screen.width-300,screen.height-500)           } "
	sout = sout + "	   function openWin() {    	        myWindow = window.open('', '', 'width=100, height=100');  } "
	sout = sout + "	   function resizeWin() {  			myWindow.resizeTo(250, 250);  myWindow.focus();   } "
	sout = sout + "	   function closeBrowserWin(){      window.open('','_self','');    window.close();  	      } "
	sout = sout + "	   function actualizar(){location.reload(true);}     setInterval('actualizar()',150000);         " 
	sout = sout + "   </script> 	 								                "
	sout = sout + "   <script type='text/javascript' src='https://www.gstatic.com/charts/loader.js'></script>       "
	sout = sout + "   <script type='text/javascript'>  						 "
	sout = sout + "	     google.charts.load('current', {packages: ['corechart', 'bar']});         "
	sout = sout + "	     google.charts.setOnLoadCallback(drawBasic);   		     	         "
	sout = sout + "	     function drawBasic() {  	                                         "
	sout = sout + "	         var data = new google.visualization.DataTable();    	   	 "
	sout = sout + "		 data.addColumn('timeofday', 'Time of Day');         		 "
	sout = sout + "		 data.addColumn('number', 'Total Watts.');  			 "
	sout = sout + "		 data.addRows([                       "
        lista = generaDataScripGgph()
        for x in range(0,len(lista)):
                 print(lista[x])
                 sout = sout +  lista[x]
	sout = sout + "		 ]);                                  "
	sout = sout + "		 var options = { title: 'Potencia Watts.', colors: ['#33ac71'],  hAxis: { title: 'Hora', format: 'h:mm a', viewWindow: { min: [00, 00, 00],  max: [24, 00, 00]  }}, vAxis: {  title: 'Potencia'  }};	"
	sout = sout + "		 var chart = new google.visualization.LineChart(document.getElementById('chart_div')); "
	sout = sout + "		 chart.draw(data, options);           "
	sout = sout + "	 }   	  				      "
	sout = sout + "	</script>                                     "
	sout = sout + "  </head> 				      "
	sout = sout + "  <body>  				      "
	sout = sout + "   <table border = '0'>			      "
	sout = sout + "		<tr><td><div id='chart_div'  style='width: 650px; height: 350px'></div></td></tr> "
	sout = sout + "	</tr>      "
	sout = sout + "   </table> "
	sout = sout + "</body>     "
	sout = sout + "</html>     "
	return sout


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

def buildGraphTableScript(snombreFuncion,sfileinput_his, formatoInput):
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
        sout = sout + "          var options = { title: 'Potencia Watts.', colors: ['#ff0000'],  hAxis: { title: 'Hora', format: 'h:mm a', viewWindow: { min: [00, 00, 00],  max: [24, 00, 00]  }}, vAxis: {  title: 'Potencia'  }};	\n"
        sout = sout + "          var chart = new google.visualization.LineChart(document.getElementById('chart_div" + snombreFuncion+ "')); \n"
        sout = sout + "          chart.draw(data, options);           \n"
        sout = sout + "  }        \n"
        sout = sout + " </script>                                     \n"
        return sout
