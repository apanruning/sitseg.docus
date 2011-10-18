import rpy2.robjects as robjects

minimo = robjects.r['min']
maximo = robjects.r['max']
rango = robjects.r['range']                
length = robjects.r['length']                
sumatoria = robjects.r['sum']
media = robjects.r['mean']
cuasi_varianza = robjects.r['var']
desviacion = robjects.r('''function(r) sqrt(var(r)/length(r)) ''')
hist = robjects.r['hist']
boxplot = robjects.r['boxplot']

x11 = robjects.r['x11']
pdf = robjects.r['pdf']
png = robjects.r['png']
off = robjects.r['dev.off']
