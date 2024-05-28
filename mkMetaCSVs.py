import csv
import random



def make_csv(val_lst, file_name):
    # Generate 100 random values
    data = [random.choice(val_lst) for _ in range(100)]
    
    # Writing data to a CSV file
    with open(file_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    

if __name__ == '__main__':
    # Possible values
    make_csv(["human", "mouse", "rat"], "testMetasSpec.csv")

    make_csv(["1-10", "11-50", "51-100", "101-500", "501-1000", "1000+"], "testMetasNumSp.csv")

    make_csv(["RNA sequencing", "Microarray"], "testMetasPlatf.csv")


    
