def u8(msg):
    s=""
    for i in range(len(msg)):
        if i%2==0:
            s+=msg[i]
    return s
def u16(msg):
    s=""
    for i in msg:
        s+=i
        s+=" "