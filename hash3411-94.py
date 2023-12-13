from shifrgost28147 import block2ns
from shifrgost28147 import encrypt
from shifrgost28147 import ns2block


uzl_zamen_28147 = (
        (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
        (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
        (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
        (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
        (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
        (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
        (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
        (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
    )

blocksize=32 #8*32=256 bit
C2 = bytes.fromhex(64*"0")
C3 = bytes.fromhex('ff00ffff000000ffff0000ff00ffff0000ff00ff00ff00ffff00ff00ff00ff00')
C4=  bytes.fromhex(64*"0")




def xor(first: bytes, second: bytes) -> bytes:
    maxi=max(len(first),len(second))
    if maxi>len(first):
        first = b'\x00' * (maxi - len(first)) + first

    if maxi>len(second):
        second = b'\x00' * (maxi - len(second)) + second

    #print(len(first),len(second))
    jjj=bytes(i ^ b for (i, b) in zip(first, second))

    # jjj=bytearray(jjj)
    # jjj.reverse()
    return jjj





def func_mix_transformation(Y):
    #делим на 16 массивов по 2
    (y16, y15, y14, y13, y12, y11, y10, y9, y8, y7, y6, y5, y4, y3, y2, y1) = (
        Y[0:2], Y[2:4], Y[4:6], Y[6:8], Y[8:10], Y[10:12], Y[12:14],
        Y[14:16], Y[16:18], Y[18:20], Y[20:22], Y[22:24], Y[24:26],
        Y[26:28], Y[28:30], Y[30:32],
    )
    #теперь нужно сделать ксор с y1, y2, y3, y4, y13, y16. в byx записываем результат
    by1, by2, by3, by4, by13, by16, byx = (
        bytearray(y1), bytearray(y2), bytearray(y3), bytearray(y4),
        bytearray(y13), bytearray(y16), bytearray(2),
    )
    byx[0] = by1[0] ^ by2[0] ^ by3[0] ^ by4[0] ^ by13[0] ^ by16[0]
    byx[1] = by1[1] ^ by2[1] ^ by3[1] ^ by4[1] ^ by13[1] ^ by16[1]
    res=b''.join((bytes(byx), y16, y15, y14, y13, y12, y11, y10, y9, y8, y7, y6, y5, y4, y3, y2))
    return res

def A(x): #Делим на 4 части, в обратном порядке записываем перемеенные  и возвраащаем в (x1 XOR x2)+ x4 + x3 + x2
    x4, x3, x2, x1 = x[0:8], x[8:16], x[16:24], x[24:32]
    return b''.join((xor(x1, x2), x4, x3, x2))

def P(x):#256 надо разбить на 32, но у нас уже разбито, поэтому не требуется
    return bytearray((
        x[0], x[8], x[16], x[24], x[1], x[9], x[17], x[25], x[2],
        x[10], x[18], x[26], x[3], x[11], x[19], x[27], x[4], x[12],
        x[20], x[28], x[5], x[13], x[21], x[29], x[6], x[14], x[22],
        x[30], x[7], x[15], x[23], x[31],
    ))

def int_to_bytes(integer):
    return integer.to_bytes((integer.bit_length() + 7) // 8, 'big')


def MainStep(h, m):
    # print("=============")
    u = h
    v = m
    w = xor(u, v)
    k1 = P(w)
    # print(k1.hex())
    # print("h",h.hex())
    # print("m",m.hex())
    # print()



    u = xor(A(u), C2)
    # print(u.hex())
    # print(v.hex())
    v = A(A(v))
    w = xor(u, v)
    k2 = P(w)
    # print(k2.hex())
    # input()

    u = xor(A(u), C3)
    v = A(A(v))
    w = xor(u, v)
    k3 = P(w)

    u = xor(A(u), C4)
    v = A(A(v))
    w = xor(u, v)
    k4 = P(w)

    # print(k1.hex())
    # print(k2.hex())
    # print(k3.hex())
    # print(k4.hex())




    # Encipher
    h4, h3, h2, h1 = h[0:8], h[8:16], h[16:24], h[24:32]  # разбиваем с конца на 4 массива по 64 бит

    s1 = ns2block(encrypt(uzl_zamen_28147, k1[::-1], block2ns(h1[::-1])))[::-1]
    s2 = ns2block(encrypt(uzl_zamen_28147, k2[::-1], block2ns(h2[::-1])))[::-1]
    s3 = ns2block(encrypt(uzl_zamen_28147, k3[::-1], block2ns(h3[::-1])))[::-1]
    s4 = ns2block(encrypt(uzl_zamen_28147, k4[::-1], block2ns(h4[::-1])))[::-1]

    # print(s1.hex())
    # print(s2.hex())
    # print(s3.hex())
    # print(s4.hex())
    # input()

    s = b''.join((s4, s3, s2, s1))  # соединяем



    # https://disk.yandex.ru/i/nU2KuRsPty5AEg
    x = s

    # 5 шаг ПЕРЕМЕШИВАЮЩЕЕ ПРЕОБРАЗОВАНИЕ
    for _ in range(12): x = func_mix_transformation(x)
    x = xor(x, m)

    x = func_mix_transformation(x)
    x = xor (x, h)

    for _ in range(61):
        x = func_mix_transformation(x)
    # print()
    # print("S",s.hex())
    # print()
    # print("X",x.hex())
    # print("=============")
    return x
    # 5 шаг ПЕРЕМЕШИВАЮЩЕЕ ПРЕОБРАЗОВАНИЕ КОНЕЦ


def Hash(data):
    L = 0 # текущее значение длины обработанной на предыдущих итерациях части последовательности М
    Z = 0 # текущее значение контрольной суммы CHECKSUM
    h = bytes.fromhex(64*"0") # текущее значение хеш-функции
    m = data # часть последовательности М, не Прошедшая процедуры хэширования на предыдущих итерациях


    for i in range(0, len(m), blocksize):
        #part = m[i:i + blocksize][::-1]
        part = m[i:i + blocksize]
        L += len(part) * 8
        Z=int.from_bytes(xor(part, int_to_bytes(Z)),"big")

        if len(part) < blocksize:
            part = b'\x00' * (blocksize - len(part)) + part
        h = MainStep(h, part)


    h = MainStep(h, L.to_bytes(32,'big'))#2.6 пункт шага

    Z = Z.to_bytes(32, 'big')  # из числа в байты
    h = MainStep(h, Z)

    # h=bytearray(h)
    # h.reverse()

    return h



message=b'hello'
#message=bytes.fromhex("73657479 62203233 3d687467 6e656c20 2c656761 7373656d 20736920 73696854")
message=bytes.fromhex("73657479622032333d6874676e656c202c6567617373656d2073692073696854")#gost первый тест



#message=bytes.fromhex("4586963702963702d6563737167656c202c656e6764786d33323022697475637")
hashedmes=Hash(message)
print(len(hashedmes.hex()))

print("Result:",hashedmes.hex())

