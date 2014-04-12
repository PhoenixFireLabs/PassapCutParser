import sys
import Image
from random import randint
palette = [randint(0,0XFFFFFF) for i in range(0,256)]
def printFile(data) :
    x = 0
    for k in data :
        print(str(x)+":"+str(k))
        x+=1
def printArr(arr) :
    for line in arr : print(line)

def writeImage(arr,rows,cols,infile) :
    img = Image.new( 'RGB', (cols,rows), "white") # create a new black image
    pixels = img.load() # create the pixel map
    for i in range(rows):    # for every pixel:
        for j in range(cols):
            e = arr[i][j]
            rgb = palette[e]
            r = rgb>>16
            g = (rgb>>8)&0xFF
            b = rgb&0xFF
            pixels[j,i] = (r,g,b)
    img.save(infile+".bmp","BMP")

def bytesto16Bit(lsb,msb) :
    assert(type(lsb) == str and type(msb) == str)
    lsb = ord(lsb)
    msb = ord(msb)
    return (msb << 8)+lsb

def strToByte(s) :
    assert(type(s) == str)
    return ord(s)

def readCutFile(infile) :
    f = open(infile,'rb')
    data = f.read()
    cols = bytesto16Bit(data[0],data[1])
    rows = bytesto16Bit(data[2],data[3])
    assert(cols>0)
    assert(rows>0)
    #printFile(data)

    i = 6
    arr = []
    #Read data
    for l in range (0,rows) :
        count = bytesto16Bit(data[i],data[i+1])
        i+=2

        line = [strToByte(c) for c in data[i:i+count]]
        i+=count
        iter = line.__iter__()
        decompressedLine = []
        eol = False

        while not eol :
            byte = iter.next()
            eol = byte==0 or byte==128
            flagbit = byte&0x80
            n = byte&0x7F

            if eol :
                eol = True
                #print("EOL")
            elif flagbit :
                nextbyte = iter.next()
                decompressedLine += [nextbyte]*n
                #print(str(nextbyte)+" "+str(n)+" times")
            else :
                for x in range(0,n) : decompressedLine+=[iter.next()]
        assert(eol)
        arr+=[decompressedLine]
    #printArr(arr)
    writeImage(arr,rows,cols,infile)
    f.close()

for i in range(1,len(sys.argv)) :
    readCutFile(sys.argv[i])

