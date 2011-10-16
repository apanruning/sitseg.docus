import rpy2.robjects as robjects

minimo = robjects.r['min']
maximo = robjects.r['max']
rango = robjects.r['range']                
length = robjects.r['length']                
sumatoria = robjects.r['sum']
media = robjects.r['mean']
cuasi_varianza = robjects.r['var']
desviacion = robjects.r('''function(r) sqrt(var(r)/length(r)) ''')

