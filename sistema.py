import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

class ProntuarioEletronico:
    def __init__(self, root):
        self.root = root
        self.root.title("Prontuário Eletrônico")
        self.root.configure(bg="#FFDB55")  # Cor de fundo principal

        # Centralizar a janela
        self.center_window(1200, 800)
        
        # Canvas e barras de rolagem
        self.canvas = tk.Canvas(root, bg="#FFDB55")
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Adicionar logomarca
        self.logo_path = "123.png"  # Certifique-se de ter uma imagem chamada '123.png' no mesmo diretório
        self.logo_img = Image.open(self.logo_path)
        self.logo = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = tk.Label(self.scrollable_frame, image=self.logo, bg="#FFDB55")
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Campos de entrada de dados conforme o PDF
        self.create_label_entry("Nome da Criança:", 1)
        self.create_label_dateentry("Data de Nascimento:", 2)
        self.create_label_entry("Idade:", 3)
        self.create_label_entry("Sexo (M/F):", 4)
        self.create_label_dateentry("Data da Avaliação:", 5)
        self.create_label_dateentry("Data do Início:", 6)
        self.create_label_entry("Diagnóstico de Origem:", 7)
        self.create_label_entry("Responsável pela Criança:", 8)

        # Campos de telefone com DDD
        self.create_label_phone("Telefone (DDD + Número):", 9)

        # História Clínica
        self.create_label_text("Gravidez (saúde da mãe, movimentos fetais, parto, peso ao nascer,\n"
                               "gestação programada, pré-natal, intercorrências):", 10, height=5)
        
        # Exame Físico
        self.create_label_text("Tônus (pescoço, tronco e membros):", 11, height=3)
        self.create_label_text("Padrões Motores e Posturais:", 12, height=10)

        # AVD's
        self.create_label_text("AVD's (Alimentação, Higiene, Vestuário):", 13, height=5)

        # Avaliação postural e controle da função motora
        self.create_label_text("Avaliação postural:", 14, height=5)
        self.create_label_text("Avaliação do controle da função motora:", 15, height=5)

        # Informações Complementares
        self.create_label_entry("Medicação:", 16)
        self.create_label_entry("Cirurgia prévia:", 17)
        self.create_label_entry("Órteses:", 18)
        self.create_label_entry("Exames complementares:", 19)
        self.create_label_entry("Objetivo / preocupação dos Pais:", 20)
        self.create_label_entry("Se criança maior ou adolescente: função que deseja como meta:", 21)
        self.create_label_text("Objetivos:", 22, height=5)
        self.create_label_text("Tratamento:", 23, height=5)

        # Botão Salvar
        self.save_button = ttk.Button(self.scrollable_frame, text="Salvar", command=self.salvar_prontuario)
        self.save_button.grid(row=24, column=0, columnspan=2, padx=10, pady=10, sticky='e')
        
        # Pesquisar Paciente
        self.search_label = ttk.Label(self.scrollable_frame, text="Pesquisar Paciente:", background="#D9EAD3")
        self.search_label.grid(row=25, column=0, padx=10, pady=10, sticky='e')
        self.search_entry = ttk.Entry(self.scrollable_frame, width=50)
        self.search_entry.grid(row=25, column=1, padx=10, pady=10)
        
        # Botão Pesquisar
        self.search_button = ttk.Button(self.scrollable_frame, text="Pesquisar", command=self.pesquisar_prontuario)
        self.search_button.grid(row=26, column=1, padx=10, pady=10, sticky='e')

        # Botão Ver Arquivos
        self.view_button = ttk.Button(self.scrollable_frame, text="Ver Arquivos", command=self.ver_arquivos)
        self.view_button.grid(row=27, column=1, padx=10, pady=10, sticky='e')

        # Menu
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Exportar", command=self.exportar_prontuario)
        file_menu.add_command(label="Imprimir", command=self.imprimir_prontuario)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=root.quit)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.sobre)

        # Evento para rolar com a bolinha do mouse
        self.root.bind_all("<MouseWheel>", self._on_mouse_wheel)

    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_label_entry(self, text, row):
        label = ttk.Label(self.scrollable_frame, text=text, background="#D9EAD3")
        label.grid(row=row, column=0, padx=10, pady=5, sticky='e')
        entry = ttk.Entry(self.scrollable_frame, width=50)
        entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"entry_{row}", entry)
    
    def create_label_text(self, text, row, height):
        label = ttk.Label(self.scrollable_frame, text=text, background="#D9EAD3")
        label.grid(row=row, column=0, padx=10, pady=5, sticky='ne')
        text_widget = tk.Text(self.scrollable_frame, height=height, width=50, bg="#FFFFFF", fg="#000000", bd=2, relief="solid")
        text_widget.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"text_{row}", text_widget)

    def create_label_dateentry(self, text, row):
        label = ttk.Label(self.scrollable_frame, text=text, background="#D9EAD3")
        label.grid(row=row, column=0, padx=10, pady=5, sticky='e')
        date_entry = DateEntry(self.scrollable_frame, width=47, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/MM/yyyy', locale='pt_BR')
        date_entry.grid(row=row, column=1, padx=10, pady=5)
        setattr(self, f"entry_{row}", date_entry)
    
    def create_label_phone(self, text, row):
        label = ttk.Label(self.scrollable_frame, text=text, background="#D9EAD3")
        label.grid(row=row, column=0, padx=10, pady=5, sticky='e')
        frame = ttk.Frame(self.scrollable_frame)
        frame.grid(row=row, column=1, padx=10, pady=5)
        ddd_entry = ttk.Entry(frame, width=5)
        ddd_entry.pack(side="left")
        number_entry = ttk.Entry(frame, width=44)
        number_entry.pack(side="left")
        setattr(self, f"ddd_{row}", ddd_entry)
        setattr(self, f"number_{row}", number_entry)

    def salvar_prontuario(self):
        nome_paciente = self.entry_1.get().strip()

        dados = {
            "Data de Nascimento": self.entry_2.get().strip(),
            "Idade": self.entry_3.get().strip(),
            "Sexo (M/F)": self.entry_4.get().strip(),
            "Data da Avaliação": self.entry_5.get().strip(),
            "Data do Início": self.entry_6.get().strip(),
            "Diagnóstico de Origem": self.entry_7.get().strip(),
            "Responsável pela Criança": self.entry_8.get().strip(),
            "Telefone (DDD)": self.ddd_9.get().strip(),
            "Telefone (Número)": self.number_9.get().strip(),
            "Gravidez (saúde da mãe, movimentos fetais, parto, peso ao nascer, gestação\nprogramada, pré-natal, intercorrências)": self.text_10.get("1.0", tk.END).strip(),
            "Tônus": self.text_11.get("1.0", tk.END).strip(),
            "Padrões Motores e Posturais": self.text_12.get("1.0", tk.END).strip(),
            "AVD's": self.text_13.get("1.0", tk.END).strip(),
            "Avaliação postural": self.text_14.get("1.0", tk.END).strip(),
            "Avaliação do controle da função motora": self.text_15.get("1.0", tk.END).strip(),
            "Medicação": self.entry_16.get().strip(),
            "Cirurgia prévia": self.entry_17.get().strip(),
            "Órteses": self.entry_18.get().strip(),
            "Exames complementares": self.entry_19.get().strip(),
            "Objetivo / preocupação dos Pais": self.entry_20.get().strip(),
            "Função que deseja como meta": self.entry_21.get().strip(),
            "Objetivos": self.text_22.get("1.0", tk.END).strip(),
            "Tratamento": self.text_23.get("1.0", tk.END).strip()
        }

        if not nome_paciente:
            messagebox.showwarning("Aviso", "Nome do paciente é obrigatório!")
            return

        filename = f"{nome_paciente}.txt"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"\n\n{'-'*40}\nData/Hora: {now}\n"

        for key, value in dados.items():
            entry += f"{key}: {value}\n"

        with open(filename, "a") as file:
            file.write(entry)

        messagebox.showinfo("Sucesso", f"Prontuário salvo com sucesso para {nome_paciente}!")
        self.limpar_campos()

    def pesquisar_prontuario(self):
        nome_paciente = self.search_entry.get().strip()

        if not nome_paciente:
            messagebox.showwarning("Aviso", "Nome do paciente é obrigatório para pesquisa!")
            return

        filename = f"{nome_paciente}.txt"

        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
            self.mostrar_prontuario(nome_paciente, content)
        else:
            messagebox.showwarning("Aviso", f"Nenhum prontuário encontrado para {nome_paciente}!")

    def mostrar_prontuario(self, nome_paciente, content):
        window = tk.Toplevel(self.root)
        window.title(f"Prontuário de {nome_paciente}")
        window.state("zoomed")

        # Canvas e barra de rolagem
        canvas = tk.Canvas(window)
        scroll_y = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # Divisão em linhas
        linhas = content.split('\n')
        row = 0

        for linha in linhas:
            if linha.strip() == "":
                continue
            if ':' in linha:
                campo, valor = linha.split(':', 1)
                campo_label = tk.Label(scrollable_frame, text=campo + ":", fg="red", anchor="w", justify="left")
                campo_label.grid(row=row, column=0, sticky="w")
                valor_label = tk.Label(scrollable_frame, text=valor.strip(), anchor="w", justify="left", wraplength=500)
                valor_label.grid(row=row, column=1, sticky="w")
            else:
                separator = tk.Label(scrollable_frame, text=linha, anchor="w", justify="left")
                separator.grid(row=row, column=0, columnspan=2, sticky="w")
            row += 1

        # Evento para rolar com a bolinha do mouse
        window.bind_all("<MouseWheel>", self._on_mouse_wheel)

        window.transient(self.root)
        window.grab_set()
        self.root.wait_window(window)

    def limpar_campos(self):
        for i in range(1, 24):
            if hasattr(self, f"entry_{i}"):
                getattr(self, f"entry_{i}").delete(0, tk.END)
            elif hasattr(self, f"text_{i}"):
                getattr(self, f"text_{i}").delete("1.0", tk.END)
        self.ddd_9.delete(0, tk.END)
        self.number_9.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def exportar_prontuario(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            with open(filename, "w") as file:
                file.write("Prontuário exportado!")
            messagebox.showinfo("Exportar", f"Prontuário exportado com sucesso para {filename}!")

    def imprimir_prontuario(self):
        filename = filedialog.askopenfilename(defaultextension=".txt",
                                              filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            os.startfile(filename, "print")

    def ver_arquivos(self):
        arquivos = [f for f in os.listdir() if f.endswith('.txt')]
        if not arquivos:
            messagebox.showinfo("Ver Arquivos", "Nenhum arquivo de prontuário encontrado.")
            return

        window = tk.Toplevel(self.root)
        window.title("Arquivos de Prontuário")
        window.state("zoomed")

        # Canvas e barra de rolagem
        canvas = tk.Canvas(window)
        scroll_y = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        listbox = tk.Listbox(scrollable_frame, selectmode=tk.SINGLE, width=80, height=20)
        for arquivo in arquivos:
            listbox.insert(tk.END, arquivo)
        listbox.pack()

        view_button = ttk.Button(scrollable_frame, text="Abrir", command=lambda: self.abrir_arquivo(listbox))
        view_button.pack(pady=10)

        # Botão flutuante de impressão
        print_button = ttk.Button(scrollable_frame, text="Imprimir", command=self.imprimir_prontuario)
        print_button.pack(pady=10)

        # Evento para rolar com a bolinha do mouse
        window.bind_all("<MouseWheel>", self._on_mouse_wheel)

        window.transient(self.root)
        window.grab_set()
        self.root.wait_window(window)

    def abrir_arquivo(self, listbox):
        selecionado = listbox.curselection()
        if not selecionado:
            return
        filename = listbox.get(selecionado)
        with open(filename, "r") as file:
            content = file.read()
        self.mostrar_prontuario(filename.replace(".txt", ""), content)

    def sobre(self):
        messagebox.showinfo("Sobre", "Prontuário Eletrônico\nVersão 1.0\nDesenvolvido por [Tiago viana da cruz 88993464285]")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProntuarioEletronico(root)
    root.mainloop()
