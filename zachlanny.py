import copy
import time

def sequence(input_list, max_len):
    lista = copy.deepcopy(input_list)
    finalSequence = [lista.pop(0)]
    string_1 = finalSequence[0][1:]
    string_2 = "init"
    while len(lista) > 0:
        z = 1
        x = 0
        while string_1 != string_2:
            while x <= len(lista) - 1:
                string_2 = lista[x][:-z]
                if string_2 == string_1:
                    element = lista.pop(x)
                    finalSequence.append(element)
                    if len(finalSequence) > max_len:
                        return finalSequence
                    string_1 = element[1:]
                    x = -1
                    z = 1
                elif x == len(lista) - 1:
                    z += 1
                    string_1 = string_1[1:]
                    x = -1
                x += 1
            if len(lista) == 0:
                break

    return finalSequence


def ucinaj(sol):
    i = 0
    max_dopasowanie = 0
    while i < len(sol) - 1:
        for j in range(1, 10):
            if sol[i][-j:] in sol[i+1][:j]:
                max_dopasowanie = j
        sol[i] = sol[i][:10 - max_dopasowanie]
        i = i + 1
        max_dopasowanie = 0
    return sol


f = open("instancje/negatywne_powtorzenia/59.500-2.txt", "r")
plaintext = f.read()
elements = plaintext.split()
print(elements)
first_elements = copy.deepcopy(elements)

start = time.time()
max_len = 509
ans = sequence(elements, max_len - 10)
print("czas: ", time.time()-start)
print(ans)
print(len(ans))
seq = ucinaj(ans)
print(seq)
sol = "".join(seq)
sol = sol[:max_len]
print(sol)
print(len(sol))

counter = 0
for el in first_elements:
    if el in sol:
        counter += 1
print("Rozwiązanie uwzględnia", counter, "na", len(first_elements), "słów wejściowych")
