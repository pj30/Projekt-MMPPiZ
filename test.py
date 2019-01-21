from MTP import getRawData, solve
import pandas as pd
resultlist=[]
objval,resultlist=solve()
print(objval)
print(resultlist)
pd.DataFrame(resultlist).to_csv('output.csv', header=False, index=False)
