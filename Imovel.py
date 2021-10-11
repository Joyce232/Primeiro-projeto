from peewee import SqliteDatabase, Model, TextField, FloatField

db = SqliteDatabase('imoveis.db')


class Imovel(Model):
    endereco = TextField()
    bairro = TextField()
    preco = FloatField()
    desconto = FloatField()
    modalidade = TextField()

    def __str__(self):
        return f"{self.id}: {self.bairro} - {self.preco}: {self.desconto} - {self.modalidade}"

    class Meta:
        database = db








