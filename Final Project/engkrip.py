def enkrip(inp, pkey):
    kript = ""
    whiteSpace = 0
    
    for i in range(len(inp)):
        if inp[i].islower():
            kript += chr((((ord(inp[i]) - ord("a")) + (ord(pkey[((i-whiteSpace)%len(pkey))]) - ord("a"))) % 26) + ord("a"))
        elif inp[i].isupper():
            kript += chr((((ord(inp[i]) - ord("A")) + (ord(pkey[((i-whiteSpace)%len(pkey))]) - ord("a"))) % 26) + ord("A"))
        elif inp[i] == " ":
            kript += " "
            whiteSpace += 1
        else:
            kript += inp[i]
                        
    return kript


def dekrip(inp, pkey):
    kript = ""
    whiteSpace = 0
    
    for i in range(len(inp)):
        if inp[i].islower():
            kript += chr((((ord(inp[i]) - ord("a")) - (ord(pkey[((i-whiteSpace)%len(pkey))]) - ord("a"))) % 26) + ord("a"))
        elif inp[i].isupper():
            kript += chr((((ord(inp[i]) - ord("A")) - (ord(pkey[((i-whiteSpace)%len(pkey))]) - ord("a"))) % 26) + ord("A"))
        elif inp[i] == " ":
            kript += " "
            whiteSpace += 1
        else:
            kript = inp[i]
            
    return kript


def privkey(sender, receiver):
    i = 0
    j = 0
    key = ""
    
    while i<len(sender) and j<len(receiver):
        if (i+j) % 2 == 0:
            key += f"{sender[i]}"
            i += 1
        else:
            key += f"{receiver[j]}"
            j += 1
    
    key = enkrip(key, key)
            
    return key

sender, receiver = input().split()
ende = int(input())
inp = str(input())
    
if ende == 1:
    kript = enkrip(enkrip(enkrip(inp, privkey(sender, receiver)), privkey(sender, receiver)), privkey(sender, receiver))
elif ende == 0:
    kript = dekrip(dekrip(dekrip(inp, privkey(sender, receiver)), privkey(sender, receiver)), privkey(sender, receiver))

    
print(kript)