# Sudoku

## Crookův algoritmus

Zadání sudoku s dopsanými čísly, které jdou dosadit
![alt text](/images/img1.png "Logo Title Text 1")

## Dosazení jediného možného čísla
Najdeme políčka, do kterých jde dosadit jen jediné číslo
![alt text](/images/img2.png "Logo Title Text 1")

Dosadíme a v políčkách ve stejném řádku, sloupci nebo boxu zakážeme dosazené číslo
![alt text](/images/img3.png "Logo Title Text 1")

Tímto postupem se ale dostaneme jen sem

![alt text](/images/img4.png "Logo Title Text 1")

## Doplnění čísla do jediného políčka možného políčka

Pokud je v nějakém řádku, sloupci nebo boxu dosadit číslo, které se v něm ještě nenachází, jen do jednoho políčka, dosadíme ho tam.
![alt text](/images/img5.png "Logo Title Text 1")

tímto postupen se dostaneme jen sem
![alt text](/images/img6.png "Logo Title Text 1")

## outside box

Pokud se některé číslo v jednom boxu objevuje jen v jednom řádku nebo sloupci, nemůže se v tomto řádku nebo sloupci objevovat mimo tento box. Proto ho vyřadíme.
![alt text](/images/img7.png "Logo Title Text 1")
Na tato políčka by šel použít i Crookův algoritmus, protože obě obsahují pouze dvě stejná čísla. Kdyby v jednom z těchto políček bylo i jiné číslo, které by v druhém nebylo, stále by šel tento postup použít, ale Crookův algoritmus už ne.

## Crook
Crookův algoritmus funguje na úvaze, že když se v *n* políčách v řádku, sloupci nebo boxu opakuje právě *n* stejných čísel, nemůžou se tato čísla obejvovat jinde. Kdyby totiž bylo jinde, nemohlo by být v zmíněné *n*-tici, takže by jedno políčko zůstalo na ocet.
![alt text](/images/img8.png "Logo Title Text 1")

