"""
Modul sadrži implementacije heš mape
"""
import random

from board import print_board
from map import Map, MapElement


class HashMap(object):
    """
    Klasa modeluje heš mapu
    """


    def __init__(self, capacity=8):
        """
        Konstruktor

        Argumenti:
        - `capacity`: inicijalni broj mesta u lookup nizu
        - `prime`: prost broj neophodan heš funkciji
        """
        self._data = capacity * [None]
        self._capacity = capacity
        self._size = 0
        self.prime = 109345121

        # konstante heširanja
        self._a = 1 + random.randrange(self.prime-1)
        self._b = random.randrange(self.prime)

    def __len__(self):
        return self._size

    def _hash(self, x):
        """
        Heš funkcija

        Izračunavanje heš koda vrši se po formuli (ax + b) mod p.

        Argument:
        - `x`: vrednost čiji se kod računa
        """
        hashed_value = (hash(x)*self._a + self._b) % self.prime
        compressed = hashed_value % self._capacity
        return compressed

    def _resize(self, capacity):
        """
        Skaliranje broja raspoloživih slotova

        Metoda kreira niz sa unapred zadatim kapacitetom u koji
        se prepisuju vrednosti koje se trenutno nalaze u tabeli.

        Argument:
        - `capacity`: kapacitet novog niza
        """
        old_data = list(self.items())
        self._data = capacity * [None]
        self._size = 0

        # prepisivanje podataka u novu tabelu
        for (k, v) in old_data:
            self[k] = v

    def __getitem__(self, key):
        """
        Pristup elementu sa zadatim ključem

        Apstraktna metoda koja opisuje pristup elementu na osnovu
        njegovog ključa. Implementacija pristupa bucketu varira u
        zavisnosti od načina rešavanja kolizija.

        Argument:
        - `key`: ključ elementa kome se pristupa
        """
        bucket_index = self._hash(key)
        return self._bucket_getitem(bucket_index, key)

    def __setitem__(self, key, value):
        bucket_index = self._hash(key)
        self._bucket_setitem(bucket_index, key, value)

        # povećaj broj raspoloživih mesta
        current_capacity = len(self._data)
        if self._size > current_capacity // 2:
            self._resize(2*current_capacity - 1)

    def __delitem__(self, key):
        bucket_index = self._hash(key)
        self._bucket_delitem(bucket_index, key)
        self._size -= 1


class ChainedHashMap(HashMap):
    """
    Klasa modeluje heš mapu koja kolizije rešava ulančavanjem
    """
    def _bucket_getitem(self, i, key):
        """
        Pristup elementu u okviru bucketa

        Metoda najpre pristupa bucketu sa zadatim indeksom. Ukoliko
        bucket postoji, pretražuje se. Ako je element pronađen metoda
        vraća njegovu vrednostu, dok se u suprotnom podiže odgovarajući
        izuzetak.

        Argumenti:
        - `i`: indeks bucketa
        - `key`: ključ elementa
        """
        bucket = self._data[i]
        if bucket is None:
            raise KeyError('Ne postoji element sa traženim ključem.')

        return bucket[key]

    def _bucket_setitem(self, i, key, value):
        """
        Postavljanje vrednosti elementa sa zadatim ključem

        Metoda najpre pronalazi bucket sa zadatim indeksom, a zatim
        dodaje novi element ili ažurira postojeći na osnovu zadatog
        ključa. Ukoliko bucket ne postoji, kreira se novi.

        Argumenti:
        - `i`: indeks bucketa
        - `key`: ključ elementa
        - `value`: vrednost elementa
        """
        bucket = self._data[i]
        if bucket is None:
            self._data[i] = Map()

        # broj elemenata u mapi se menja samo u slučaju da je došlo do
        # dodavanja, dok ažuriranje ne menja broj elemenata
        current_size = len(self._data[i])
        self._data[i][key] = value
        if len(self._data[i]) > current_size:
            self._size += 1

    def _bucket_delitem(self, i, j):
        """
        Brisanje elementa sa zadatim ključem

        Metoda najpre pristupa bucketu sa zadatim indeksom. Ukoliko
        bucket postoji, pretražuje se. Ako je element pronađen vrši
        se njegovo brisanje, u suprotnom se podiže odgovarajući
        izuzetak.

        Argumenti:
        - `i`: indeks bucketa
        - `key`: ključ elementa
        """
        bucket = self._data[i]
        if bucket is None:
            raise KeyError('Ne postoji element sa traženim ključem.')

        del bucket[j]

    def __iter__(self):
        for bucket in self._data:
            if bucket is not None:
                for key in bucket:
                    yield key


class LinearHashMap(HashMap):
    """
    Klasa modeluje heš mapu koja rešava kolizije linearnim pretraživanjem
    """
    # sentinel koji označava lokaciju u mapi sa koje je obrisan element
    _MARKER = object()

    def _is_available(self, i):
        """
        Metoda proverava da li je bucket sa zadatim indeksom slobodan

        Argument:
        - `i`: indeks bucketa
        """
        return self._data[i] is None or self._data[i] is self._MARKER

    def _find_bucket(self, i, key):
        """
        Metoda pronalazi bucket koji sadrži element sa zadatim ključem
        """
        available_slot = None
        while True:
            if self._is_available(i):
                if available_slot is None:
                    available_slot = i

                if self._data[i] is None:
                    return (False, available_slot)
            elif key == self._data[i].get_key():
                return (True, i)

            i = (i+1) % len(self._data)

    def _bucket_getitem(self, i, key):
        """
        Pristup elementu u okviru bucketa

        Metoda najpre pristupa bucketu sa zadatim indeksom. Ukoliko
        bucket postoji, pretražuje se. Ako je element pronađen metoda
        vraća njegovu vrednostu, dok se u suprotnom podiže odgovarajući
        izuzetak.

        Argumenti:
        - `i`: indeks bucketa
        - `key`: ključ elementa
        """
        found, index = self._find_bucket(i, key)
        if not found:
            raise KeyError('Ne postoji element sa traženim ključem.')
        return self._data[index].get_value()

    def _bucket_setitem(self, i, key, value):
        """
        Postavljanje vrednosti elementa sa zadatim ključem

        Metoda najpre pronalazi bucket sa zadatim indeksom, a zatim
        dodaje novi element ili ažurira postojeći na osnovu zadatog
        ključa. Ukoliko bucket ne postoji, kreira se novi.

        Argumenti:
        - `i`: indeks bucketa
        - `key`: ključ elementa
        - `value`: vrednost elementa
        """
        found, index = self._find_bucket(i, key)
        if not found:
            self._data[index] = MapElement(key, value)
            self._size += 1
        else:
            self._data[index].set_value(value)

    def _bucket_delitem(self, i, key):
        """
        Brisanje elementa sa zadatim ključem

        Metoda najpre pristupa bucketu sa zadatim indeksom. Ukoliko
        bucket postoji, pretražuje se. Ako je element pronađen vrši
        se njegovo brisanje, u suprotnom se podiže odgovarajući
        izuzetak.

        Argumenti:
        - `i`: indeks bucketa
        - `key`: ključ elementa
        """
        found, index = self._find_bucket(i, key)
        if not found:
            raise KeyError('Ne postoji element sa traženim ključem.')

        # označi element markerom
        self._data[index] = self._MARKER

    def __iter__(self):
        total_buckets = len(self._data)
        for i in range(total_buckets):
            if not self._is_available(i):
                yield self._data[i].get_key()




if __name__ == '__main__':
    print("\nChained Hash Map\n---------------------")
    hash_map = ChainedHashMap()
    hash_map[3] = 10
    hash_map[2] = 11

    print('Inicijalno dodavanje')
    for item in hash_map:
        print(item, hash_map[item])

    print('Izmena vrednosti')
    hash_map[3] = 5
    for item in hash_map:
        print(item, hash_map[item])

    print('Brisanje elementa')
    del hash_map[2]
    for item in hash_map:
        print(item, hash_map[item])

    print("\nLinear Hash Map\n---------------------")
    hash_map = LinearHashMap()
    hash_map[3] = 10
    hash_map[2] = 11

    print('Inicijalno dodavanje')
    for item in hash_map:
        print(item, hash_map[item])

    print('Izmena vrednosti')
    hash_map[3] = 5
    for item in hash_map:
        print(item, hash_map[item])

    print('Brisanje elementa')
    del hash_map[2]
    for item in hash_map:
        print(item, hash_map[item])



