__author__ = 'joanneyeh'

with open('countrynames.txt') as file:
    importedfile = file.read().split()


print(importedfile)