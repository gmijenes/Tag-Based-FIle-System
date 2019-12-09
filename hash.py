from datetime import datetime

def hash():
    now = datetime.now()
    s = tobin(now.day)

def toBin(n):
    i = 7
    s = ''
    while(i >= 0):
        s+= str(int(n / (2 ** i)))
        n = n % (2 ** i)
        i = i - 1
    return s
    


    
