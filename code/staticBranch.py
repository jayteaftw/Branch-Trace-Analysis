
def staticBranch(fileName, taken):
    f = open(fileName, 'r')
    res = []
    for x in f:
        line = x.strip("\n").split(" ")
        res.append(line)
    
    value = 'T' if taken else 'N'
    count = 0
    
    for i in res:
        if i[1] == value: count += 1

    if taken:
        print(f'Static Always Taken:{count},    total:{len(res)}, Miss Prediction: {round((len(res) - count ) / len(res), 3)}')
    else:
        print(f'Static Always Not Taken:{count}, total:{len(res)}, Miss Prediction: {round((len(res) - count ) / len(res), 3)}')

if __name__ == "__main__":
    files = [   "gcc-short.br.txt" , 
                "BranchTraces/art.br.txt", 
                "BranchTraces/mcf.br.txt",
                "BranchTraces/sjeng.br.txt",
                "BranchTraces/sphinx3.br.txt"]
    for names in files:
        print(names)
        staticBranch(names, taken=True)
        staticBranch(names, taken=False)
        print()

