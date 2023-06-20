import os
import psycopg2
from asseclas import objeto, usuario

SQL_DELETA_OBJETO = 'delete from objeto where id = %s'
SQL_OBJETO_POR_ID = 'select id, coduser, comentario from objeto where id=%s'
SQL_USUARIO_POR_CODUSER = 'select id, coduser, nome, senha from usuario where coduser=%s'
SQL_ATUALIZA_OBJETO = 'update objeto set coduser=%s, comentario=%s where id=%s'
SQL_BUSCA_OBJETO = 'select id, coduser, comentario from objeto'
SQL_CRIA_OBJETO = 'insert into objeto (coduser, comentario) values (%s, %s)'


class ComentarioDao:
    def __init__(self, db):
        self.__db = db
        
    def salvar(self, Objeto):
        cursor = self.__db.cursor()
        
        if (Objeto.id):
            cursor.execute(SQL_ATUALIZA_OBJETO, (Objeto.coduser, Objeto.comentario, Objeto.id))
        else:
            cursor.execute(SQL_CRIA_OBJETO, (Objeto.coduser, Objeto.comentario))
            Objeto.id = cursor.lastrowid
        self.__db.commit()
        return Objeto
    
    def listar(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_BUSCA_OBJETO)
        objetos = traduz_objetos(cursor.fetchall())
        return objetos
    
    def busca_por_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_OBJETO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return objeto(*tupla)
    
    def deletar(self, id):
        self.__db.cursor().execute(SQL_DELETA_OBJETO, (id,))
        self.__db.commit()
        
class UsuarioDao:
    def __init__(self, db):
        self.__db = db
        
    def buscar_por_coduser(self, coduser):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USUARIO_POR_CODUSER, (coduser,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario
    
def traduz_objetos(objetos):
    def cria_objeto_com_tupla(tupla):
        return objeto(tupla[1], tupla[2], id=tupla[0])
    return list(map(cria_objeto_com_tupla, objetos))

def traduz_usuario(tupla):
    return usuario(tupla[0], tupla[1], tupla[2], tupla[3])