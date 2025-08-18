def criar_saudacao():
    def ola():
        print("Oi!")
    return ola

f = criar_saudacao()
f()  # chama a função retornada
