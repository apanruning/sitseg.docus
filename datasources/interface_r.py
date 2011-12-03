import rpy2.robjects as robjects

#statitics function
minimo = robjects.r['min']
maximo = robjects.r['max']
rango = robjects.r['range']                
length = robjects.r['length']                
sumatoria = robjects.r['sum']
media = robjects.r['mean']
cuasi_varianza = robjects.r['var']
desviacion = robjects.r('''function(r) sqrt(var(r)/length(r)) ''')


#plots function
bxp = robjects.r['bxp']
hist = robjects.r['hist']
boxplot = robjects.r['boxplot']
densityplot = robjects.r['density']
dotchart = robjects.r['dotchart']
genericplot = robjects.r['plot']
ecdfplot = robjects.r['plot.ecdf']
#paretochart = robjects.r['pareto.chart'] 
piechart = robjects.r['pie']
scatterplot = robjects.r['plot']
#scatterplotmatrix = robjects.r['scatterplotMatrix']
#stripchart = robjects.r['stripchart']


#device function
x11 = robjects.r['x11']
pdf = robjects.r['pdf']
png = robjects.r['png']
off = robjects.r['dev.off']
