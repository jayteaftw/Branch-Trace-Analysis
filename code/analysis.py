
def analysis(fileName):
    f = open(fileName, 'r')
    res = []
    for x in f:
        line = x.strip("\n").split(" ")
        res.append(line)
    
    taken, notTaken = 0, 0
    distinct = set()
    for i in res:
        if i[1] == 'T': taken += 1
        if i[1] == 'N': notTaken += 1
        distinct.add(i[3])
    print(f'taken:{taken}, notTaken:{notTaken}, total:{len(res)}')
    print(distinct)

if __name__ == "__main__":
    files = [   "gcc-short.br.txt" , 
                "BranchTraces/art.br.txt", 
                "BranchTraces/mcf.br.txt",
                "BranchTraces/sjeng.br.txt",
                "BranchTraces/sphinx3.br.txt"]
    for names in files:
        print(names)
        analysis(names)
        print()

