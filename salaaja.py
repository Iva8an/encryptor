import streamlit as st
import sqlite3
import random
import string

#creating the database for hashes
conn = sqlite3.connect('hashes.db')
c = conn.cursor()

c.execute("""
          CREATE TABLE IF NOT EXISTS hashes(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            passage TEXT,
            hash TEXT
         )
""")
conn.commit()
#def lisaa_kayttaja(id: int, nimi: str, sana: str):
#    c.execute("INSERT INTO hashes VALUES(id, name, sana)", (id, nimi, sana))


#Salaaja
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

st.title("This is a secreter")

nimi = st.text_input("Insert your name:")
if nimi:
    #Does user exist
    c.execute("SELECT id FROM hashes WHERE name = ?", (nimi,))
    kayttaja = c.fetchone()
    if not kayttaja:
        #New user
        st.write(f"Welcome, {nimi}! Looks like you are a new user.")
        viesti = st.text_area("Insert a message you would like to hash:")

        if st.button("Save message"):
            satunnais_id = random.randint(1000000, 9999999)
            salattu_viesti = salaaja(viesti)
            c.execute("INSERT INTO hashes (id, name, passage, hash) VALUES (?, ?, ?, ?)", 
                      (satunnais_id, nimi, viesti, salattu_viesti))
            conn.commit()
            st.write(f"Message saved! Your ID is: {satunnais_id}")

    else:
            #Old user
            st.write(f"Welcome back, {nimi}!")
            id_numero = st.text_input("Insert your message ID:")

            if st.button("Search message"):
                c.execute("SELECT passage, hash FROM hashes WHERE id = ? AND name = ?", 
                        (id_numero, nimi))
                viesti = c.fetchone()

                if viesti:
                    alkuperainen, salattu = viesti
                    st.write(f"Your message is: {alkuperainen}")
                else:
                    st.write("Wrong ID. Heres a hashed message:")
                    st.write(salaaja(id_numero))  # Salattu ID esimerkkinä

    conn.close()
    

#valittu = st.file_uploader("Pick .txt file")
#if valittu is not None:
#    sisalto = valittu.read()
#    teksti = sisalto.decode('UTF-8')
#    viesti = salaaja(teksti)
#    st.write(viesti)
#else:
#    st.write("Upload a file")