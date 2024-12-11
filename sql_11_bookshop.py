# Slajd 77 u prezentaciji

# Kreirajte aplikaciju koja će biti katalog knjiga dostupnih u Bookshopu.
# Za svaku knjigu treba čuvati podatke o nazivu, autoru, izdavaču, cijeni i raspoloživosti
# Za svakog autora treba čuvati podatke o imenu i prezimenu te knjigama koje je napisao
# Podaci o svakom izdavaču su naziv, lista autora s kojima rade te lista izdanih knjiga

# 1 knjiga -> 1 autor i 1 izdavač
# 1 autor -> list["Knjiga"] i 1 izdavač
# 1 izdavač -> list["Autor"] i list["Knjiga"]

# Koristite SQLAlchemy ili SQLModel
# Koristite dokumentaciju i internet, primjere s nastave
# Opcionalno: stavite na svoj GitHub račun

from sqlmodel import SQLModel, Field, create_engine, Session, Relationship, select
from datetime import date

class Izdavac(SQLModel, table = True):
    id: int = Field(default = None, primary_key=True)
    naziv: str
    autori: list["Autor"] = Relationship(back_populates = "izdavac") # -> relacije (selfpopulate) 
    knjige: list["Knjiga"] = Relationship(back_populates = "izdavac") # -> relacije (selfpopulate) 

class Autor(SQLModel, table = True):
    id: int = Field(default = None, primary_key=True)
    ime_i_prezime: str
    izdavac: Izdavac = Relationship(back_populates = "autori")
    knjige: list["Knjiga"] = Relationship(back_populates = "autor") # -> relacije (selfpopulate)

    #knjiga_id: int = Field(foreign_key = "knjiga.id")
    izdavac_id: int = Field(foreign_key = "izdavac.id")

class Knjiga(SQLModel, table = True):
    id: int = Field(default = None, primary_key=True)
    naslov: str
    autor: Autor = Relationship(back_populates = "knjige")
    izdavac: Izdavac = Relationship(back_populates = "knjige")
    cijena: float
    raspolozivost: bool

    izdavac_id:int = Field(foreign_key = "izdavac.id")
    autor_id: int = Field(foreign_key = "autor.id")

    

    # def __str__(self):
    #     return f"{self.naslov}, {self.autor}, {self.izdavac}, US${self.cijena}, {self.raspolozivost}"

engine = create_engine("sqlite:///BookstoreDB.db", echo = False)
SQLModel.metadata.create_all(bind = engine)

# unos podataka    
# # izdavači
with Session(engine) as session:
    izdavac1 = Izdavac(naziv = "Simon & Schuster")
    izdavac2 = Izdavac(naziv = "HarperCollins")
    izdavac3 = Izdavac(naziv = "Penguin Random House")
    session.add(izdavac1)
    session.add(izdavac2)
    session.add(izdavac3)
    session.commit()  # obavezno


# # autori
with Session(engine) as session:
    autor1 = Autor(ime_i_prezime="Stephen King", izdavac = izdavac1)
    autor2 = Autor(ime_i_prezime="J.R.R. Tolkien", izdavac = izdavac2)
    autor3 = Autor(ime_i_prezime="Emily Henry", izdavac = izdavac3)
    session.add(autor1)
    session.add(autor2)
    session.add(autor3)
    session.commit()  # obavezno

# # knjige
with Session(engine) as session:
    knjiga1 = Knjiga(naslov="The Shining", autor=autor1, izdavac=izdavac1,cijena=18.99, raspolozivost=True )
    knjiga2 = Knjiga(naslov="It", autor=autor1, izdavac=izdavac1, cijena=48.99, raspolozivost=True )
    knjiga3 = Knjiga(naslov="The Stand", autor=autor1,izdavac=izdavac1, cijena=41.29, raspolozivost=True )
    knjiga4 = Knjiga(naslov="The Hobbit", autor=autor2, izdavac=izdavac2, cijena=7.13, raspolozivost=True )
    knjiga5 = Knjiga(naslov="The Lord of the Rings", autor=autor2, izdavac=izdavac2, cijena=8.25, raspolozivost=True )
    knjiga6 = Knjiga(naslov="The Silmarillion", autor=autor2, izdavac=izdavac2, cijena=8.25, raspolozivost=True )
    knjiga7 = Knjiga(naslov="People We Meet on Vacation", autor=autor3, izdavac=izdavac3, cijena=8.25, raspolozivost=True )
    knjiga8 = Knjiga(naslov="Beach Read", autor=autor3, izdavac=izdavac3, cijena=8.25, raspolozivost=True )
    knjiga9 = Knjiga(naslov="Book Lovers", autor=autor3, izdavac=izdavac3, cijena=8.25, raspolozivost=True )

    session.add(knjiga1)
    session.add(knjiga2)
    session.add(knjiga3)
    session.add(knjiga4)
    session.add(knjiga5)
    session.add(knjiga6)
    session.add(knjiga7)
    session.add(knjiga8)
    session.add(knjiga9)

    session.commit()

# dohvaćanje proizvoda
with Session(engine) as session:
    knjige = session.exec(select(Knjiga)).all()

    for knjiga in knjige:
        print("#####    KNJIGA   ####")
        print(f"naslov = {knjiga.naslov}, autor = {knjiga.autor}, \n izdavač = {knjiga.izdavac}, cijena = {knjiga.cijena}, raspoloživost = {knjiga.raspolozivost}")

# dohvaćanje autora
with Session(engine) as session:
    autori = session.exec(select(Autor)).all()

    for autor in autori:
        print("#####    AUTOR   ####")
        print(autor.ime_i_prezime, autor.knjige)

# dohvaćanje izdavača
with Session(engine) as session:
    izdavaci = session.exec(select(Izdavac)).all()

    for izdavac in izdavaci:
        print("#####    IZDAVAC   ####")
        print(izdavac.naziv, izdavac.autori, izdavac.knjige)



