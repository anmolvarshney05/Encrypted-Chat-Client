import MathBox


class RSA:
    def __init__(self):
        self.sep = chr(8)
        self.left = MathBox.generateLargePrime(100)
        self.right = MathBox.generateLargePrime(100)
        self.phi = (self.left-1)*(self.right-1)
        self.n = self.left*self.right
        self.e = MathBox.PrimeTo(self.phi)
        self.publicKey = (self.e, self.n)
        self.d = MathBox.moduloInv(self.e, self.phi)
        self.privateKey = (self.d, self.n)

    def encrypt(self, M, key):
        M_INT = int(M)
        key = key.split(self.sep)
        E = int(key[0])
        N = int(key[1])
        final = MathBox.modulo(M_INT, E, N)
        return str(final)

    def decrypt(self, M):
        M_INT = int(M)
        final = MathBox.modulo(M_INT, self.d, self.n)
        final = str(final)
        while len(final) < 16:
            final = "0"+final
        return final[0:16]

    def getPublicKey(self):
        string = str(self.e)+self.sep+str(self.n)
        return string
