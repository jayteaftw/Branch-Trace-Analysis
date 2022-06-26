import fuckit
import time

#Global array for fetch target queue (FTQ), GShare
FTQ = []

addressBits = 10
GShareAddrSpace = [0 for i in range((2**addressBits))]
nBitAddrSpace = [0]*(2**addressBits)


@fuckit
def removeFromArray(upperBound):
    del FTQ[upperBound-1]
    del FTQ[upperBound-2]
    del FTQ[upperBound-3]

# Convert x least significant bits of a hexadecimal number to an integer
def hexLastBitsToInt(hex, bits=5):
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

def nBitPredictor(res, bits, lowerBound, upperBound, selectedAddrBits, flag):
    #Postive numbers without zero (1,2,3,....), Take.
    #Negative Numbers with 0 (0,-1, -2,......), Dont take
    conv  = lambda x: 'T' if x > 0 else 'N'

    []
    ['T']
    ['T', 'F']
    ['T', 'F', 'T']
    for i in res[slice(lowerBound, upperBound)]:
        idx = hexLastBitsToInt(i[0])
        pred = nBitAddrSpace[idx]

        convPred = conv(pred)

        if i[1] == convPred:
            #Saturates at 0+bits and 1-bits.
            #For example, 3 bit predictor saturates at 0+3=3 and 1-3=-2.
            nBitAddrSpace[idx] = min(pred+1, 0+bits) if i[1] == 'T' else max(pred-1, 1-bits)
        else:
            #Adds 1 if prediction was supposed to be True. Subtracts 1 if prediction is supposed to be False.
            nBitAddrSpace[idx] += -1 if i[1] == 'N' else 1
        #critiques.append(convPred)

    #If branch future only has 3 branches (nearing end of branch array)
    if not flag:
        if upperBound == len(res)-3:
            #Replace prophet's prediction with critic's, flush FTQ future branch, and redirect prophet's predictions
            if FTQ[upperBound-3] != convPred:
                removeFromArray(upperBound)
                FTQ[upperBound-3] = convPred
                GShareAddrSpace[selectedAddrBits] = 1 if convPred == 'T' else 0

        #If branch future only has 2 branches (nearing end of branch array)
        elif upperBound == len(res)-2:
            #Replace prophet's prediction with critic's, flush FTQ future branch, and redirect prophet's predictions
            if FTQ[upperBound-2] != convPred:
                removeFromArray(upperBound)
                FTQ[upperBound-2] = convPred
                GShareAddrSpace[selectedAddrBits] = 1 if convPred == 'T' else 0

        #If branch future only has 1 branch (nearing end of branch array)
        elif upperBound == len(res)-1:
            #Replace prophet's prediction with critic's, flush FTQ future branch, and redirect prophet's predictions
            if FTQ[upperBound-1] != convPred:
                FTQ[upperBound-1] = convPred
                GShareAddrSpace[selectedAddrBits] = 1 if convPred == 'T' else 0

    #Branch future has all four branches
    else:
        #Replace prophet's prediction with critic's, flush FTQ future branch, and redirect prophet's predictions
        if FTQ[upperBound-4] != convPred:
            removeFromArray(upperBound)
            FTQ[upperBound-4] = convPred
            GShareAddrSpace[selectedAddrBits] = 1 if convPred == 'T' else 0

def Gshare(res, upperBound):

    #Postive numbers without zero (1,2,3,....), Take.
    #Negative Numbers with 0 (0,-1, -2,......), Dont take
    conv  = lambda x: 'T' if x > 0 else 'N'

    correct = 0
    incorrect = 0
    counter = 0
    branchFuture = 0

    #Shift Register with size equal to 10
    shiftReg = '0'*5

    iter = 0
    start_time = time.time() 
    for i in res[slice(0, upperBound)]:
        idxSelectedAddrBits = hexLastBitsToInt(i[0], bits=10)
        idxShiftReg = binToInt(shiftReg)

        #Set index to xor of Shift Register and the Selected Address Bits
        idx = idxShiftReg ^ idxSelectedAddrBits

        pred = GShareAddrSpace[idx]
        convPred = conv(pred)

        #Only make prediction and add to array if not already in it
        try:
            FTQ[counter]
        except IndexError:
            FTQ.append(convPred)
            actual = 1 if i[1] == 'T' else 0
            if actual == pred:
                correct += 1
            else:
                GShareAddrSpace[idx] = actual
                incorrect += 1
            branchFuture +=1

            #If the branch future == 4, call on critic
            if (branchFuture > 3 and counter < len(res)-4):
                nBitPredictor(res, 3, counter-1, counter, idxSelectedAddrBits, 0)
                branchFuture = 0
            elif (counter >= len(res)-4):
                nBitPredictor(res, 3, counter-1, counter, idxSelectedAddrBits, 1)

            #Shift the shift register with the actual case
            shiftReg = shiftString(shiftReg,actual)
        counter+=1

        iter+=1
        if(counter == 1 or iter  == 10**6):
            check_time = time.time()

            timePerIter = (check_time - start_time)/iter
            total_iter = len(res[slice(0, upperBound)])
            Minutes, Seconds = divmod((total_iter - counter)*timePerIter, 60)
            Hours, Minutes = divmod(Minutes, 60)
            print(f"{counter}/{total_iter}. Left: {total_iter - counter} Est Time Left Hours: {Hours}, Minutes: {Minutes}, Seconds: {Seconds}")
            iter = 0
            start_time = time.time() 

def ProphetCritic(res):
    correct = 0
    incorrect = 0
    counter = 0

    Gshare(res, len(res))

    for i in res:
        try:
            FTQ[counter]
        except IndexError:
            pass
        else:
            if i[1] == FTQ[counter]:
                correct+=1
            else:
                incorrect+=1
            counter+=1

    print(f'Prophet-Critic Prediction:, total:{len(FTQ)}, Miss Prediction: {round(incorrect / len(res), 3)}')

if __name__ == "__main__":
    files = [   "gcc-short.br.txt",
                "BranchTraces/art.br.txt",
                "BranchTraces/mcf.br.txt",
                "BranchTraces/sjeng.br.txt",
                "BranchTraces/sphinx3.br.txt"
            ]
    for names in files:
        print(names)
        GShareAddrSpace = [0 for i in range((2**addressBits))]
        nBitAddrSpace = [0]*(2**addressBits)
        FTQ = []
        f = open(names, 'r')
        res = []
        for x in f:
            line = x.strip("\n").split(" ")
            res.append(line)
        print('Running...')

        ProphetCritic(res)
        print()
