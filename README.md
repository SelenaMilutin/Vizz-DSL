# Vizz – Domain-Specific Language za vizuelizaciju podataka

## 1. Opis projekta  

Vizz je domenski specifičan jezik (DSL) namenjen za grafički prikaz korisnikovih podataka bez potrebe poznavanja pandas ili matplotlib biblioteke. Cilj je da na osnovu ulaza moze sam da nacrta korisne grafike za specifične podatke.  

DSL je implementiran korišćenjem textX biblioteke za definisanje gramatike i parsiranje, dok se semantika jezika mapira na Matplotlib biblioteku za iscrtavanje grafika u Pythonu. Na ovaj način, DSL skripta se prevodi u odgovarajući Matplotlib kod koji generiše grafički prikaz.  

Jezik podržava više tipova grafika (linijski grafici, stubičasti grafici, scatter plotovi, pie grafici), rad sa više subplotova unutar jedne figure, osnovno stilizovanje (boje, naslovi, legende, mreže) kao i čuvanje rezultata u fajl.

Jezik poseduje mogućnost samostalnog određivanja vrste grafika na osnovu datih podataka. Podaci se mogu učitati iz date liste, .csv fajla ili iz eksternih izvora (kaggle dataset). Jezik omogućava parametrizaciju maksimalnog broja elemenata na X osi (stubova u bar plotu i isečaka u pie plotu).

## 2. Korišćene tehnologije  

**Python 3.x** – glavni programski jezik  
**textX** – definisanje gramatike i parsiranje DSL-a  
**Matplotlib** – generisanje grafičkih prikaza  
**Git / GitHub** – verzionisanje i upravljanje projektom  

## 3. Primer upotrebe  

```
figure sales_analysis {
    size: (12, 8)
    title: "Sales analysis"
    rows: 1
    cols: 2
    source: ./data/file.csv

    plot {
        position: (1, 1)
        x: source.date
        y: source.price
        groupBy: ("year", 2024)
        label: "Online sales"
        color: "blue"
        xlabel: "Month"
        ylabel: "Prices"
        legend: true
        grid: true
    }

    bar {
        position: (1, 2)
        x: source.date
        y: [80, 70, 60, 90, 110]
        label: "Store sales"
        color: "orange"
        legend: false
        false: false
    }

    bar {
        x: source.date
        y: source.price
        color: "red"
    }

    save: "sales.png"
}
```

## 4. Način rada sistema  

Arhitektura projekta je podeljena u tri sloja:  
**Sintaksa (Grammar)** – definisana pomoću textX (.tx fajl)  
**Model / Semantika** – objektni model generisan iz gramatike  
**Backend – mapiranje** DSL konstrukata na matplotlib API  

Način rada:  
DSL skripta se učitava iz fajla  
textX parser generiše model na osnovu definisane gramatike  
Model se mapira na Matplotlib pozive Matplotlib generiše i prikazuje grafike 

## 5. Instalacija projekta

Projekat je može instalirati na dva načina:
1. Pokretanjem komande `pip install -e .` iz korenskog direktorijma.
2. Pokretanjem komande `pip install -e git+https://github.com/SelenaMilutin/Vizz-DSL.git#egg=vizz`

Pokretanje projekta se vrši komandom `vizz <file.vizz>`.

## 6. Ekstenzija za VSCode

Uz jezik je dostupna ekstenzija za VSCode koja omogućava syntax highlighting, code autocomplete and LSP server za error checking. Ekstenzija se može instalirati ulaskom u VSCode, pokretanjem prečice CTRL + SHIFT + P, biranjem opcije Extensions: Install from VSIX.
