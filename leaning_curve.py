import numpy as np
import matplotlib.pyplot as plt
file = open('history.dat',mode='r')
all_data=file.read().split(" ")
file.close()
minimums=[]
averages=[]
maximums=[]
for i in range(0,len(all_data)-1,3):
    minimums.append(float(all_data[i]))
    averages.append(float(all_data[i+1]))
    maximums.append(float(all_data[i+2]))

generations=np.arange(0,len(averages),1)
plt.plot(generations,minimums,'r',label='minimum')
plt.plot(generations,averages,'b',label='average')
plt.plot(generations,maximums,'g',label='maximums')
plt.legend()
plt.show()