# Convert x least significant bits of a hexadecimal number to an integer
def hexLastBitsToInt(hex, bits=10):
    binary = bin(int(hex,16))
    binary = binary[-bits:]
    return int(binary, 2)

#Shift string from left to right with new value. Ex: 1 >> 0100 = 1010
def shiftString(string, newVal):
        string = str(newVal)+string[:-1]
        return string

#Convert binary to int
def binToInt(bin):
    return int(bin,2)

def Correlation(fileName):
    f = open(fileName, 'r')
    res = []
    for x in f:
        line = x.strip("\n").split(" ")
        res.append(line)
    
    addrSpace = [[0]*(2**5) for i in range((2**5))]
   
    
    #Postive numbers without zero (1,2,3,....), Take. 
    #Negative Numbers with 0 (0,-1, -2,......), Dont take
    conv  = lambda x: 'T' if x > 0 else 'N'
   
    correct = 0
    incorrect = 0

    #Shift Register with size equal to 5
    shiftReg = '0'*5 
    for i in res:
        idxSelectedAddrBits = hexLastBitsToInt(i[0], bits=5)
        
        idxShiftReg = binToInt(shiftReg)
        #print(i[0], idxSelectedAddrBits, idxShiftReg)


        pred = addrSpace[idxSelectedAddrBits][idxShiftReg]
        actual = 1 if i[1] == 'T' else 0
        
        if actual == pred: 
            correct += 1
        else:
            addrSpace[idxSelectedAddrBits][idxShiftReg] = actual
            incorrect += 1


        #Shift the shift register with the actual case
        shiftReg = shiftString(shiftReg, actual)

        """     for i in addrSpace:
        print(i) """
        
    print(f'Correlation Prediction:, total:{len(res)}, Miss Prediction: {round((len(res) - correct ) / len(res), 3)}')

def Gshare(fileName):
    f = open(fileName, 'r')
    res = []
    for x in f:
        line = x.strip("\n").split(" ")
        res.append(line)
    
    addrSpace = [0]*(2**10)
    addrSpace = [0 for i in range((2**10))]

    #Postive numbers without zero (1,2,3,....), Take. 
    #Negative Numbers with 0 (0,-1, -2,......), Dont take
    conv  = lambda x: 'T' if x > 0 else 'N'
    
    correct = 0
    incorrect = 0

    #Shift Register with size equal to 10
    shiftReg = '0'*10
    for i in res:
        idxSelectedAddrBits = hexLastBitsToInt(i[0], bits=10)
        idxShiftReg = binToInt(shiftReg)

        #Set index to xor of Shift Register and the Selected Address Bits
        idx = idxShiftReg ^ idxSelectedAddrBits

        pred = addrSpace[idx]
        
        actual = 1 if i[1] == 'T' else 0
        if actual == pred: 
            correct += 1
        else:
            addrSpace[idx] = actual
            incorrect += 1

        #Shift the shift register with the actual case
        shiftReg = shiftString(shiftReg,actual)

        
    print(f'Gshare Prediction:, total:{len(res)}, Miss Prediction: {round((len(res) - correct ) / len(res), 3)}')


if __name__ == "__main__":
    files = [   "gcc-short.br.txt" , 
                "BranchTraces/art.br.txt", 
                "BranchTraces/mcf.br.txt",
                "BranchTraces/sjeng.br.txt",
                "BranchTraces/sphinx3.br.txt"]

    for names in files:
        print(names)
        Correlation(names)
        Gshare(names)
        print()