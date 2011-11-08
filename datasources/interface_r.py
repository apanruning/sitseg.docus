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
histplot = robjects.r['hist']
boxplot = robjects.r['boxplot']
densityplot = robjects.r['boxplot']
dotchart = robjects.r['dotchart']
genericplot = robjects.r['genericplot']
ecdfplot = robjects.r['ecdfplot']
paretochart = robjects.r['paretochart'] 
piechart = robjects.r['piechart']
scatterplot = robjects.r['scatterplot']
scatterploatmatrix = robjects.r['scatterplotmatrix']
stripchart = robjects.r['stripchart']


#device function
x11 = robjects.r['x11']
pdf = robjects.r['pdf']
png = robjects.r['png']
off = robjects.r['dev.off']
