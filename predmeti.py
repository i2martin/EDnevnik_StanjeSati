def find_weekly_hours(single_class, subject):
    if "at" in single_class:
        print(subject)
        if subject == "Hrvatski jezik" or subject == "Tloznanstvo" or subject == "Proizvodnja bilja" \
                or subject == "Voćarstvo" or subject == "Specijalno voćarstvo" or subject == "Specijalna zaštita bilja" \
                or subject == "Poljoprivredna tehnika u biljnoj proizvodnji":
            return 3
        elif "Vjeronauk" in subject or "Etika" in subject or subject == "Zoohigijena i zdravlje životinja" \
                or subject == "Skladištenje, dorada i prerada poljoprivrednih proizvoda" \
                or subject == "Organizacija poljoprivredne proizvodnje" or subject == "Pčelarstvo" \
                or subject == "Ovčarstvo i kozarstvo" or subject == "Sat razrednika":
            return 1
        else:
            return 2

    if "tr" in single_class:
        if subject == "Hrvatski jezik" or (
                subject == "Engleski jezik I" and ("3" in single_class or "4" in single_class)) \
                or (
                subject == "Matematika" and ("3" in single_class or "4" in single_class)) or subject == "Građa računala" \
                or subject == "Algoritmi i programiranje" or subject == "Digitalna logika" \
                or subject == "Konfiguriranje računalnih mreža i servisa" \
                or (subject == "Dijagnostika i održavanje informacijskih sustava" and "3" in single_class):
            return 3
        elif subject == "Matematika" or subject == "Osnove elektrotehnike":
            return 4
        elif "Vjeronauk" in subject or "Etika" in subject or subject == "Uvod u baze podataka" or subject == "Biologija" \
                or (subject == "Geografija" and "2" in single_class) or (
                subject == "Primijenjena matematika" and "3" in single_class) \
                or (subject == "Multimedija" and "4" in single_class) or (
                subject == "Web dizajn" and "4" in single_class) or subject == "Sat razrednika":
            return 1
        else:
            return 2

    if "ag" in single_class:
        if subject == "Hrvatski jezik" or (subject == "Kuharstvo" and "4" in single_class):
            return 3
        elif "Vjeronauk" in subject or "Etika" in subject or (subject == "Stočarstvo" and "2" in single_class)\
                or subject == "Sat razrednika":
            return 1
        elif subject == "Praktična nastava" and "3" not in single_class:
            return 7
        elif subject == "Praktična nastava" and "3" in single_class:
            return 8
        else:
            return 2

    if "g" in single_class:
        if subject == "Hrvatski jezik" or (subject == "Matematika" and ("1" in single_class or "2" in single_class)):
            return 4
        elif subject == "Njemački jezik I" or subject == "Engleski jezik I" \
                or (subject == "Matematika" and ("3" in single_class or "4" in single_class)):
            return 3
        elif subject == "Glazbena umjetnost" or subject == "Likovna umjetnost" or subject == "Psihologija" \
                or "Vjeronauk" in subject or "Etika" in subject or subject == "Politika i gospodarstvo"\
                or subject == "Sat razrednika":
            return 1

        else:
            return 2

    if "vv" in single_class:
        if subject == "Hrvatski jezik":
            return 3
        elif subject == "Računalstvo" or subject == "Promet i vožnja" or subject == "Matematika" \
                or "Vjeronauk" in subject or "Etika" in subject or subject == "Sat razrednika":
            return 1
        elif subject == "Praktična nastava":
            return 14
        else:
            return 2
