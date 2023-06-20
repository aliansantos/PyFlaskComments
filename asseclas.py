class usuario:
    def __init__(self, id, coduser, nome, senha):
        self.id = id
        self.coduser = coduser
        self.nome = nome
        self.senha = senha
        
class objeto:
    def __init__(self, coduser, comentario, id=None):
        self.id = id
        self.coduser = coduser
        self.comentario = comentario