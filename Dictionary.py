from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.scrolledtext import *
from tkinter import messagebox
import sqlite3
from typing import TypeVar


#//////////////////////////////////////       FUNCTIONS   ////////////////////////////////////////////////////////////////////////////

conn = sqlite3.connect("data.db")
c=conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS usersdata( ID INTEGER PRIMARY KEY AUTOINCREMENT,WORD TEXT,ETHIMOLOGY TEXT,SYNONYME TEXT,ANTONYME TEXT,PARONYME TEXT,HOMONYME TEXT, DIFFICULTE TEXT)')
  #COMPLEXE = O(NlogN) car nous voulons construire une table de n ligne avec les index automatic

def add_data(WORD,ETHIMOLOGY,SYNONYME,ANTONYME,PARONYME,HOMONYME,DIFFICULTE):
    a=c.execute('INSERT INTO usersdata(WORD,ETHIMOLOGY,SYNONYME,ANTONYME,PARONYME,HOMONYME,DIFFICULTE) VALUES (?,?,?,?,?,?,?)',(WORD,ETHIMOLOGY,SYNONYME,ANTONYME,PARONYME,HOMONYME,DIFFICULTE))
    conn.commit()
     #COMPLEXITE O(logN^2) 
         
    
def view_all_words():
    c.execute('SELECT * FROM usersdata ORDER BY WORD ASC')
    data = c.fetchall()
    for row in data:
        tree.insert("",tk.END,values=row)# ICI NOUS AVONS UNE COMPLEXITE DE "O(n^2logn)" car nous avons dans notre requete 
                                         # oderby = O(nlogn)
                                         # select * ....= O(1)
                                         # la boucle for = O(n)

def get_single_word(WORD):#ICI NOUS AVONS UNE COMPLEXITE DE "O(n^2)" pour le scan
    c.execute('SELECT * FROM usersdata WHERE WORD="{}"'.format(WORD))
    data = c.fetchmany()
    return data 

def get_synonyme_word(WORD):#ICI NOUS AVONS UNE COMPLEXITE AU PIRE DES CAS DE "O(n)" puisque l'on utilise pas l'index ID pour le scan
    a=c.execute('SELECT SYNONYME FROM usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data[0]    
def get_homonyme_word(WORD):#ICI NOUS AVONS UNE COMPLEXITE AU PIRE DES CAS DE "O(n)" puisque l'on utilise pas l'index ID pour le scan
    a=c.execute('SELECT HOMONYME FROM usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data  
#print(get_homonyme_word('A'))  
def get_paronyme_word(WORD):
    a=c.execute('SELECT PARONYME FROM usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data   
def get_ethimologie_word(WORD):
    a=c.execute('SELECT ETHIMOLOGY FROM usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data   
def get_antonyme_word(WORD):
    a=c.execute('SELECT ANTONYME FROM usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data    
def get_dif_word(WORD):
    a=c.execute('SELECT DIFFICULTE FROM usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data    

#print(get_synonyme_word('A'))
def distinctval():# COMPLEXITE = O(n^2)
    a=c.execute('SELECT DISTINCT ID,WORD FROM usersdata ORDER BY ID')
    data=a.fetchall()
    return data
#print(distinctval())
def predecesseur(WORD):#COMPLEXITE = O(logn) car pour le scan nous faisons appel a l'index ID
    a=c.execute('SELECT ID-1,WORD from usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data
#print(predecesseur('M'))
def SUCESSEUR(WORD):#COMPLEXITE = O(logn) car pour le scan nous faisons appel a l'index ID
    a=c.execute('SELECT ID+1,WORD from usersdata WHERE WORD="{}"'.format(WORD))
    data = a.fetchall()
    return data
#print(SUCESSEUR('M'))
def update():#COMPLEXITE = O(logn^2) car pour le scan nous faisons appel a l'index ID
    record_id = str(entry_mod.get())
    id= str(entry_mod1.get())
    s= str(entry_mod2.get())
    a= str(entry_mod3.get())
    e= str(entry_mod4.get())
    h= str(entry_mod5.get())
    p= str(entry_mod6.get())
    d= str(entry_mod7.get())
    c.execute('UPDATE usersdata SET WORD=?, SYNONYME=?, ANTONYME=?, ETHIMOLOGY=?, HOMONYME=?, PARONYME=?, DIFFICULTE=? WHERE WORD=?',(record_id,s,a,e,h,p,d,id))
    conn.commit()
    
def supprimer():#COMPLEXITE = O(logn^2) car pour le scan nous faisons appel a l'index ID
    a=str(entry_sup.get())
    c.execute('DELETE FROM usersdata WHERE WORD=?',(a,))
    conn.commit()
    
#JE DIRAI QUE LA COMPLEXITE GENERAL EST O(n^2)
     
#//////////////////////////////////////////////AUTRES FONTIONS POUR INTERACTION AVEC INTERFACE///////////////////////////////
def clear_text():
    entry_word.delete('0',END)
    entry_syn.delete('0',END)
    entry_ant.delete('0',END)
    entry_meaning.delete('0',END)
    entry_paro.delete('0',END)
    entry_homo.delete('0',END)
    entry_diff.delete('0',END)
    
def add_details():
    WORD=str(entry_word.get())
    ETHIMOLOGY=str(entry_meaning.get())
    SYNONYME=str(entry_syn.get())
    ANTONYME=str(entry_ant.get())
    PARONYME=str(entry_paro.get())
    HOMONYME=str(entry_homo.get())
    DIFFICULTE=str(entry_diff.get())
    
    add_data(WORD,ETHIMOLOGY,SYNONYME,ANTONYME,PARONYME,HOMONYME,DIFFICULTE)
    result='\nWORD:[{}]'.format(WORD),'\nETHIMOLOGY:[{}]'.format(ETHIMOLOGY),'\nSYNONYME:[{}]'.format(SYNONYME),'\nANTONYME:[{}]'.format(ANTONYME),'\nPARONYME:[{}]'.format(PARONYME),'\nHOMONYME:[{}]'.format(HOMONYME),'\nDIFFICULTE:[{}]'.format(DIFFICULTE)
    tab1_display.insert(tk.END,result)
    messagebox.showinfo(title="DICTIONAIRES DES DONNEES",message="ENREGISTRER DANS LA BD")
     
def clear_display_result():
    tab1_display.delete('1.0',END)
    
def search_word_by_name():
    WORD = str(entry_search.get())
    result=get_single_word(WORD)
    tab2_display.insert(tk.END,result)
    
def search_word_synonyme_by_name():
    WORD=str(entry_search_syn.get())
    result=get_synonyme_word(WORD)
    tab5_display.insert(tk.END,result)
    
def search_word_predecesseur_by_name():
    WORD=str(entry_search.get())
    result=predecesseur(WORD)
    tab10_display.insert(tk.END,result)
    
def search_word_successeur_by_name():
    WORD=str(entry_search.get())
    result=SUCESSEUR(WORD)
    tab9_display.insert(tk.END,result)
    
def search_word_antonyme_by_name():
    WORD=str(entry_search.get())
    result=get_antonyme_word(WORD)
    tab4_display.insert(tk.END,result)
    
def search_word_homonyme_by_name():
    WORD=str(entry_search.get())
    result=get_homonyme_word(WORD)
    tab6_display.insert(tk.END,result)
    
def search_word_paronyme_by_name():
    WORD=str(entry_search.get())
    result=get_paronyme_word(WORD)
    tab7_display.insert(tk.END,result)
    
def search_word_ethimologie_by_name():
    WORD=str(entry_search.get())
    result=get_ethimologie_word(WORD)
    tab3_display.insert(tk.END,result)
    
def search_word_difficulte_by_name():
    WORD=str(entry_search.get())
    result=get_dif_word(WORD)
    tab11_display.insert(tk.END,result)
    

def clear_entered_search():
    entry_search.delete('0',END)
def clear_entered_syn_search():
    entry_search_syn.delete('0',END)
def clear_ayn_search():
    entry_ayn.delete('0',END)
def clear_pre_search():
    entry_pre.delete('0',END)
def clear_suc_search():
    entry_suc.delete('0',END)
def clear_paro_search():
    entry_par.delete('0',END)
def clear_eth_search():
    entry_eth.delete('0',END)
def clear_hyn_search():
    entry_hyn.delete('0',END)
def clear_dif_search():
    entry_dif.delete('0',END)
    
    
def clear_displaysyn_view():
    tab5_display.delete('1.0',END)
def clear_displayayn_view():
    tab4_display.delete('1.0',END)
def clear_displayhym_view():
    tab6_display.delete('1.0',END)
def clear_displayparo_view():
    tab7_display.delete('1.0',END)
def clear_displayeth_view():
    tab3_display.delete('1.0',END)
def clear_displaypre_view():
    tab10_display.delete('1.0',END)
def clear_displaysuc_view():
    tab9_display.delete('1.0',END)
def clear_displaydif_view():
    tab11_display.delete('1.0',END)
def clear_display_view():
    tab2_display.delete('1.0',END)

def clear_tree_view():
    sel_item=tree.selection()[0]
    tree.delete(sel_item)


   
     


#fenetre
fenetre = Tk()
fenetre.title("DICTIONAIRE DES DONNEES")
fenetre.geometry("1000x900")


style = ttk.Style(fenetre)
style.configure("lefttab.TNotebook",tabposition='wn')


 #////////////////////////////////////////////////////////////      INTERFACE    ///////////////////////////////////////////




#tab layout
tab_control = ttk.Notebook(fenetre, style='lefttab.TNotebook',height=100, padding=2)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)
tab5 = ttk.Frame(tab_control)
tab6 = ttk.Frame(tab_control)
tab7 = ttk.Frame(tab_control)
tab8 = ttk.Frame(tab_control)
tab9 = ttk.Frame(tab_control)
tab10 = ttk.Frame(tab_control)
tab11 = ttk.Frame(tab_control)
tab12 = ttk.Frame(tab_control)
tab13 = ttk.Frame(tab_control)



#add tabs to notebook
tab_control.add(tab1, text=f'{"HOME":^30s}')
tab_control.add(tab2, text=f'{"RECHERCHE":^30s}')
tab_control.add(tab3, text=f'{"ETHIMOLOGIES":^30s}')
tab_control.add(tab4, text=f'{"ANTONYMES":^30s}')
tab_control.add(tab5, text=f'{"SYNONYMES":^30s}')
tab_control.add(tab6, text=f'{"HOMONYMES":^30s}')
tab_control.add(tab7, text=f'{"PARONYMES":^30s}')
tab_control.add(tab8, text=f'{"VUE":^30s}')
tab_control.add(tab9, text=f'{"SUCCEUSEUR":^30s}')
tab_control.add(tab10, text=f'{"PREDESSESEUR":^30s}')
tab_control.add(tab11, text=f'{"MODIFIER":^30s}')
tab_control.add(tab12, text=f'{"SUPPRIMER":^30s}')
tab_control.add(tab13, text=f'{"DIFFICULTE":^30s}')



tab_control.pack(expand=1, fill="both")#define location

create_table()

#create the labels
#label2 = Label(tab2, text="h", padx=5, pady=5)
#label2.grid(column=0, row=0)
#label3 = Label(tab3, text="e", padx=5, pady=5)
#label3.grid(column=0, row=0)
#label4 = Label(tab4, text="g", padx=5, pady=5)
#label4.grid(column=0, row=0)
#label5 = Label(tab5, text="o", padx=5, pady=5)
#label5.grid(column=0, row=0)
#label6 = Label(tab6, text="o", padx=5, pady=5)
#label6.grid(column=0, row=0)#



#individual tabs for each label
#///////////////////////////////////////////////////////modifier///////////////////////////////////////////////////////////////
button1 = Button(tab11, text="EDIT", width=12, bg="#03A9F4", fg="#fff", command=update)
button1.grid(row=3, column=1, padx=5, pady=10, ipady=5)


label_mod1= Label(tab11, text="WORD1", pady=8,font=('Verdana',15))
label_mod1.grid(column=1, row=4)
entry_mod1 = Entry(tab11,width=10, font=('Verdana',15))
entry_mod1.grid(row=5, column=1)


label_mod= Label(tab11, text="WORD2", pady=8,font=('Verdana',15))
label_mod.grid(column=1, row=6)
entry_mod = Entry(tab11,width=10, font=('Verdana',15))
entry_mod.grid(row=7, column=1)


label_mod2= Label(tab11, text="SYNONYME", pady=8,font=('Verdana',15))
label_mod2.grid(column=1, row=8)
entry_mod2 = Entry(tab11,width=10, font=('Verdana',15))
entry_mod2.grid(row=9, column=1)

label_mod3= Label(tab11, text="ANTONYME", pady=8,font=('Verdana',15))
label_mod3.grid(column=1, row=10)
entry_mod3 = Entry(tab11,width=10, font=('Verdana',15))
entry_mod3.grid(row=11, column=1)

label_mod4= Label(tab11, text="ETHIMOLOGIE", pady=8,font=('Verdana',15))
label_mod4.grid(column=1, row=12)
entry_mod4 = Entry(tab11,width=10, font=('Verdana',15))
entry_mod4.grid(row=13, column=1)

label_mod5= Label(tab11, text="HOMONYME", pady=8,font=('Verdana',15))
label_mod5.grid(column=1, row=14)
entry_mod5 = Entry(tab11,width=10, font=('Verdana',15))
entry_mod5.grid(row=15, column=1)

label_mod6= Label(tab11, text="PARONYME", pady=8,font=('Verdana',15))
label_mod6.grid(column=1, row=16)
entry_mod6 = Entry(tab11,width=10, font=('Verdana',15))
entry_mod6.grid(row=17, column=1)

label_mod7= Label(tab11, text="DIFFICULTE", pady=8,font=('Verdana',15))
label_mod7.grid(column=1, row=18)
entry_mod7 = Entry(tab11,width=10, font=('Verdana',15))
entry_mod7.grid(row=19, column=1)

#////////////////////////////////////////////////SUPPRIMER///////////////////////////////////////////////////////////
button1 = Button(tab12, text="SUPPRIMER", width=12, bg="#03A9F4", fg="#fff", command=supprimer)
button1.grid(row=3, column=1, padx=5, pady=10, ipady=5)

label_sup= Label(tab12, text="WORD", pady=8,font=('Verdana',15))
label_sup.grid(column=1, row=4)
entry_sup = Entry(tab12,width=10, font=('Verdana',15))
entry_sup.grid(row=5, column=1)


#1:home

l1= Label(tab1, text="Mot", pady=8,font=('Verdana',15))
l1.grid(column=0, row=1)
word_raw_entry = StringVar()
entry_word = Entry(tab1, textvariable=word_raw_entry, width=10, font=('Verdana',15))
entry_word.grid(row=1, column=1)

l2= Label(tab1, text="Ethimology",font=('Verdana',15))
l2.grid(column=0, row=2)
syn_raw_entry = StringVar()
entry_meaning = Entry(tab1, textvariable=syn_raw_entry, width=50, font=('Verdana',15))
entry_meaning.grid(row=2, column=1)

l3= Label(tab1, text="Synonymes", pady=8, font=('Verdana',15))
l3.grid(column=0, row=3)
ant_raw_entry = StringVar()
entry_syn = Entry(tab1, textvariable=ant_raw_entry, width=50, font=('Verdana',15))
entry_syn.grid(row=3, column=1)

l3= Label(tab1, text="Paronymes",  font=('Verdana',15))
l3.grid(column=0, row=4)
paro_raw_entry = StringVar()
entry_paro = Entry(tab1, textvariable=paro_raw_entry,width=50, font=('Verdana',15))
entry_paro.grid(row=4, column=1)

l3= Label(tab1, text="Homonymes",pady=8, font=('Verdana',15))
l3.grid(column=0, row=5)
homo_raw_entry = StringVar()
entry_homo = Entry(tab1, textvariable=homo_raw_entry, width=50, font=('Verdana',15))
entry_homo.grid(row=5, column=1)

l4= Label(tab1, text="Antonymes", font=('Verdana',15))
l4.grid(column=0, row=6)
mean_raw_entry = StringVar()
entry_ant = Entry(tab1, textvariable=mean_raw_entry, width=50, font=('Verdana',15))
entry_ant.grid(row=6, column=1)

l5= Label(tab1, text="Difficulte", font=('Verdana',15))
l5.grid(column=0, row=8)
dif_raw_entry = StringVar()
entry_diff = Entry(tab1, textvariable=dif_raw_entry, width=50, font=('Verdana',15))
entry_diff.grid(row=8, column=1)

#/////////////////////////////////////////////button to add our entries to our db/////////////////////////////////////////////////////
button1 = Button(tab1, text="ADD", width=12, bg="#03A9F4", fg="#fff", command=add_details)
button1.grid(row=12, column=1, padx=5, pady=10, ipady=5)

button2 = Button(tab1, text="EFFACER", width=12, bg="#03A9F4", fg="#fff", command=clear_text)
button2.grid(row=13, column=1, padx=5, pady=10, ipady=5)

#///////////////////////////////////////////////////////Display on screen/////////////////////////////////////////////////////

tab1_display = ScrolledText(tab1, height=10)
tab1_display.grid(row=14, column=1, padx=5, pady=10, columnspan=3)

button3 = Button(tab1, text="CLEAR DISPLAY", width=12, bg="#03A9F4", fg="#fff", command=clear_display_result)
button3.grid(row=15, column=1, padx=5, pady=15, ipady=5)

#////////////////////////////////////////////////////View//////////////////////////////////////////////////////////////////
button_view2 = Button(tab8, text="View all", width=12,bg='#03A9FA',fg='#fff',command=view_all_words)
button_view2.grid(row=1, column=0,padx=10,pady=10)
button_view6 = Button(tab8,text="clear", width=12,bg='#03A9FA',fg='#fff',command=clear_tree_view)
button_view6.grid(row=0, column=0,padx=10,pady=10)
#button_view7 = Button(tab6,text="clear", width=12,bg='#03A9FA',fg='#fff',command=edit)
#button_view7.grid(row=2, column=0,padx=10,pady=10)
tree=ttk.Treeview(tab8,columns=("column 1","column2","column3","column4", "column5", "column6","column7","column8"),show='headings')
tree.heading("#1",text="ID")
tree.column("#1",minwidth=0,width=50)
tree.heading("#2",text="MOT")
tree.column("#2",minwidth=0,width=200)
tree.heading("#3",text="ETHIMOLOGY")
tree.column("#3",minwidth=0, anchor=N)
tree.heading("#4",text="SYNONYMES")
tree.column("#4",minwidth=0,width=150)
tree.heading("#5",text="ANTONYMES")
tree.column("#5",minwidth=0,width=150)
tree.heading("#6",text="PARONYME")
tree.column("#6",minwidth=0,width=150)
tree.heading("#7",text="HOMONYME")
tree.column("#7",minwidth=0,width=150)
tree.heading("#8",text="DIFFICULTE")
tree.column("#8",minwidth=0,width=100)
tree.grid(row=15,column=0,padx=0,pady=0, ipadx=0)

#//////////////////////////////////////////////////search synonyme of a word/////////////////////////////////////////////////////////
label1_syn = Label(tab5, text="SYNONMYE", padx=5, pady=5)
label1_syn.grid(column=0, row=1)
search_syn_entry = StringVar()
entry_search_syn = Entry(tab5,textvariable=search_syn_entry,width=30)
entry_search_syn.grid(row=1,column=1)


button_view3=Button(tab5,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_entered_syn_search)
button_view3.grid(row=2,column=1,padx=10,pady=10)

button_view4=Button(tab5,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displaysyn_view)
button_view4.grid(row=2,column=2,padx=10,pady=10)

button_view5=Button(tab5,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_synonyme_by_name)
button_view5.grid(row=1,column=2,padx=10,pady=10)

tab5_display = ScrolledText(tab5,height=5)
tab5_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#///////////////////////////////////////////////////////////////search antonyme of a word//////////////////////////////////////////////////
label1_ayn = Label(tab4, text="ANTONYME", padx=5, pady=5)
label1_ayn.grid(column=0, row=1)
search_ayn = StringVar()
entry_ayn = Entry(tab4,textvariable=search_ayn,width=30)
entry_ayn.grid(row=1,column=1)


button_view7=Button(tab4,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_ayn_search)
button_view7.grid(row=2,column=1,padx=10,pady=10)

button_view7=Button(tab4,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displayayn_view)
button_view7.grid(row=2,column=2,padx=10,pady=10)

button_view7=Button(tab4,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_antonyme_by_name)
button_view7.grid(row=1,column=2,padx=10,pady=10)

tab4_display = ScrolledText(tab4,height=5)
tab4_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#////////////////////////////////////////////////////////search predesseur of a word////////////////////////////////////////////////////
label1_pre = Label(tab10, text="PREDECESSEUR", padx=5, pady=5)
label1_pre.grid(column=0, row=1)
search_pre = StringVar()
entry_pre = Entry(tab10,textvariable=search_pre,width=30)
entry_pre.grid(row=1,column=1)


button_view9=Button(tab10,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_pre_search)
button_view9.grid(row=2,column=1,padx=10,pady=10)

button_view9=Button(tab10,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displaypre_view)
button_view9.grid(row=2,column=2,padx=10,pady=10)

button_view9=Button(tab10,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_predecesseur_by_name)
button_view9.grid(row=1,column=2,padx=10,pady=10)

tab10_display = ScrolledText(tab10,height=5)
tab10_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#//////////////////////////////////////search sucesseur of a word//////////////////////////////////////////////////
label1_suc = Label(tab9, text="SUCESSEUR", padx=5, pady=5)
label1_suc.grid(column=0, row=1)
search_suc = StringVar()
entry_suc = Entry(tab9,textvariable=search_suc,width=30)
entry_suc.grid(row=1,column=1)


button_view8=Button(tab9,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_suc_search)
button_view8.grid(row=2,column=1,padx=10,pady=10)

button_view8=Button(tab9,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displaysuc_view)
button_view8.grid(row=2,column=2,padx=10,pady=10)

button_view8=Button(tab9,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_successeur_by_name)
button_view8.grid(row=1,column=2,padx=10,pady=10)

tab9_display = ScrolledText(tab9,height=5)
tab9_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#///////////////////////////////////////search homonyme of a word///////////////////////////////////////////////////
label1_hym = Label(tab6, text="HOMONYME", padx=5, pady=5)
label1_hym.grid(column=0, row=1)
search_hyn = StringVar()
entry_hyn = Entry(tab6,textvariable=search_hyn,width=30)
entry_hyn.grid(row=1,column=1)


button_view10=Button(tab6,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_hyn_search)
button_view10.grid(row=2,column=1,padx=10,pady=10)

button_view10=Button(tab6,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displayhym_view)
button_view10.grid(row=2,column=2,padx=10,pady=10)

button_view10=Button(tab6,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_homonyme_by_name)
button_view10.grid(row=1,column=2,padx=10,pady=10)

tab6_display = ScrolledText(tab6,height=5)
tab6_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#//////////////////////////////////////////search paromyne of a word///////////////////////////////////////////////////
label1_paro = Label(tab7, text="PARONYME", padx=5, pady=5)
label1_paro.grid(column=0, row=1)
search_paro = StringVar()
entry_par = Entry(tab7,textvariable=search_paro,width=30)
entry_par.grid(row=1,column=1)

button_view11=Button(tab7,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_paro_search)
button_view11.grid(row=2,column=1,padx=10,pady=10)

button_view11=Button(tab7,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displayparo_view)
button_view11.grid(row=2,column=2,padx=10,pady=10)

button_view11=Button(tab7,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_paronyme_by_name)
button_view11.grid(row=1,column=2,padx=10,pady=10)

tab7_display = ScrolledText(tab7,height=5)
tab7_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#//////////////////////////////////////////////search ethimologie of a word//////////////////////////////////////////////////
label1_eth = Label(tab3, text="ETHIMOLOGIE", padx=5, pady=5)
label1_eth.grid(column=0, row=1)
search_eth = StringVar()
entry_eth = Entry(tab3,textvariable=search_eth,width=30)
entry_eth.grid(row=1,column=1)


button_view12=Button(tab3,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_eth_search)
button_view12.grid(row=2,column=1,padx=10,pady=10)

button_view12=Button(tab3,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displayeth_view)
button_view12.grid(row=2,column=2,padx=10,pady=10)

button_view12=Button(tab3,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_ethimologie_by_name)
button_view12.grid(row=1,column=2,padx=10,pady=10)

tab3_display = ScrolledText(tab3,height=5)
tab3_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#/////////////////////////////// DIFFICULTER ////////////////////////////////////////////////////////////////////////

label1_dif = Label(tab13, text="DIFFICULTER", padx=5, pady=5)
label1_dif.grid(column=0, row=1)
search_dif = StringVar()
entry_dif = Entry(tab13,textvariable=search_dif,width=30)
entry_dif.grid(row=1,column=1)


button_view13=Button(tab13,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_dif_search)
button_view13.grid(row=2,column=1,padx=10,pady=10)

button_view13=Button(tab13,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_displaydif_view)
button_view13.grid(row=2,column=2,padx=10,pady=10)

button_view13=Button(tab13,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_difficulte_by_name)
button_view13.grid(row=1,column=2,padx=10,pady=10)

tab11_display = ScrolledText(tab13,height=5)
tab11_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

#/////////////////////////////////////////////////////////search//////////////////////////////////////////////////////////////////
label1_search = Label(tab2, text="View", padx=5, pady=5)
label1_search.grid(column=0, row=1)
search_raw_entry = StringVar()
entry_search = Entry(tab2,textvariable=search_raw_entry,width=30)
entry_search.grid(row=1,column=1)


button_view3=Button(tab2,text="clear search",width=12,bg='#03A9F4',fg="#fff",command=clear_entered_search)
button_view3.grid(row=2,column=1,padx=10,pady=10)

button_view4=Button(tab2,text="clear results",width=12,bg='#03A9F4',fg="#fff",command=clear_display_view)
button_view4.grid(row=2,column=2,padx=10,pady=10)

button_view5=Button(tab2,text="search",width=12,bg='#03A9F4',fg="#fff",command=search_word_by_name)
button_view5.grid(row=1,column=2,padx=10,pady=10)

tab2_display = ScrolledText(tab2,height=5)
tab2_display.grid(row=10,column=0,columnspan=3,padx=5,pady=5)

fenetre.mainloop()
