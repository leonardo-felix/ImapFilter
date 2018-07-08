from django.db import models
from django.contrib import admin

class Email(models.Model):
    descricao = models.CharField(max_length=20)
    email = models.CharField(max_length=250)
    senha = models.CharField(max_length=250)

    def __str__(self):
        return self.descricao

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    pass


class Regra(models.Model):
    email_id = models.ForeignKey(Email, on_delete=models.CASCADE)
    pasta_pesquisar = models.CharField(max_length=250, default='INBOX')
    pasta_destino = models.CharField(max_length=250)

    def __str__(self):
        return "de {0} para {1}".format(self.pasta_pesquisar, self.pasta_destino)


@admin.register(Regra)
class RegraAdmin(admin.ModelAdmin):
    pass


class ItemRegra(models.Model):
    DE = 'FROM'
    PARA = 'TO'
    COPIA = 'CC'

    OPCOES_VALIDACAO = (
        (DE, 'Remetente'),
        (PARA, 'Destinatário'),
        (COPIA, 'Destinatário em cópia')
    )

    regra_id = models.ForeignKey(Regra, on_delete=models.CASCADE)
    validacao = models.CharField(max_length=4, choices=OPCOES_VALIDACAO)
    conteudo = models.CharField(max_length=250)

    def __str__(self):
        return "{0} *{1}*".format(self.validacao, self.conteudo)


@admin.register(ItemRegra)
class ItemRegraAdmin(admin.ModelAdmin):
    pass







