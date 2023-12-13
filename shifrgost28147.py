def block2ns(data):
    return (
        int.from_bytes((data[0:4][::-1]), byteorder='big', signed=False),
        int.from_bytes((data[4:9][::-1]), byteorder='big', signed=False)
    )

def ns2block(ns):
    n1, n2 = ns
    return n2.to_bytes(4,"big")[::-1]+n1.to_bytes(4,"big")[::-1]






#https://internet-law.ru/gosts/gost/11287/
porydok_schitivania = (
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    0, 1, 2, 3, 4, 5, 6, 7,
    7, 6, 5, 4, 3, 2, 1, 0,
)



def _K(s, _in):#функция замены, делим 32 на 4 блока по 8 бит, делаем цикл с заменой сразу 2 значений, потому что берем по 4 бит а мы поделили на байты, сдвигаем и плюсаем

    j = _in.to_bytes(4, "big")[::-1]
    ready=0
    for k in range(0,4):
        c2=int('{0:08b}'.format(j[k])[0:4],2)
        c1=int('{0:08b}'.format(j[k])[4:8],2)
        ready+=(s[k*2][c1] << k*8)+ (s[k*2+1][c2] << k*8+4)
    return ready

def cyqil_sdvig_11(x):
    return ((x << 11) & (2 ** 32 - 1)) | ((x >> (32 - 11)) & (2 ** 32 - 1))

def mod_2_values(x, y, mod=2 ** 32):
    r = x + y
    return r if r < mod else r - mod



def encrypt(sbox, key, ns):
    s = sbox
    x = [int.from_bytes((key[4*i:4*i+4][::-1]), byteorder='big', signed=False) for i in range(8)]#2.1.2 делим 256 бит на 8 участков по 32 бита

    n1, n2 = ns
    for i in porydok_schitivania:
        n1, n2 = cyqil_sdvig_11(_K(s, mod_2_values(n1, x[i]))) ^ n2, n1

    return n1, n2