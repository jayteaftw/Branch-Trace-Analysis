
def nBitPredictor(fileName, bits):
    if not isinstance(bits, int): exit("error! Not an int.")
    f = open(fileName, 'r')
    res = []
    addrSpace = [0]*(2**10)

    for x in f:
        line = x.strip("\n").split(" ")
        res.append(line)

    # Convert x least significant bits of a hexadecimal number to an integer
    def hexLastBitsToInt(hex, bits=10):
        binary = bin(int(hex,16))
        binary = binary[-bits:]
        return int(binary, 2)
    
    #Postive numbers without zero (1,2,3,....), Take. 
    #Negative Numbers with 0 (0,-1, -2,......), Dont take
    conv  = lambda x: 'T' if x > 0 else 'N'  

    correct = 0
    incorrect = 0
    for i in res:
        idx = hexLastBitsToInt(i[0])
        pred = addrSpace[idx]
        if i[1] == conv(pred): 
            correct += 1

            #Saturates at 0+bits and 1-bits. 
            #For example, 3 bit predictor saturates at 0+3=3 and 1-3=-2.
            addrSpace[idx] = min(pred+1, 0+bits) if i[1] == 'T' else max(pred-1, 1-bits)
        else:
            incorrect += 1

            #Adds 1 if prediction was supposed to be True. Subtracts 1 if prediction is supposed to be False.
            addrSpace[idx] += -1 if i[1] == 'N' else 1
        
        
    print(f'Dynamic {bits} Bit Prediction:, total:{len(res)}, Miss Prediction: {round((len(res) - correct ) / len(res), 3)}')

if __name__ == "__main__":
    files = [   "gcc-short.br.txt" , 
                "BranchTraces/art.br.txt", 
                "BranchTraces/mcf.br.txt",
                "BranchTraces/sjeng.br.txt",
                "BranchTraces/sphinx3.br.txt"]

    for names in files:
        print(names)
        nBitPredictor(names, 1)
        nBitPredictor(names, 2)
        nBitPredictor(names, 3)
        print()

        