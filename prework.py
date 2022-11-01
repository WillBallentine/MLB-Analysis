import csv
import urllib2


def main():
    with open('myData.csv', 'w') as f:
        stocks = ['aapl', 'f']
        for stk in stocks:
            myfile = open(stk + '.csv', 'r')
            reader = csv.reader(myfile)
            headers = next(reader, None)
            #print(headers)
            count = 0
            for x in reader:
                f.write(stk + "," + x[0] + "," + x[1] + "," + x[4] + "," + x[6] + "\n")
                count = count + 1
            print count
            myfile.close()
    f.close()
    print("done")





main()