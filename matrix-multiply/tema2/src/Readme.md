# ASC Tema 2
MAN ANDREI VLAD 336CA
## BLAS
    - am folosit functiile dgemm, care functioneaza astfel:
    - C = A * B + beta * C
    - prima functie face A*B si pune rezultatul in C
    - a doua functie face C * At si pune tot in C
    - a treia face Bt*Bt + C si pune in C, rezultat final
    - am incercat folosirea functiilor pentru matrici triunghiulare (comentat) dtrmm
    - acestea ar fi facut A * B_res (B) si pune rezultatul in B_res
    - B_res (A*B) * C (A) , cu C transpus si pus rezultatul in C
    - iar apoi Bt*Bt + C, cu rezultatul in C
    - implementarea aceasta nu a functionat, rezultatele fiind diferite
    - insa ar fi trebuit sa fie o implementare corecta conform documentatiei.

## NEOPT
    - se inmultesc matricile clasic cu 3 for-uri, fara niciun fel de optimizare

## OPT_M
    - folosim metoda ce favorizeaza CACHE-ul, impartind matricea in block-uri
    - dupa mai multe analize, am constat ca dimenisunea optima pentru block este de 80
    - folosim registrii pentru datele apelate foarte des, adica indexi si sum
    - calculam mai intai in sum si dupa punem pe pozitie
    - calculam iarasi indicii de dinainte, cei care nu se modifica la fiecare iteratie in for-ul cel mai interior

## Memory
    - nu sunt pierderi de memorie

## Cache
    - I refs -> nr de instrunctiuni utilizate
    - I1 -> nr de instructiuni cache miss
    - D -> nr de r/w pt date
    - D1 -> nr de cache miss pt date
    - Branches -> nr de branch-uri executate
    - Mispredicts -> nr de mispredicts pt branch-uri

### NEOPT
    - I : 8 B
    - D : 4 B
    - D1 : 3.3%
    - Mispred 0.3%

### OPT
    - I : 3 B
    - D : 0.6 B
    - D1 : 2.9%
    - Mispred : 1.2%

### BLAS
    - I : 0.3 B
    - D : 0.1 B
    - D1 : 1.7%
    - Mispred : 1.5%

### Interpretare
    Din valorile lui I si D, putem sa vedem o ierarhie a numarului de instructiuni executate
    - BLAS < OPT < NEOPT
    Din D1, putem sa observam localitatea datelor. BLAS foloseste cel mai bine acest aspect, avand un miss rate mai mic.
    - BLAS < OPT < NEOPT 
    Din punctul de vedere al predictiilor compilatorului, NEOPT este mai bun, iar BLAS mai rau
    - OPT in comparatie cu NEOPT, prin optimizari, este avantajat de localitatea datelor (blocks) si executa mai putine instructiuni catre cache (regsitrii, acumulator)

## Performanta
    Vom analiza performanta pe urmatoarele valori ale lui N: 400,800,1200,1600,2000
    [plot](Performanta.png)
    Putem observa din grafic ca BLAS este cea mai eficienta, urmata de OPT, de x10 mai lenta, iar apoi NEOPT, de x50 mai lenta
    Intre OPT si NEOPT, este o diferenta de x5.