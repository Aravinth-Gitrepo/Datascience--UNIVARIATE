class univariates:
    
        def quanQual(self,dataset):
            Quan=[]
            Qual=[]
            for columnName in dataset.columns:
                if dataset[columnName].dtypes=="O":
                    #print('Qual', columnName)
                    Qual.append(columnName)
                else:
                    #print('Quan',columnName)
                    Quan.append(columnName)
            return Quan, Qual

        def descriptive (dataset,Quan):
            descriptive=pd.DataFrame(index=['mean','median','mode','Q1:25%','Q2:50%','Q3:75%','Q4:100%','99%','IQR','1.5RULE','LESSER IQR','GREATER IQR','MIN','MAX','skew','kurtosis','var','std'],columns=Quan)
        
            for columnName in Quan:
                descriptive[columnName]['mean']=(dataset[columnName].mean())
                descriptive[columnName]['median']=(dataset[columnName].median())
                descriptive[columnName]['mode']=(dataset[columnName].mode()[0])
                #descriptive[columnName]['Q1:25']=np.percentile(dataset['ssc_p'],25)
                descriptive[columnName]['Q1:25%']=dataset.describe()[columnName]['25%']
                descriptive[columnName]['Q2:50%']=dataset.describe()[columnName]['50%']
                descriptive[columnName]['Q3:75%']=dataset.describe()[columnName]['75%']
                descriptive[columnName]['Q4:100%']=dataset.describe()[columnName]['max']
                descriptive[columnName]['99%']=np.percentile(dataset[columnName],99)
                descriptive[columnName]['IQR']= descriptive[columnName]['Q3:75%']-descriptive[columnName]['Q1:25%']
                descriptive[columnName]['1.5RULE']=1.5*descriptive[columnName]['IQR']
                descriptive[columnName]['LESSER IQR']=descriptive[columnName]['Q1:25%']- descriptive[columnName]['1.5RULE']
                descriptive[columnName]['GREATER IQR']=descriptive[columnName]['Q3:75%']+ descriptive[columnName]['1.5RULE']
                descriptive[columnName]['MIN']=dataset[columnName].min()
                descriptive[columnName]['MAX']=dataset[columnName].max()
                descriptive[columnName]['skew']=(dataset[columnName].skew())
                descriptive[columnName]['kurtosis']=(dataset[columnName].kurtosis())
                descriptive[columnName]['var']=(dataset[columnName].var())
                descriptive[columnName]['std']=(dataset[columnName].std())
            return descriptive

    
        def IQRcomparison(Quan,descriptive):
            lesser=[]
            greater=[]           
            for columnName in Quan:
                if descriptive[columnName]['MIN']<descriptive[columnName]['LESSER IQR']:
                    lesser.append(columnName)
                if descriptive[columnName]['MAX']>descriptive[columnName]['GREATER IQR']:
                    greater.append(columnName)
            return lesser,greater

        def Outlier_replacement(dataset,descriptive):
            for columnName in lesser:
                dataset[columnName] [dataset[columnName]<descriptive[columnName]['LESSER IQR']]=descriptive[columnName]['LESSER IQR']
            for columnName in greater:
                dataset[columnName] [dataset[columnName]>descriptive[columnName]['GREATER IQR']]=descriptive[columnName]['GREATER IQR']
            return dataset

        def freqtable(dataset,columnName):            
            freqtable=pd.DataFrame(columns=["uniquevalues","Frequency","Relative_Freq","Cumulative_Freq"])
            freqtable['uniquevalues']=dataset[columnName].value_counts().index
            freqtable['Frequency']=dataset[columnName].value_counts().values
            freqtable['Relative_Freq']=(freqtable['Frequency']/len(dataset))
            freqtable['Cumulative_Freq']=freqtable['Relative_Freq'].cumsum()
            return freqtable