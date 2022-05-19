import copy
import math
import random
import time


def lancuchy(elements, length):
    length = length - 1
    range_of_count = len(elements) - 1
    i = 0
    while i < range_of_count:
        matches_of_el, last_match = znajdz_lancuch(elements[i], elements, length)
        while matches_of_el == 1:
            el2 = elements[last_match]
            elements[i] += el2[length:]
            del elements[last_match]
            range_of_count -= 1
            if last_match < i:
                i -= 1
            matches_of_el, last_match = znajdz_lancuch(elements[i], elements, length)
        i += 1
    return elements


def znajdz_lancuch(el1, elements, length):
    matches = 0
    last_match_index = 0
    for i in range(len(elements)):
        el2 = elements[i]
        if el1 != el2:
            if el1[-length:] == el2[:length]:
                last_match_index = i
                matches += 1
    return matches, last_match_index


def osobniki_poczatkowe(elementy, wielkosc_pop):
    osobniki_startowe = []
    shorten = []
    counter = 0
    while counter < wielkosc_pop:
        kopia = copy.deepcopy(elementy)
        random.shuffle(kopia)
        not_short = copy.deepcopy(kopia)
        skrocone = ucinaj(kopia)
        if skrocone not in shorten:
            shorten.append(skrocone)
            osobniki_startowe.append(not_short)
            counter += 1
    return osobniki_startowe, shorten


def populacja_poczatkowa(nieuciete, qualities, n):  # osobniki, jakości, oczekiwana liczność populacji
    populacja = []
    q_populacji = []
    licznosc = 0
    while licznosc < n:
        max_q = -500
        max_index = 0
        for q in range(len(qualities)):
            if qualities[q] > max_q:
                max_q = qualities[q]
                max_index = q
        populacja.append(nieuciete[max_index])
        q_populacji.append(qualities[max_index])
        del (nieuciete[max_index])
        del (qualities[max_index])
        licznosc += 1
    return populacja, q_populacji


def ucinaj(vsol):
    i = 0
    max_dopasowanie = 0
    while i < len(vsol) - 1:
        for j in range(1, 10):
            if vsol[i][-j:] in vsol[i + 1][:j]:
                max_dopasowanie = j
        if max_dopasowanie != 0:
            vsol[i] = vsol[i][:-max_dopasowanie]
        i = i + 1
        max_dopasowanie = 0
    return vsol


def count_len(elements):
    length = 0
    for el in elements:
        length += len(el)
    return length


def licz_jakosc(populacja_in, lista_pierwotna, n):
    jakosc = []
    i = 0
    while i < len(populacja_in):
        sol1 = populacja_in[i]
        sol1 = "".join(sol1)
        sol1 = sol1[:n]
        counter = 0
        for el in lista_pierwotna:
            if el in sol1:
                counter += 1
        jakosc.append(counter)
        i += 1
    return jakosc


def krzyzowanie(populacja, n):         # tu wchodzą pełne ciągi, przed ucięciem
    potomkowie = []
    licznosc = 0
    while licznosc < n:
        o1 = random.randint(0, len(populacja) - 1)
        o2 = random.randint(0, len(populacja) - 1)
        while o1 == o2:
            o2 = random.randint(0, len(populacja) - 1)
        o1 = populacja[o1]
        o2 = populacja[o2]
        i = 0
        potomek = []
        while i < len(o1):
            x = random.randint(0, 1)
            if x == 0:
                if o1[i] not in potomek:
                    potomek.append(o1[i])
                else:
                    potomek.append(o2[i])
            else:
                if o2[i] not in potomek:
                    potomek.append(o2[i])
                else:
                    potomek.append(o1[i])
            i += 1
        potomkowie.append(potomek)
        licznosc += 1
    return potomkowie


def wybor_nastepnego_pokolenia(lista_osobnikow, jakosci_osobnikow, wielkosc_populacji):
    najlepsze = sorted(range(len(jakosci_osobnikow)), key=lambda ival: jakosci_osobnikow[ival], reverse=True)
    print(jakosci_osobnikow)
    nowe_pokolenie = []
    wymiana_osobikow_val = wielkosc_populacji - rotacja_osobnikow
    counter = 0
    for wynik in najlepsze:
        if counter == wymiana_osobikow_val:
            break
        nowe_pokolenie.append(lista_osobnikow[wynik])
        counter += 1
    nowe_krzyzowanie = krzyzowanie(lista_osobnikow, wielkosc_populacji - wymiana_osobikow_val)
    pokolenie_out = nowe_pokolenie + nowe_krzyzowanie
    for i in range(math.ceil(percent_of_mutation/100*wielkosc_populacji)):
        chosen_one = random.randint(0, wielkosc_populacji-1)
        nb_of_string = len(pokolenie_out[chosen_one]) - 1
        x1 = random.randint(0, nb_of_string)
        x2 = random.randint(0, nb_of_string)
        while x1 == x2:
            x2 = random.randint(0, nb_of_string)
        pokolenie_out[chosen_one][x1], pokolenie_out[chosen_one][x2] = pokolenie_out[chosen_one][x2], pokolenie_out[chosen_one][x1]
    ucieci_potomkowie = []
    i = 0
    while i < len(pokolenie_out):
        p = copy.deepcopy(pokolenie_out[i])
        p = ucinaj(p)
        ucieci_potomkowie.append(p)
        i += 1

    jakosci_pok = licz_jakosc(ucieci_potomkowie, first_elements, len_of_out_string)

    return pokolenie_out, jakosci_pok


def iteracje_algorytmu(ilosc_iteracji, lista_osobnikow, jakosci_osobnikow, wielkosc_populacji):
    pokolenie = lista_osobnikow
    jakosci_pok = jakosci_osobnikow
    for iteracja in range(ilosc_iteracji):
        pokolenie, jakosci_pok = wybor_nastepnego_pokolenia(pokolenie, jakosci_pok, wielkosc_populacji)
        if len(set(jakosci_pok)) <= percent_of_mutation * 3 and max(jakosci_pok) > 0.95 * number_of_words:
            break
        if max(jakosci_pok) == number_of_words:
            break
        if len(set(jakosci_pok)) <= percent_of_mutation * 1.5:  # przyspieszone odcięcie
            break

    return pokolenie, jakosci_pok


filename = "instancje/negatywne_losowe/25.500-200.txt"
number_of_words = 0
len_of_out_string = 0
if '-' in filename:
    vx = filename.split("/")[2].split('-')
    number_of_words = int(vx[0].split('.')[1]) - int(vx[1].split('.')[0])
    len_of_out_string = int(filename.split('-')[0].split('.')[1]) + 9
if '+' in filename:
    vx = filename.split("/")[2].split('+')
    number_of_words = int(vx[0].split('.')[1])
    len_of_out_string = int(filename.split('+')[0].split('.')[1]) + 9
start = time.time()
f = open(filename, "r")
len_of_word = 10
plaintext = f.read()
elements_in = plaintext.split()
# print("-------------------------------------- Zawartość pliku --------------------------------------")
# print(elements_in)
first_elements = copy.deepcopy(elements_in)
# zmienne
size_of_population = 200
number_of_iterations = 300
percent_of_mutation = 5
rotacja_osobnikow = math.ceil(0.68 * size_of_population)
# print("-------------------------------------- Łańcuchy --------------------------------------")
lancuchy = lancuchy(elements_in, len_of_word)
# print(lancuchy)
# print("-------------------------------------- Osobniki początkowe --------------------------------------")
osobniki_poczatkowe, osobniki_skrocone = osobniki_poczatkowe(lancuchy, size_of_population*3)
# print(osobniki_poczatkowe)
# print("-------------------------------------- Populacja początkowa --------------------------------------")
quality = licz_jakosc(osobniki_skrocone, first_elements, number_of_words)
populacja_poczatkowa, q_populacji_poczatkowej = populacja_poczatkowa(osobniki_poczatkowe, quality, size_of_population)
# print(populacja_poczatkowa)
# print("-------------------------------------- Krzyżowanie --------------------------------------")
kolejne_pokolenie = krzyzowanie(populacja_poczatkowa, size_of_population)
# print(kolejne_pokolenie)
# print("-------------------------------------- Ostatnia populacja --------------------------------------")
osobniki_skrocone = []
licznik = 0
while licznik < len(kolejne_pokolenie):
    osobnik_kopia = copy.deepcopy(kolejne_pokolenie[licznik])
    osobnik_kopia = ucinaj(osobnik_kopia)
    osobniki_skrocone.append(osobnik_kopia)
    licznik += 1
quality = licz_jakosc(osobniki_skrocone, first_elements, number_of_words)
ostatnia_populacja, jakosci_populacji = iteracje_algorytmu(number_of_iterations, kolejne_pokolenie, quality, size_of_population)
# print(ostatnia_populacja)
# print("-------------------------------------- Ciąg wyjściowy --------------------------------------")
najlepszy_osobnik = ostatnia_populacja[jakosci_populacji.index(max(jakosci_populacji))]
najlepszy_skrocony = ucinaj(najlepszy_osobnik)
best_quality = licz_jakosc([najlepszy_skrocony], first_elements, len_of_out_string)[0]
string_out = "".join(najlepszy_skrocony)[:len_of_out_string]
# print("osobnik: ", najlepszy_osobnik)
print("wynik: ", string_out)
# print("długość ciągu: ", len(string_out))
print("jakość: ", best_quality, "/", number_of_words, ", ", round(best_quality/number_of_words * 100), "%")
print("time:", time.time()-start)
