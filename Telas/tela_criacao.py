from Configurações.Config import *

def enviar_formulario():
    nome = entry_nome.get()
    email = entry_email.get()
    senha = entry_senha.get()
    
    # Aqui você pode processar os dados do formulário, como salvá-los em um arquivo ou banco de dados
    
    # Exemplo de impressão dos dados:
    print("Nome:", nome)
    print("Email:", email)
    print("Senha:", senha)

# Criar uma instância da janela principal
janela = tk.Tk()
janela.title("Formulário")

# Criar rótulos e campos de entrada para cada campo do formulário
label_nome = tk.Label(janela, text="Qunatidade de Jogadores:")
label_nome.grid(row=0, column=0, padx=10, pady=5)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=5)

label_email = tk.Label(janela, text="Bias:")
label_email.grid(row=1, column=0, padx=10, pady=5)
entry_email = tk.Entry(janela)
entry_email.grid(row=1, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="Configuração de Camadas:")
label_senha.grid(row=2, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=2, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="funções das Camadas:")
label_senha.grid(row=3, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=3, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="Partidas por Geração:")
label_senha.grid(row=4, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=4, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="Número de Projeteis:")
label_senha.grid(row=5, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=5, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="Número de players:")
label_senha.grid(row=6, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=6, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="Taxa de elitismo:")
label_senha.grid(row=7, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=7, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="Taxa de Mutação:")
label_senha.grid(row=8, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=8, column=1, padx=10, pady=5)

label_senha = tk.Label(janela, text="Reconpensa objetivo:")
label_senha.grid(row=9, column=0, padx=10, pady=5)
entry_senha = tk.Entry(janela, show="*")  # A opção show="*" faz com que a senha seja ocultada
entry_senha.grid(row=9, column=1, padx=10, pady=5)

# Botão para enviar o formulário
botao_enviar = tk.Button(janela, text="Enviar", command=enviar_formulario)
botao_enviar.grid(row=10, columnspan=2, padx=10, pady=10)

# Iniciar o loop principal da janela
janela.mainloop()