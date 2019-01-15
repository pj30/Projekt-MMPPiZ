from flask import Flask,render_template
from MTP import getRawData, solve, solve2

app = Flask(__name__)

@app.route("/")
def index():
    file_name = 'Database.xlsx'
    PojemnoscMagazynu = getRawData(file_name, sheet_name = 'PojemnoscMagazynu')
    DostepnoscProduktowWMagazynach = getRawData(file_name, sheet_name = 'DostepnoscProduktowWMagazynach')
    Zapotrzebowanie = getRawData(file_name, sheet_name = 'Zapotrzebowanie')
    WagaProduktu = getRawData(file_name, sheet_name = 'WagaProduktu')
    Koszt = getRawData(file_name, sheet_name = 'Koszt')
    resultlist = solve()
    resultobj = solve2()
    return render_template('homepage.html', PojemnoscMagazynu=PojemnoscMagazynu , DostepnoscProduktowWMagazynach=DostepnoscProduktowWMagazynach , Zapotrzebowanie = Zapotrzebowanie, WagaProduktu = WagaProduktu, Koszt = Koszt,  resultlist = resultlist , resultobj = resultobj)

if __name__ == "__main__":
    app.run()
