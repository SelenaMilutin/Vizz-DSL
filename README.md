# Vizz – Domain-Specific Language za vizuelizaciju podataka

## 1. Opis projekta  

Vizz je domenski specifičan jezik (DSL) namenjen za grafički prikaz korisnikovih podataka bez potrebe poznavanja pandas ili matplotlib biblioteke. Cilj je da na osnovu ulaza moze sam da nacrta korisne grafike za specifične podatke.  

DSL je implementiran korišćenjem textX biblioteke za definisanje gramatike i parsiranje, dok se semantika jezika mapira na Matplotlib biblioteku za iscrtavanje grafika u Pythonu. Na ovaj način, DSL skripta se prevodi u odgovarajući Matplotlib kod koji generiše grafički prikaz.  

Jezik podržava više tipova grafika (linijski grafici, stubičasti grafici, scatter plotovi), rad sa više subplotova unutar jedne figure, osnovno stilizovanje (boje, naslovi, legende, mreže) kao i čuvanje rezultata u fajl.

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
