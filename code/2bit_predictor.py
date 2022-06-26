
def twoBitPredictor(fileName):
    f = open(fileName, 'r')
    res = []
    twoBit = [0]*(2**10) #0 , -1 , 2 dont take. 1, 2 or 3 take.
    for x in f:
        line = x.strip("\n").split(" ")
        res.append(line)
    

    correct = 0
    incorrect = 0

    # Convert x least significant bits of a hexadecimal number to an integer
    def hexLastBitsToInt(hex, bits=10):
        binary = bin(int(hex,16))
        binary = binary[-bits:]
        return int(binary, 2)

    conv  = lambda x: 'N' if x in [-2, -1, 0] else 'T'  

    for i in res:
        idx = hexLastBitsToInt(i[0])
        pred = twoBit[idx]
        if i[1] == conv(pred): 
            correct += 1
            twoBit[idx] = min(pred+1, 2) if i[1] == 'T' else max(-1, pred-1)
        else:
            incorrect += 1
            twoBit[idx] += -1 if i[1] == 'N' else 1
        
        print(twoBit[idx])
        

    print(f'{correct + incorrect} == {len(res)}')
    print(f'Dynamic 2 bit Prediction:, total:{len(res)}, Miss Prediction: {round((len(res) - correct ) / len(res), 3)}')

if __name__ == "__main__":
    files = [   "gcc-short.br.txt" , 
                "BranchTraces/art.br.txt", 
                "BranchTraces/mcf.br.txt",
                "BranchTraces/sjeng.br.txt",
                "BranchTraces/sphinx3.br.txt"]
    for names in files:
        print(names)
        twoBitPredictor(names)
        print()
