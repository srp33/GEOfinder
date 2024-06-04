import pandas as pd

        
metadata_dct = {"Species": ["human", "rat"], "Num Samples":["1-10","501-1000"], "Platform":["RNA sequencing"]}
filePath = "dummy_metadatas.tsv"
dataFrame = pd.read_csv(filePath, index_col=0, sep="\t")

print(dataFrame.head(n=15))

for key, value_list in metadata_dct.items():
    dataFrame = dataFrame[dataFrame[key].isin(value_list)]

print(dataFrame.head(n=15))

