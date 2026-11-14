# Checklist MFA — sair do SMS em 5 minutos por conta

SMS como segundo fator não basta mais: o golpe de troca de chip (SIM swap) e a clonagem
de número deixam o código cair no celular do golpista. Use **app autenticador**
(TOTP) ou, melhor ainda, **chave física / passkey**.

| Método | Proteção | Observação |
|---|---|---|
| Só senha | fraca | troque já |
| SMS / ligação | fraca | cai em SIM swap e clonagem |
| E-mail | média | só vale se o e-mail tiver MFA forte |
| App autenticador (TOTP) | boa | Google Authenticator, Microsoft Authenticator, Aegis (Android), 2FAS, Ente Auth |
| Passkey / chave física (FIDO2) | ótima | YubiKey, Titan, passkey do celular; resiste a phishing |

## Ordem de prioridade
1. [ ] **E-mail principal** (é a chave de recuperação de tudo)
2. [ ] **Bancos e corretoras** (inclusive app do banco e cartão)
3. [ ] **Gerenciador de senhas**
4. [ ] **Conta Google / Apple / Microsoft** do celular
5. [ ] **WhatsApp** (confirmação em duas etapas com PIN)
6. [ ] **Redes sociais** e contas de trabalho
7. [ ] **Domínio, hospedagem, GitHub** (se você tem site ou código)
8. [ ] **Operadora do celular**: peça senha/PIN para portabilidade e troca de chip

## Passo a passo em cada conta
1. [ ] Instale o app autenticador (uma vez só).
2. [ ] Na conta: Segurança → Verificação em duas etapas → "App autenticador".
3. [ ] Leia o QR code com o app e digite o código de 6 dígitos.
4. [ ] **Salve os códigos de recuperação** (imprima; guarde junto do dinheiro do kit).
5. [ ] **Remova o SMS** como método, se a conta deixar.
6. [ ] Se a conta aceitar passkey ou chave física, cadastre também.
7. [ ] Marque no relatório: `python3 seguranca/auditoria_contas.py`.

## Cuidados
- [ ] Faça backup do app autenticador (exportar criptografado ou app com sincronização).
- [ ] Nunca passe código por telefone ou mensagem, para ninguém.
- [ ] Uma senha diferente por conta (gerenciador de senhas resolve).
- [ ] Revise a cada 6 meses, junto com o kit da casa.
