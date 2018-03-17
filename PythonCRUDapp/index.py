from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Aplicação Python: CRUD Simples")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 900
height = 500
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(0, 0)

# ==================================VARIABLES==========================================
NOMECOMP = StringVar()
GENERO = StringVar()
ENDERECO = StringVar()
USERNAME = StringVar()
SENHA = StringVar()

# ==================================FRAME==============================================
Top = Frame(root, width=900, height=50, bd=8, relief="raise")
Top.pack(side=TOP)
Left = Frame(root, width=300, height=500, bd=8, relief="raise")
Left.pack(side=LEFT)
Right = Frame(root, width=600, height=500, bd=8, relief="raise")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, height=100, bd=8, relief="raise")
Buttons.pack(side=BOTTOM)
RadioGroup = Frame(Forms)
Masculino = Radiobutton(RadioGroup, text="Masculino", variable=GENERO, value="Masculino", font=('arial', 16)).pack(side=LEFT)
Feminino = Radiobutton(RadioGroup, text="Feminino", variable=GENERO, value="Feminino", font=('arial', 16)).pack(side=LEFT)

# ==================================LABEL WIDGET=======================================
txt_title = Label(Top, width=900, font=('arial', 24), text="Python: Simple CRUD Application")
txt_title.pack()
txt_nomecompleto = Label(Forms, text="Digite seu nome completo:", font=('arial', 16), bd=15)
txt_nomecompleto.grid(row=0, stick="e")
txt_gender = Label(Forms, text="Seu gênero:", font=('arial', 16), bd=15)
txt_gender.grid(row=1, stick="e")
txt_address = Label(Forms, text="Endereço:", font=('arial', 16), bd=15)
txt_address.grid(row=2, stick="e")
txt_username = Label(Forms, text="Nome de Usuario:", font=('arial', 16), bd=15)
txt_username.grid(row=3, stick="e")
txt_password = Label(Forms, text="Senha:", font=('arial', 16), bd=15)
txt_password.grid(row=4, stick="e")
txt_resultado = Label(Buttons)
txt_resultado.pack(side=TOP)

# ==================================ENTRY WIDGET=======================================
firstname = Entry(Forms, textvariable=NOMECOMP, width=50)
firstname.grid(row=0, column=1)
RadioGroup.grid(row=1, column=1)
address = Entry(Forms, textvariable=ENDERECO, width=30)
address.grid(row=2, column=1)
username = Entry(Forms, textvariable=USERNAME, width=30)
username.grid(row=3, column=1)
password = Entry(Forms, textvariable=SENHA, show="*", width=30)
password.grid(row=4, column=1)

# ==================================BUTTONS WIDGET=====================================
btn_create = Button(Buttons, width=10, text="Adicionar", command=Create)
btn_create.pack(side=LEFT)
btn_read = Button(Buttons, width=10, text="Pesquisar", command=Read)
btn_read.pack(side=LEFT)
btn_update = Button(Buttons, width=10, text="Atualizar", state=DISABLED)
btn_update.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Excluir", state=DISABLED)
btn_delete.pack(side=LEFT)
btn_exit = Button(Buttons, width=10, text="Sair", command=Exit)
btn_exit.pack(side=LEFT)

# ==================================LIST WIDGET========================================
scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=("NomeCompleto", "Genero", "Endereco", "Username", "Senha"),
                    selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('NomeCompleto', text="Nome Completo", anchor=W)
tree.heading('Genero', text="Gênero", anchor=W)
tree.heading('Endereco', text="Endereço", anchor=W)
tree.heading('Username', text="Username", anchor=W)
tree.heading('Senha', text="Nome de Usuário", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=80)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=80)
tree.column('#4', stretch=NO, minwidth=0, width=150)
tree.column('#5', stretch=NO, minwidth=0, width=120)
tree.pack()

#==================================METHODS============================================
def Database():
    global conn, cursor
    conn = sqlite3.connect('dbcrudpython.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `usuario` "
                   "(user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nomeComp TEXT,"
                   " genero TEXT, endereco TEXT, username TEXT, senha TEXT)")

def Create():
    if  NOMECOMP.get() == "" or GENERO.get() == "" or ENDERECO.get() == "" or USERNAME.get() == "" or SENHA.get() == "":
        txt_resultado.config(text="Por favor verifique os campos!", fg="red")
    else:
        Database()
        cursor.execute("INSERT INTO `usuario` (nomeComp, genero, endereco, username, senha)"
                       " VALUES(?, ?, ?, ?, ?)",
                       (str(NOMECOMP.get()), str(GENERO.get()), str(ENDERECO.get()),
                        str(USERNAME.get()), str(SENHA.get())))
        conn.commit()
        NOMECOMP.set("")
        GENERO.set("")
        ENDERECO.set("")
        USERNAME.set("")
        SENHA.set("")
        cursor.close()
        conn.close()
        txt_resultado.config(text="Usuário cadastrado com sucesso", fg="green")

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM `usuario` ORDER BY `nomeComp` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[1], data[2], data[3], data[4], data[5]))
    cursor.close()
    conn.close()
    txt_resultado.config(text="Pesquisa realizada com sucesso", fg="black")

def Exit():
    result = tkMessageBox.askquestion('Aplicação Python: CRUD Simples', 'Deseja sair da aplicação?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

#==================================INITIALIZATION=====================================
if __name__ == '__main__':
    root.mainloop()