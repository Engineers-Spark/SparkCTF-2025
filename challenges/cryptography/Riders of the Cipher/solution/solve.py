
with open('output.txt') as f:
    enc = f.read().split('\n')

freq = {}
for i in enc:
    if i in freq:
        freq[i] += 1
    else:
        freq[i] = 1

a = ((sorted(freq.items(), key=lambda item: item[1], reverse=True)))
ll = [i[0] for i in a]
char_freq = ' etaoinshrduwmfcgypblvkxqz????'
for i in enc:
    print(char_freq[ll.index(i)], end='')


### to get the flag u just need to put the output here https://quipqiup.com