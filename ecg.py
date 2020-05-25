import scipy.signal
import matplotlib
import pywt
import pandas as pd
import pandasql as sql
pysqldf = lambda q: sql.sqldf(q, globals())
file=pd.read_csv('e0127.csv',skiprows=[1,1])
file=pd.DataFrame(data=file)

end=10000           #setting end of interval to process
start=8000              #setting start of interval to process

ekg=pysqldf("SELECT * from file WHERE `sample interval`<"+str(end)+" AND `sample interval`>"+str(start))
coeffs = pywt.wavedec(ekg.V4, 'db1',level=3)
from matplotlib import pyplot
matplotlib.pyplot.plot(coeffs[0])         														#smoothed example plot
fname='V4_plott_smoothed.pdf'
matplotlib.pyplot.savefig(fname)

h=(1/2)*(max(coeffs[0])+min(coeffs[0]))
peaks=scipy.signal.find_peaks(coeffs[0],height=float(h))
amount=len(peaks[0])
time=(pysqldf("SELECT max(`sample interval`) as bpm from file WHERE `sample interval`<"+str(end)+" AND `sample interval`>"+str(start))-pysqldf("SELECT min(`sample interval`) as bpm from file WHERE `sample interval`<"+str(begin)+" AND `sample interval`>"+str(end)))*0.004
bps=amount/time
bpm=bps*60      																				#average myocardial contractions for selected range [beats per minute]
bpm.to_csv(r'bpm.txt',header=None, index=None, sep=' ', mode='w')

ekg=pysqldf("SELECT * from file")
coeffs = pywt.wavedec(ekg.V4, 'db1',level=3)
h=(1/2)*(max(coeffs[0])+min(coeffs[0]))
peaks=scipy.signal.find_peaks(coeffs[0],height=float(h))
amount=len(peaks[0])
time=pysqldf("SELECT max(`sample interval`) as bpm from file")*0.004
bps=amount/time
bpm=bps*60     																					#average myocardial contractions for whole series [beats per minute]
bpm.to_csv(r'bpm.txt',header=None, index=None, sep=' ', mode='a')
