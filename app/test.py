from MTP import getRawData, solve

file_name = 'Database.xlsx'
PojemnoscMagazynu = getRawData(file_name, sheet_name = 'PojemnoscMagazynu')
DostepnoscProduktowWMagazynach = getRawData(file_name, sheet_name = 'DostepnoscProduktowWMagazynach')
Zapotrzebowanie = getRawData(file_name, sheet_name = 'Zapotrzebowanie')
WagaProduktu = getRawData(file_name, sheet_name = 'WagaProduktu')
Koszt = getRawData(file_name, sheet_name = 'Koszt')

resultlist = solve()
