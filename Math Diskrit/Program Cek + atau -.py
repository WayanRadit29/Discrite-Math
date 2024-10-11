#Jadi program kita kali ini diminta untuk membuat sebuah program yang memeriksa nilai x :

x = float(input("Input Nilai x : "))

#if x >= 0:
    #if x % 2 == 0:
        #print("hi")
        #print("x adalah bilangan positif genap")
    #else:
        #print("ho")
        #print("x adalah bilangan positif ganjil")
#else:
    #if x % 2 == 0:
        #print("ha")
        #print("x adalah bilangan neagtif genap")
    #else:
        #print("he")
        #print("x adalah bilangan negatif ganjil")

#Cara 2 yang lebih hemat space :
if x > 0:
    print('hi') if x % 2 == 0 else print('ho')
elif x == 0:
    print("nol adalah bilangan netral")
else:
    print('ha') if x % 2 == 0 else print('he')
#Cara 3 yang paling rapi dari mas abdan :
#pake not(x%2) ini cluenya


