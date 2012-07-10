import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

#statitics function
minimo = robjects.r['min']
maximo = robjects.r['max']
rango = robjects.r['range']                
length = robjects.r['length']                
sumatoria = robjects.r['sum']
media = robjects.r['mean']
cuasi_varianza = robjects.r['var']
desviacion = robjects.r('''function(r) sqrt(var(r)/length(r)) ''')


#plots built-in function
bar = robjects.r['barplot']
hist = robjects.r['hist']
boxplot = robjects.r['boxplot']
densityplot = robjects.r['density']
piechart = robjects.r['pie']
scatterplot = robjects.r['plot']
scatterplotmatrix = robjects.r['pairs']
strip = robjects.r['stripchart']

#modules import

#RgoogleMaps = importr('RgoogleMaps')
#maptools = importr('maptools')
pbsmapping = importr('PBSmapping')

#device function
x11 = robjects.r['x11']
pdf = robjects.r['pdf']
png = robjects.r['png']
off = robjects.r['dev.off']

#others
par = robjects.r['par']

