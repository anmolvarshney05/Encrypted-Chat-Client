from collections import deque
from random import randint


class BREA:
    def __init__(self):
        self.length = 0
        self.row = 0
        self.column = 0
        self.Arrays = []
        self.CharArray = [[], [], [], []]
        self.temp = []
        self.mappings = {}
        self.mappings2 = {}
        self.temp2 = [[], [], [], []]
        self.Ke = [[], [], [], []]
        self.Cpk = []
        self.text = ''
        self.stringkey = ''
        self.stringencrypt = ''
        self.stringdecrypt = ''
        self.gen_mappings()
        self.generateKe()

    def read_text(self):
        self.length = 0
        self.row = 0
        self.column = 0
        for i in self.text:
            character = i
            if self.length >= 16:
                self.Arrays.append(self.CharArray)
                self.CharArray = [[], [], [], []]
                self.length = 0
                self.row = 0
                self.column = 0
            if self.column >= 4:
                self.column = 0
                self.row += 1
            self.CharArray[self.row].append(character)
            self.column += 1
            self.length += 1

    def remain_fill(self):
        if self.length <= 16:
            while self.length < 16:
                if self.column >= 4:
                    self.row += 1
                    self.column = 0
                self.CharArray[self.row].append(chr(240))
                self.length += 1
                self.column += 1
            self.Arrays.append(self.CharArray)

    def invremain_fill(self):
        last = len(self.Arrays)
        for lists in self.Arrays[last - 1]:
            for index, value in enumerate(lists):
                if value == chr(240):
                    lists[index] = None

    def gen_mappings(self):
        for i in range(0, 255, 1):
            self.mappings[chr(i)] = i
            self.mappings2[i] = chr(i)

    def substituteM(self):
        for CharArrays in self.Arrays:
            for lists in CharArrays:
                for index, value in enumerate(lists):
                    lists[index] = self.mappings.get(value)

    def invsubstituteM(self):
        for CharArrays in self.Arrays:
            for lists in CharArrays:
                for index, value in enumerate(lists):
                    lists[index] = self.mappings2.get(value)

    def transposeM(self):
        self.temp = []
        for CharArrays in self.Arrays:
            CharAr = map(list, zip(*CharArrays))
            self.temp.append(CharAr)
        self.Arrays = self.temp

    def generateKe(self):
        self.length = 0
        self.row = 0
        self.column = 0
        while self.length < 16:
            if self.column >= 4:
                self.column = 0
                self.row += 1
            self.Ke[self.row].append(randint(1, 26) % 9)
            self.column += 1
            self.length += 1

    def generateKefromText(self, text):
        self.Ke = [[], [], [], []]
        self.length = 0
        self.row = 0
        self.column = 0
        for i in text:
            if self.column >= 4:
                self.column = 0
                self.row += 1
            self.Ke[self.row].append(int(i))
            self.column += 1
            self.length += 1

    def addMpTandKe(self):
        self.temp = []
        self.temp2 = []
        lister = []
        for CharArrays in self.Arrays:
            for (Arr, K) in zip(CharArrays, self.Ke):
                for (val, val2) in zip(Arr, K):
                    lister.append((val + val2) % 256)
                self.temp2.append(lister)
                lister = []
            self.temp.append(self.temp2)
            self.temp2 = []
        self.Cpk = self.temp

    def invaddMpTandKe(self):
        self.temp = []
        self.temp2 = []
        lister = []
        for CharArrays in self.Cpk:
            for (Arr, K) in zip(CharArrays, self.Ke):
                for (val, val2) in zip(Arr, K):
                   lister.append((val - val2 + 256) % 256)
                self.temp2.append(lister)
                lister = []
            self.temp.append(self.temp2)
            self.temp2 = []
        self.Arrays = self.temp

    def rotate_hor(self):
        for fourDArray in self.Cpk:
            d = deque(fourDArray[0])
            d1 = deque(fourDArray[1])
            d2 = deque(fourDArray[2])
            d.rotate(-1)
            d1.rotate(-2)
            d2.rotate(-3)
            fourDArray[0] = list(d)
            fourDArray[1] = list(d1)
            fourDArray[2] = list(d2)

    def invrotate_hor(self):
        for fourDArray in self.Cpk:
            d = deque(fourDArray[0])
            d1 = deque(fourDArray[1])
            d2 = deque(fourDArray[2])
            d.rotate(1)
            d1.rotate(2)
            d2.rotate(3)
            fourDArray[0] = list(d)
            fourDArray[1] = list(d1)
            fourDArray[2] = list(d2)

    def rotate_ver(self):
        self.temp = []
        for fourDArray in self.Cpk:
            fourD = map(list, zip(*fourDArray))
            self.temp.append(fourD)
        self.Cpk = self.temp
        self.rotate_hor()
        self.temp = []
        for fourDArray in self.Cpk:
            fourD = map(list, zip(*fourDArray))
            self.temp.append(fourD)
        self.Cpk = self.temp

    def invrotate_ver(self):
        self.temp = []
        for fourDArray in self.Cpk:
            fourD = map(list, zip(*fourDArray))
            self.temp.append(fourD)
        self.Cpk = self.temp
        self.invrotate_hor()
        self.temp = []
        for fourDArray in self.Cpk:
            fourD = map(list, zip(*fourDArray))
            self.temp.append(fourD)
        self.Cpk = self.temp

    def makeCe(self):
        for fourDArray in self.Cpk:
            for lists in fourDArray:
                for index, value in enumerate(lists):
                    lists[index] = self.mappings2.get(value)

    def invmakeCe(self):
        for fourDArray in self.Cpk:
            for lists in fourDArray:
                for index, value in enumerate(lists):
                    lists[index] = self.mappings.get(value)

    def getKey(self):
        self.stringkey = ''
        for linearArray in self.Ke:
            for charac in linearArray:
                self.stringkey += str(charac)
        return self.stringkey

    def encrypt(self, text):
        self.CharArray = [[], [], [], []]
        self.Arrays = []
        self.text = text
        self.read_text()
        self.remain_fill()
        self.substituteM()
        self.transposeM()
        self.addMpTandKe()
        self.rotate_hor()
        self.rotate_ver()
        self.makeCe()
        self.stringencrypt = ''
        for fourDArray in self.Cpk:
            for lists in fourDArray:
                for charac in lists:
                    self.stringencrypt += str(charac)
        return self.stringencrypt

    def decrypt(self, text, key):
        self.generateKefromText(key)
        self.CharArray = [[], [], [], []]
        self.Arrays = []
        self.text = text
        self.read_text()
        self.remain_fill()
        self.Cpk = self.Arrays
        self.invmakeCe()
        self.invrotate_ver()
        self.invrotate_hor()
        self.invaddMpTandKe()
        self.transposeM()
        self.invsubstituteM()
        self.invremain_fill()
        self.stringdecrypt = ''
        for fourDArray in self.Arrays:
            for lists in fourDArray:
                for charac in lists:
                    if charac is None:
                        continue
                    self.stringdecrypt += str(charac)
        return self.stringdecrypt



