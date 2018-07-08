import imaplib
import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LPFX.settings")
django.setup()

from imapfilter import models


class MoverEmail:
    def __init__(self, email):
        self.email = email.email
        self.senha = email.senha
        self.email_id = email.id

    def processar(self):
        imap_conn = imaplib.IMAP4_SSL(host='mail.bennercloud.com.br')
        status, msg = imap_conn.login(self.email, self.senha)

        if status != 'OK':
            return self._sair_graciosamente(status, msg)

        for regra in models.Regra.objects.filter(email_id__exact=self.email_id):
            status, msg = imap_conn.select(mailbox=regra.pasta_pesquisar)
            print("Retorno pesquisar {0}: '{1}' '{2}'".format(regra.pasta_pesquisar, status, msg))
            if status != 'OK':
                return self._sair_graciosamente(status, msg)

            itens_regra = models.ItemRegra.objects.filter(regra_id__exact=regra.id)

            if itens_regra.count() > 0:
                regra_str = ' '.join([str(item_regra) for item_regra in
                                      models.ItemRegra.objects.filter(regra_id__exact=regra.id)])
                print("Pesquisando: UNSEEN {0}".format(regra_str))
                status, lista_emails = imap_conn.search(None, 'UNSEEN {0}'.format(regra_str))
                lista_emails = [email for email in lista_emails if email != b'']

                print("Existe(m) {0} email a ser movido pela regra {1}".format(len(lista_emails), regra))

                for email_id in lista_emails:
                    status, msg = imap_conn.copy(email_id, regra.pasta_destino)

                    if status == 'OK':
                        imap_conn.store(email_id, '+FLAGS', '\\Deleted')
                        imap_conn.expunge()
                        print("Movido email {0} de {1} para {2}".format(email_id, regra.pasta_pesquisar,
                                                                        regra.pasta_destino))

    @staticmethod
    def _sair_graciosamente(status, msg):
        print("Status '{0}' não OK, saindo.\r\nmensagem: {1}".format(status, msg))


def mover_email():
    emails = models.Email.objects.all()
    for email in emails:
        cop = MoverEmail(email)
        cop.processar()


if __name__ == '__main__':
    mover_email()
