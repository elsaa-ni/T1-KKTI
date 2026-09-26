class Rotor:
    def __init__(self, wiring, notch):
        self.wiring = wiring
        self.notch = notch
        self.ring = 0
        self.pos = 0

    def step(self):
        self.pos = (self.pos + 1) % 26

    def is_at_notch(self):
        return chr(self.pos + ord('A')) == self.notch

    def forward(self, c):
        shift = self.pos - self.ring
        idx = (c + shift) % 26
        out_char = self.wiring[idx]
        return (ord(out_char) - ord('A') - shift) % 26

    def backward(self, c):
        shift = self.pos - self.ring
        idx = (c + shift) % 26
        out_char = chr(idx + ord('A'))
        out_idx = self.wiring.index(out_char)
        return (out_idx - shift) % 26

class Enigma:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def step_rotors(self):
        left, middle, right = self.rotors
        
        middle_notch = middle.is_at_notch()
        right_notch = right.is_at_notch()
        
        if middle_notch:
            left.step()
            middle.step()
            right.step()
        elif right_notch:
            middle.step()
            right.step()
        else:
            right.step()

    def process(self, text):
        res = ""
        for char in text:
            if not char.isalpha(): continue
            self.step_rotors()
            
            c = ord(char) - ord('A')
            c = self.plugboard.get(c, c)
            
            for rotor in reversed(self.rotors):
                c = rotor.forward(c)
                
            c = self.reflector[c]
            
            for rotor in self.rotors:
                c = rotor.backward(c)
                
            c = self.plugboard.get(c, c)
            res += chr(c + ord('A'))
        return res

wiring = {
    'I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
    'II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
    'III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
}
notches = {'I': 'Q', 'II': 'E', 'III': 'V'}

# Urutan Rotor (Kiri ke Kanan): II, I, III
left = Rotor(wiring['II'], notches['II'])
middle = Rotor(wiring['I'], notches['I'])
right = Rotor(wiring['III'], notches['III'])

# Ring Setting (Kanan ke Kiri: W, U, H) -> Kiri=H, Tengah=U, Kanan=W
left.ring = ord('H') - ord('A')
middle.ring = ord('U') - ord('A')
right.ring = ord('W') - ord('A')

# Posisi awal (Kanan ke Kiri: R, M, Q) -> Kiri=Q, Tengah=M, Kanan=R
left.pos = ord('Q') - ord('A')
middle.pos = ord('M') - ord('A')
right.pos = ord('R') - ord('A')

# Reflector B (Standar)
reflector_B = [ord(c) - ord('A') for c in 'YRUHQSLDPXNGOKMIEBFZCWVJAT']

# Plugboard: V-M, Q-B
pb_pairs = ['VM', 'QB']
plugboard = {}
for a, b in pb_pairs:
    plugboard[ord(a)-ord('A')] = ord(b)-ord('A')
    plugboard[ord(b)-ord('A')] = ord(a)-ord('A')

# Inisiasi dan Eksekusi
enigma = Enigma([left, middle, right], reflector_B, plugboard)
ciphertext = "BBQAOTHROVNXFJVTWJSOLGTDPLHRCMTQXDEGAOJIK"
print("Plaintext:", enigma.process(ciphertext))