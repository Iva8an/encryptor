def salaaja(sisalto: str) -> str:
    salattu_teksti = ""
    kirjaimet = "abcdefghijklmnopqrstuvwxyz"

    for merkki in sisalto:
        if merkki.isalpha():
            indeksi = kirjaimet.find(merkki.lower())
            uusi_indeksi = (indeksi + 13) % len(kirjaimet)
            salattu_teksti += kirjaimet[uusi_indeksi]
        else:
            salattu_teksti += merkki

    return salattu_teksti

with open("teksti.txt") as tiedosto:
    teksti = tiedosto.read()  # Luetaan koko tiedosto yhdeksi merkkijonoksi
viesti = salaaja(teksti)
print(viesti)

