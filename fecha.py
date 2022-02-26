from datetime import date

today = date.today()

print(today)

print("El dia actual es {}".format(today.day))
print("El mes actual es {}".format(today.month))
print("El anio actual es {}".format(today.year))


print (format(today.year) + " test ")

format = today.strftime('Dia :%d, Mes: %m, Anio %Y, Hora: %H, Minutos: %M, Segundos: %S')

print (format)

