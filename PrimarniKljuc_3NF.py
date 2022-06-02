import itertools

class relacija:
    def __init__(self, rel, fo, k=[]):
        self.rel=rel
        self.fo=fo
        self.k=k

def print_relacije(baza):
     cnt=1
     for i in baza:
         print("Relacija",cnt,":","\nRelacijska shema:",i.rel,"\nFunkcionalne ovisnosti:",i.fo,"\nKljučevi:",i.k)
         print()
         cnt+=1

def izbrisi_relaciju(baza):
    n=int(input("Unesite broj relacije koju želite izbrisati:"))
    while ((n < 1) or (n>len(baza))):
        n=int(input("Krivi unos, unesite broj relacije koju želite izbrisati:"))
    baza.pop(n-1)
    print_relacije(baza)

def check_fo(rel,fo):
    if "->" not in fo:
        return False
    j=fo.split("->")
    if not (j[0].isalpha() and j[1].isalpha()):
        return False
    for i in j:
        for k in i:
            if k not in rel:
                return False
    return True

def nova_relacija(baza):
    tmp_rel=input("Unesite relacijsku shemu:")
    while not (tmp_rel.isalpha()):
         tmp_rel=input("Krivi unos, unesite relacijsku shemu:")
    rel=[]
    tmp_rel=tmp_rel.upper()
    for i in range(0,len(tmp_rel),1):
        rel.append(tmp_rel[i])

    fo=[]
    n=0
    n=input("Unesite broj funkcionalnih ovisnosti u relaciji:")
    while not (n.isdigit()):
         n=input("Krivi unos, unesite broj funkcionalnih ovisnosti u relaciji:")
    n=int(n)
    for i in range(0,n,1):
        tmp_fo=input("Unesite funkcionalnu ovisnost:")
        while not (check_fo(rel,tmp_fo.upper())):
             tmp_fo=input("Krivi unos, unesite funkcionalnu ovisnost:")
             
        fo.append(tmp_fo.upper())
    
    rel_obj=relacija(rel,fo)
    baza.append(rel_obj)
    return baza

def split_fo (fo):
    j=[]
    for i in range (0,len(fo),1):
        k=fo[i].split("->")
        j=j+k
    return j

def containeri (p):
    temp_left, left, right, mid, temp = [], [], [], [], []

    fo_list=split_fo(p.fo)
    for i in range (0,len(p.rel),1):
        for j in range (0,len(fo_list),2):
            if p.rel[i]  in fo_list[j]:
                if p.rel[i]  not in temp_left:
                    temp_left.append(p.rel[i])
        for k in range (1,len(fo_list),2):
            if p.rel[i] in fo_list[k]:
                if p.rel[i]  not in right:
                    right.append(p.rel[i])

    for x in temp_left:
        if x in right:
            mid.append(x) 
          
    for x in temp_left:
        if x not in mid and x not in left:
            left.append(x) 
                
    for x in p.rel:
        if x not in left and x not in right:
            temp.append(x) 
    
    return left,mid,temp
    
def ograda (atribut,fo,rel):
    flag = True
    temp_at=atribut
    ograda=[]
    fo_list=split_fo(fo)
    
    while (flag):
        tmp_ograda=""
        tmp_ograda=tmp_ograda.join(ograda)

        for i in range (0,len(fo_list),2):
            cnt=0
            for j in range (0,len(fo_list[i]),1):
                if fo_list[i][j] in temp_at:
                    cnt=cnt+1
                    if cnt == len(fo_list[i]):
                        temp_at=temp_at+fo_list[i+1]
                        
        for x in temp_at:
            if x not in ograda:
                ograda.append(x)
        ograda.sort()

        if (ograda==rel):
            break
        
        if(len(ograda) > (len(tmp_ograda))):
            flag=True
        else:
            flag=False
            
    return ograda

def pretraga (p):
    livi,srednji,tmp_cont=containeri(p)
    
    relacija=[]
    for i in p.rel:
        if i not in tmp_cont:
            relacija.append(i)
    relacija.sort()
    
    kljucevi=[]
    for k in range(0,len(srednji)+1,1):
        tmp = list(itertools.combinations(srednji, k))
        distinct = list(set(tmp))
      
        if (len(livi)==0):
            for i in range (0,len(distinct),1):
                tmp_str = "".join(distinct[i])
                
                if (ograda(tmp_str,p.fo,relacija))==relacija:
                    tmp_str += "".join(tmp_cont)
                    kljucevi.append(tmp_str)
                
        if (len(livi)>0):
            for i in range (0,len(distinct),1):
                tmp_str = "".join(livi) + "".join(distinct[i])
                if ograda(tmp_str,p.fo,relacija)==relacija:
                    tmp_str += "".join(tmp_cont)
                    kljucevi.append(tmp_str)
    
        if(len(kljucevi)):
            break 

    kljucevi.sort()
    
    print("RELACIJA: ",p.rel)
    print("OVISNOSTI:",p.fo)
    print("KLJUČEVI: ",["".join(sorted(i)) for i in kljucevi])
    print()
    return kljucevi

def add_keys(R,K):
    R.k=["".join(sorted(i)) for i in K]

def decompose_3nf(fo_list, k):
    print("Dekompozicija u treću normalnu formu:")
    nova=[]
    for fo in fo_list:
        temp_fo = fo
        fo = ''.join(set(fo.split('->')))
        uvjet = False
        for temp_rel in nova:
            uvjet = True
            for att in fo:
                if att not in temp_rel:
                    uvjet = False

            if uvjet:
                print(temp_fo + " je uključen u " + temp_rel)
                break

        if not uvjet:
            print(temp_fo + " nije uključen, dodajemo ga.")
            fo="".join(sorted(set(fo)))
            nova.append(fo)

    for key in k:
        for fo in fo_list:
            uvjet = True
            fo = ''.join(set(fo.split('->')))
            for att in key:
                if att not in fo:
                    uvjet = False
                    break
            if uvjet:
                print('Ključ ' + key + ' je već uključen.')
                nova.sort()
                return nova

    print('Nijedan ključ nije uključen, dodajemo ključ: ' + k[0])
    nova.append(k[0])
    nova.sort()
    return nova

def izbor_relacije(baza):
    n=len(baza)
    odabir=input(f"Odaberite 1-{n}, slovo u/U za unos, slovo a/A za prikaz svih relacija, slovo b/B za brisanje ili slovo x/X za izlaz:")
    print()
    if odabir.isdigit():
        odabir=int(odabir)
        if((odabir<=len(baza)) and (odabir>0)):
            print ("Odabrali ste relaciju",odabir)
            rez = pretraga(baza[odabir-1])
            add_keys(baza[odabir-1], rez)
            print('\n3NF rješenje: ' + ', '.join(decompose_3nf(baza[odabir-1].fo, baza[odabir-1].k)))
            return izbor_relacije(baza)
        else:
            return izbor_relacije(baza)
    
    if (odabir.upper() == "U"):
        novi_p=nova_relacija(baza)
        rez = pretraga(baza[len(novi_p)-1])
        add_keys(baza[len(novi_p)-1], rez)
        print('\n3NF rješenje: ' + ', '.join(decompose_3nf(baza[len(novi_p)-1].fo, baza[len(novi_p)-1].k)))
        return izbor_relacije(baza)

    if (odabir.upper() == "A"):
        print_relacije(baza)
        return izbor_relacije(baza)

    if (odabir.upper() == "B"):
        izbrisi_relaciju(baza)
        return izbor_relacije(baza)

    if (odabir.upper() == "X"):
        return 0
            
    else:
        return izbor_relacije(baza)

def aplikacija():
    baza=[
        relacija(["A","B","C","D","E","F","G"],["A->D","AG->B","B->G","B->E","E->B","E->F"],[]), 
        relacija(["A","B","C","D","E","F","G","H","I","J"],["D->AB","E->BC","HI->AF","CJ->G","B->IJ"],[]), 
        relacija(["A","B","C","D","E","F","G","H","I","J"],["AD->B","E->J","CF->G","B->EH","D->EJ"],[]),
        relacija(["A","B","C","D","E","F","G","H","I","J"],["A->BC","D->C","FI->IJ","E->F","FJ->D"],[]),
        relacija(["A","B","C","D","E","F","G","H","I","J"],["B->CE","E->CH","I->DH","CJ->I","BE->JC","C->D"],[]),
        relacija(["A","B","C","D","E","F","G","H","I","J"],["DI->B","AJ->F","GB->FJE","AJ->HD","I->CG"],[]),
        relacija(["A","B","C","D","E","F","G","H","I","J"],["A->EF","F->CH" ,"I->DB","CJ->I","BF->JE","E->CD"],[]), 
        relacija(["A","B","C","D","E","F","G"],["A->B","BE->G", "EF->A", "D->AC"],[]),
        relacija(["A","B","C"],["A->B","B->A","B->C","A->C","C->A"],[]),
        relacija(["A","B","C","D","E","F","G","H","I","J"],["J->I","HG->F","A->BC","BC->DE", "I->AB"],[])
    ]
    
    print_relacije(baza)
    izbor_relacije(baza)

aplikacija()