def odredi_normu(razred, predmet):
    if "at" in razred:
        if predmet == "Hrvatski jezik" or predmet == "Tloznanstvo" or predmet == "Proizvodnja bilja"\
                or predmet == "Voćarstvo" or predmet == "Specijalno voćarstvo" or predmet == "Specijalna zaštita bilja"\
                or predmet == "Poljoprivredna tehnika u biljnoj proizvodnji":
            return 3
        elif "Vjeronauk" in predmet or "Etika" in predmet or predmet == "Zoohigijena i zdravlje životinja"\
            or predmet == "Skladištenje, dorada i prerada poljoprivrednih proizvoda"\
            or predmet == "Organizacija poljoprivredne proizvodnje" or predmet == "Pčelarstvo"\
            or predmet == "Ovčarstvo i kozarstvo":
            return 1
        else:
            return 2
    if "tr" in razred:
        if predmet == "Hrvatski jezik" or (predmet == "Engleski jezik" and ("3" in razred or "4" in razred))\
                or (predmet == "Matematika" and ("3" in razred or "4" in razred)) or predmet == "Građa računala"\
                or predmet == "Algoritmi i programiranje" or predmet == "Digitalna logika" \
                or predmet == "Konfiguriranje računalnih mreža i servisa" \
                or (predmet == "Dijagnostika i održavanje informacijskih sustava" and "3" in razred):
            return 3
        elif predmet == "Matematika" or predmet == "Osnove elektrotehnike":
            return 4
        elif "Vjeronauk" in predmet or "Etika" in predmet or predmet == "Uvod u baze podataka" or predmet == "Biologija"\
            or (predmet =="Geografija" and "2" in razred) or (predmet == "Primijenjena matematika" and "3" in razred)\
            or (predmet == "Multimedija" and "4" in razred) or (predmet == "Web dizajn" and "4" in razred):
            return 1
        else:
            return 2
    if "g" in razred:
        pass
    if "vv" in razred:
        pass
