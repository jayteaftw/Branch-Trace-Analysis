
def oneBitPredictor(fileName):
    f = open(fileName, 'r')
    res = []
    for x in f:
        line = x.strip("\n").split(" ")
        res.append(line)
    
    oneBit = ['N']*(2**10)
    correct = 0
    incorrect = 0

    # Convert x least significant bits of a hexadecimal number to an integer
    def hexLastBitsToInt(hex, bits=10):
        binary = bin(int(hex,16))
        #print(binary)
        binary = binary[-bits:]
        #print(binary)
        return int(binary, 2)

    for i in res:
        idx = hexLastBitsToInt(i[0])
        if i[1] == oneBit[idx]: 
            correct += 1
        else:
            oneBit[idx] = i[1]
            incorrect += 1

    print(f'{correct + incorrect} == {len(res)}')
    print(f'Dynamic 1 Bit Prediction:, total:{len(res)}, Miss Prediction: {round((len(res) - correct ) / len(res), 3)}')

if __name__ == "__main__":
    files = [   "gcc-short.br.txt" , 
                "BranchTraces/art.br.txt", 
                "BranchTraces/mcf.br.txt",
                "BranchTraces/sjeng.br.txt",
                "BranchTraces/sphinx3.br.txt"]
    for names in files:
        print(names)
        oneBitPredictor(names)
        print()
        #exit()