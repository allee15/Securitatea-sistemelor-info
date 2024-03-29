# -*- coding: utf-8 -*-
"""SSI.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NSwZxE74n729PPavtT6h1G4K6nMrjW3i
"""

# lab 6, ex 1

# 1001 ; 0110
#Acest cod primește coeficienții și starea inițială de la utilizator, apoi
# generează secvența de ieșire și perioada folosind funcția lfsr. În funcția
# lfsr, utilizăm un buclă while pentru a genera următoarea stare din starea curentă,
#folosind operația XOR și o shiftare la dreapta. Continuăm bucla până când starea
#devine 0 sau 1, sau până când starea se repetă.

def lfsr(coef, init_state):
   state = init_state
   period = 0
   while state not in (0, 1) and state not in init_state:
       period += 1
       next_state = 0
       for i in range(len(coef)):
           next_state ^= (coef[i] & (int(''.join(map(str, state)), 2) >> i))
       state = next_state
   return state, period

coef = list(map(int, input("Introduceți coeficienții (separati de spațiu): ").split()))
init_state = list(map(int, input("Introduceți starea inițială (separati de spațiu): ").split()))
state, period = lfsr(coef, init_state)
print("Starea finală este:", state)
print("Perioada este:", period)

#2

from Crypto.Cipher import AES

key = b'0 cheie oarecare'
data = b'testtesttesttesttesttesttesttesttesttesttesttest'
cipher = AES.new(key, AES.MODE_ECB)
cipher.encrypt(data)

#b) Modul de operare folosit este ECB (Electronic Code Book). În acest mod, fiecare bloc
#de date de intrare este criptat independent de celelalte.

#c) Nu ar fi recomandat să se folosească modul ECB pentru criptarea datelor în modul real.
# Acest lucru se datorează problemei cu vizibilitatea blocurilor.

#d) Dimensiunea cheii este de 16 octeți, conform valorii key = b'0 cheie oarecare'.

#e) Pentru a modifica codul astfel încât să funcționeze dacă se înlocuiește valoarea data cu
#data=b'test', trebuie să adaugam padding la datele de intrare pentru a le face de exact 16 octeți.

#f) Pentru a schimba modul de operare cu un alt mod de operare, trebuie să inlocuim AES.MODE_ECB cu alt mod de operare,
# cum ar fi AES.MODE_CBC sau AES.MODE_GCM.

pip install pycryptodome

# 3
from Crypto.Cipher import DES


def encodeText(k: int, text):
    key = format(k, 'x') + '\x00\x00\x00\x00\x00\x00\x00'
    cipher1 = DES.new(key.encode(), DES.MODE_ECB)
    return cipher1.encrypt(text)


def decodeText(k: int, text):
    key = format(k, 'x') + '\x00\x00\x00\x00\x00\x00\x00'
    cipher1 = DES.new(key.encode(), DES.MODE_ECB)
    return cipher1.decrypt(text)


def bruteForce(plaintext_result, ciphertext):
    for i in range(16):
        for j in range(16):
            plaintext = decodeText(j, decodeText(i, ciphertext))
            if plaintext == plaintext_result:
                return i, j
    return False


def mitm(plaintext, ciphertext_result):
    A = dict()
    candidates = list()

    def testCandidate(candidate):
        return decodeText(candidate[1], decodeText(candidate[0], ciphertext_result)) == plaintext

    for i in range(16):
        a = encodeText(i, plaintext)
        if a not in A:
            A[a] = i
    for j in range(16):
        b = decodeText(j, ciphertext_result)
        if b in A:
            candidate = (j, A[b])
            if testCandidate(candidate):
                candidates.append(candidate)
    if len(candidates) == 0:
        return False
    return candidates


if __name__ == '__main__':
    plaintext_ = "Provocare MitM!!".encode()
    ciphertext_result_ = encodeText(8, encodeText(14, plaintext_))
    print(ciphertext_result_)
    print(bruteForce(plaintext_, ciphertext_result_))
    print(mitm(plaintext_, ciphertext_result_))

#lab 7 ex 1

#a -> adevarat
#b -> fals
#c -> adevarat
#d -> adevarat
#e -> fals
#f -> fals
#g -> fals

#ex 2
#input.txt

fisier = int(input("range = "))
cuvant = "contor"
with open("input.txt", "w") as w:
   for i in range(fisier):
      w.write(cuvant + str(i) + "\n")


# verificare coliziuni
with open("output_test.txt", "r") as rt:
    tests = [x.replace("\n", "") for x in rt.readlines()][1:]
    tests = [x.split("::::: ")[1] for x in tests]

with open("output.txt", "r") as r:
    lines = [x.replace("\n", "") for x in r.readlines()][1:]
    lines = [x.split("::::: ")[1] for x in lines]

used = set()
hasCollisions = False
idx = 0
for line in lines:
    if line in used:
       hasCollisions = True
       print(line + " has a collision")
    used.add(line)
    idx += 1
if hasCollisions:
    print("Collisions found")
else:
    print("No collisions found")

# fara coliziuni

#ex 3
#1: Functia data salveaza toate parolele criptate intr-o lista (sau set). Atunci cand dorim sa verificam o parola nu avem cum sa aflam
#carui utilizator ii corespunde.

#2: Un user poate sa si faca mai multe conturi cu acelasi username.

#3: Pentru o securitate mai buna, am avea nevoie de un salt atribuit fiecarei encriptari de parole.

#4: Salt-ul ar trebui sa fie generat random de fiecare data, nu salvat global intr-un fisier. Astfel,
#toate parolele create ar avea acelasi
#salt si parolele ar putea fii compromise printr-un simplu rainbow table attack.

#5: Aceasta functie stocheaza parolele folosind MD5, algoritm ce nu e destinat criptarii parolelor,
# datorita multiplelor vulnerabilitati gasite in algoritm.

#lab 8, ex 2
# nu am gasit nicio parola care sa afiseze tot "Parola introdusa este corecta"
# am incercat sa pun primele 6 caractere altceva, iar apoi fmiSSI, pentru a pacali, dar nu a mers
# am incercat si invers si tot nu a mers
#abcdefmiSSI
# fmiSSIabcde
# atac buffer overflow
'''
#include <iostream>
#include <string.h>

using namespace std;

int main() {
    char pass[7] = "fmiSSI";
    char input[7];
    int passLen = strlen(pass);
    cout<<"Introduceti parola: ";
    cin>>input;

    if (strncmp(input, pass, passLen) == 0) {
        cout<<"Parola introdusa este corecta\n";
    }
    else {
        cout<<"Ati introdus o parola gresita\n";
    }

    return 0;
}'''

# ex 3
import hashlib
import requests

def calculateSha256(filePath):
    with open(filePath, "rb") as fileToHash:
        hashValue = hashlib.sha256(fileToHash.read()).hexdigest()
    return hashValue

def retrieveFileInfo(filePath):
    apiUrl = 'https://www.virustotal.com/api/v3/files'
    apiHeaders = {'x-apikey': 'eb04072fe2ea92baddfaedadc1614423b65b1664b3f71db2c4673cf8ecf2a044'}
    with open(filePath, 'rb') as fileToUpload:
        fileData = {'file': ('malware.png', fileToUpload)}
        initialResponse = requests.post(apiUrl, headers=apiHeaders, files=fileData)
        if initialResponse.status_code == 200:
            fileHash = calculateSha256(filePath)
            fileUrl = f"https://www.virustotal.com/api/v3/files/{fileHash}"
            finalResponse = requests.request("GET", fileUrl, headers=apiHeaders)
            if finalResponse.status_code == 200:
                return finalResponse.json()
    return None

if __name__ == '__main__':
    fileInfo = retrieveFileInfo("malware.png")
    if fileInfo is None:
        print("An error occured")
    else:
        print(fileInfo['data']['attributes']['last_analysis_stats']['suspicious'])

# Funcția `calculateSha256` calculează hash-ul SHA256 al unui fișier. Acest hash este un rezumat
# al conținutului fișierului și este unic pentru fiecare fișier.
# Funcția `retrieveFileInfo` încarcă un fișier pe VirusTotal, un serviciu online care analizează
# fișierele pentru a detecta viruși și alte tipuri de malware. În primul rând, deschide fișierul și
# îl încarcă pe VirusTotal folosind API-ul lor. Dacă încărcarea reușește (adică dacă răspunsul HTTP
# are codul de stare 200), atunci calculează hash-ul SHA256 al fișierului și face o altă cerere la
# VirusTotal pentru a obține informații despre fișier. Dacă această a doua cerere reușește, atunci
# returnează informațiile despre fișier ca un obiect JSON.
# În partea de jos a codului, se apelează funcția `retrieveFileInfo` pentru a încărca și a obține
# informații despre un fișier numit "malware.png". Dacă funcția returnează `None`, atunci afișează un
# mesaj de eroare. Altfel, afișează numărul de scanări suspecte raportate de VirusTotal pentru fișier.