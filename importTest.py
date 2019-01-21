from MTP import getRawData

file_name = 'Database.xlsx'
data = getRawData(file_name, sheet_name = 'Zapotrzebowanie')
print(data)
