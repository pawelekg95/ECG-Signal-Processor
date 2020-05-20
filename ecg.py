import scipy.signal
import matplotlib
import pywt
import pandas as pd
import pandasql as sql
pysqldf = lambda q: sql.sqldf(q, globals())
file=pd.read_csv('e0127.csv',skiprows=[1,1])
file=pd.DataFrame(data=file)

ekg=pysqldf("SELECT * from file WHERE `sample interval`<1000 AND `sample interval`>100")        #setting range of interval to process
coeffs = pywt.wavedec(ekg.V4, 'db1',level=2)
from matplotlib import pyplot
matplotlib.pyplot.plot(coeffs[0])         														#decomposed example plot
fname='V4_plott_smoothed.pdf'
matplotlib.pyplot.savefig(fname)

h=(pysqldf("SELECT max(V4) as bpm from file WHERE `sample interval`<1000 AND `sample interval`>100")+pysqldf("SELECT min(V4) as bpm from file WHERE `sample interval`<1000 AND `sample interval`>100"))/2
peaks=scipy.signal.find_peaks(coeffs[0],height=float(h.values))
amount=len(peaks[0])
time=(pysqldf("SELECT max(`sample interval`) as bpm from file WHERE `sample interval`<1000 AND `sample interval`>100")-pysqldf("SELECT min(`sample interval`) as bpm from file WHERE `sample interval`<1000 AND `sample interval`>100"))*0.004
bps=amount/time
bpm=bps*60      																				#average myocardial contractions for selected range [beats per minute]
bpm.to_csv(r'bpm.txt',header=None, index=None, sep=' ', mode='w')

ekg=pysqldf("SELECT * from file")
coeffs = pywt.wavedec(ekg.V4, 'db1',level=2)
h=(pysqldf("SELECT max(V4) as bpm from file WHERE `sample interval`<1000 AND `sample interval`>100")+pysqldf("SELECT min(V4) as bpm from file WHERE `sample interval`<1000 AND `sample interval`>100"))/2
peaks=scipy.signal.find_peaks(coeffs[0],height=float(h.values))
amount=len(peaks[0])
time=pysqldf("SELECT max(`sample interval`) as bpm from file")*0.004
bps=amount/time
bpm=bps*60     																					#average myocardial contractions for whole series [beats per minute]
bpm.to_csv(r'bpm.txt',header=None, index=None, sep=' ', mode='a')
