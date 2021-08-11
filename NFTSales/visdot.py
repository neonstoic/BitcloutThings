import math

# Run output from this in https://visjs.github.io/vis-network/examples/network/data/dotLanguage/dotPlayground.html#

f = open('nft_sells.csv', 'r')
f2 = open('nft_sells_dotlang.txt', 'w')
c = 0

f2.write('digraph G {\n ranksep=3;\n ratio=auto;\n')

for l in f.readlines():
    c += 1
    if c > 1:
        tokens=l.split(',')
        p = float(tokens[1])
        p = p / 1000000
        p = math.trunc(p)
        p = p / 1000
        s = tokens[4] + ' -> ' + tokens[5] + ' [label="' + str(p) + '"]'
        f2.write(' ' + s + '\n')
        #if(c > 10):
        #    break
f.close()

f2.write('}')
f2.close()