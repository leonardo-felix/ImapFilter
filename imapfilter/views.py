from django.shortcuts import render

import imaplib


def listar(request):

    imap_conn = imaplib.IMAP4_SSL(host='mail.bennercloud.com.br')
    print(imap_conn.login('leonardo.felix@benner.com.br', '6!sF'))
    print(imap_conn.list('INBOX'))
    imap_conn.select()
    status, emails_list = imap_conn.search(None, 'UNSEEN FROM "camed"')
    for email_id in emails_list:
        print("Email_id: {0}".format(email_id))
        print(imap_conn.copy(email_id, 'INBOX.Clientes.Camed'))
    return render(request, 'listar.html')