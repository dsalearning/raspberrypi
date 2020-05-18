#/usr/bin/python3.7

i = 9
def doOneThing():
    i=10
    print("doOneThing's i=",i)
    
if __name__ == '__main__':
    i = 20
    doOneThing()
    print("i=",i)    

    