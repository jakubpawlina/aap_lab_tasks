# Sprawozdanie - zestaw zaliczeniowy AAP

Notebook zostal uruchomiony od poczatku do konca na Pythonie 3.14.4 i PySpark 4.1.2. Ponizsze czasy pochodza z jednego uruchomienia i zaleza od maszyny; wyniki merytoryczne sa deterministyczne dla probki IMDB tasowanej z `seed=42`, zgodnie z trescia zadania.

## 1. Dekoratory

Dekorator `retry` uzyskal 96 poprawnych wynikow na 100 wywolan przy `seed=42`. Wynik jest zgodny z losowym eksperymentem, ktorego teoretyczne prawdopodobienstwo sukcesu w pieciu probach wynosi `1 - 0.5**5 = 96.875%`. Drugie wywolanie tego samego identyfikatora nie wykonalo ciala funkcji, co potwierdza dzialanie cache JSON na dysku.

## 2. Wspolbieznosc

Zmierzony czas dla 5000 recenzji wyniosl 0.352 s sekwencyjnie, 0.379 s dla `ThreadPool` i 0.194 s dla `multiprocessing.Pool`. Procesy byly najszybsze, poniewaz omijaja GIL, ale nie jest to gwarantowane dla kazdej maszyny: przy bardzo lekkiej funkcji koszt uruchomienia procesow i IPC moze przewyzszyc zysk z rownoleglosci.

## 3. Testowanie

Pytest zakonczyl sie wynikiem `11 passed, 1 xfailed`. Testy obejmuja fixtury, szesc parametryzowanych przypadkow brzegowych, opcje tokenizatora, filtrowanie dlugosci, zbior IMDB oraz swiadomie nieobslugiwany format adresu e-mail. Dla 100 recenzji slownik mial 5053 tokeny, a pojedyncza recenzja zawierala srednio 153.17 unikalnego tokenu.

## 4. Bazy danych

Oba schematy zwrocily po 1000 recenzji negatywnych i pozytywnych oraz zgodne srednie dlugosci. Baza relacyjna zajela 3,215,360 bajtow, a JSON 3,518,464 bajtow. Wstawianie trwalo odpowiednio 0.0445 s i 0.1758 s, a sredni odczyt agregacji 0.001734 s i 0.013061 s. Dla stalego schematu i zapytan analitycznych lepszy jest model relacyjny; JSON warto wybrac, gdy wazniejsza jest zmiennosc struktury dokumentow.

## 5. PySpark

Window functions wyznaczyly ranking i po trzy najdluzsze recenzje w kazdej klasie. Roznica od sredniej zostala policzona bez redukcji liczby wierszy, a `rowsBetween(-49, 0)` tworzy okno obejmujace biezaca i 49 poprzednich recenzji danej klasy. Wykres pokazuje osobny przebieg sredniej kroczacej dla obu etykiet.

## 6. Jakosc danych

W probce 2000 rekordow nie bylo nulli, blednych etykiet, zbyt krotkich lub zbyt dlugich tekstow ani duplikatow; klasy byly idealnie zbalansowane. Znaczniki HTML wystapily w 1189 rekordach. Regula `no_html_tags` ma severity `warning`, dlatego problem jest zapisany w raporcie, ale nie zatrzymuje pipeline'u; naruszenie reguly `error` zatrzymaloby walidacje natychmiast.
