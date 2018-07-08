import imaplib
import django
import os
from apscheduler.schedulers.blocking import BlockingScheduler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LPFX.settings")
django.setup()

from imapfilter import models


class MoverEmail:
    def __init__(self, email):
        self.email = email.email
        self.senha = email.senha
        self.email_id = email.id

    def _item_regra(self, item_regra_id):
        item_regra = models.ItemRegra.objects.get(id=item_regra_id)
        return '{0} "{1}"'.format(item_regra.validacao, item_regra.conteudo)

    def processar(self):
        imap_conn = imaplib.IMAP4_SSL(host='mail.bennercloud.com.br')
        status, msg = imap_conn.login(self.email, self.senha)

        if status != 'OK':
            return self._sair_graciosamente(status, msg)

        for regra in models.Regra.objects.filter(email_id__exact=self.email_id):
            imap_conn.select(mailbox=regra.pasta_pesquisar)
            itens_regra = models.ItemRegra.objects.filter(regra_id__exact=regra.id)

            if itens_regra.count() > 0:
                regra_lista = [self._item_regra(item_regra.id) for item_regra in
                               models.ItemRegra.objects.filter(regra_id__exact=regra.id)]
                status, lista_emails = imap_conn.search(None, 'UNSEEN {0}'.format(' '.join(regra_lista)))
                lista_emails = [email for email in lista_emails if email != b'']

                for email_id in lista_emails:
                    status, msg = imap_conn.copy(email_id, regra.pasta_destino)

                    if status == 'OK':
                        imap_conn.store(email_id, '+FLAGS', '\\Deleted')
                        imap_conn.expunge()

    @staticmethod
    def _sair_graciosamente(status, msg):
        print("Status '{0}' não OK, saindo.\r\nmensagem: {1}".format(status, msg))









sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=1)
def mover_email():
    emails = models.Email.objects.all()
    for email in emails:
        cop = MoverEmail(email)
        cop.processar()


sched.start()