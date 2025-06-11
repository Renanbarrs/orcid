# ORCID Data Extractor

Este projeto contém dois scripts Python para buscar e exibir informações públicas de pesquisadores na plataforma ORCID, utilizando a API pública do ORCID.

## Pré-requisitos
- Python 3.7 ou superior
- Biblioteca `requests` instalada

Você pode instalar a biblioteca `requests` com o comando:
```bash
"pip install requests"

Como usar
1. Pesquisa por ID ORCID (Para teste e validação do programa)
O script api_orcid_id.py permite buscar informações detalhadas de um pesquisador a partir do ID ORCID.

Como executar:

Você será solicitado a digitar o ID ORCID (exemplo: 0000-0002-1825-0097).
O script irá exibir:

Nome completo
E-mails (se públicos)
Biografia (se pública)
Palavras-chave
Outros nomes
País
URLs de pesquisa
Empregos (afiliações profissionais)
Educação (afiliações acadêmicas)
Produções científicas (título, ano, tipo, DOI, etc)

2. Pesquisa por Nome
O script api_orcid_nome.py permite buscar informações a partir do nome e sobrenome do pesquisador.

Como executar:

Você será solicitado a digitar o primeiro nome e o sobrenome.
O script irá buscar o primeiro resultado correspondente na base ORCID e exibir as mesmas informações detalhadas listadas acima.

Observações
Os scripts retornam apenas informações públicas disponíveis na API do ORCID.
Alguns campos podem aparecer como "Não disponível" caso o pesquisador não tenha tornado a informação pública.
O script de busca por nome retorna apenas o primeiro resultado encontrado na busca do ORCID.
Estrutura dos arquivos
api_orcid_id.py: Busca por ID ORCID.
api_orcid_nome.py: Busca por nome e sobrenome

Link de pesquisa da orcid: https://orcid.org/orcid-search/search