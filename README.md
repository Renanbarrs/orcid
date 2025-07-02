# ORCID Data Extractor

Este projeto contém dois scripts Python para buscar e exibir informações públicas de pesquisadores na plataforma ORCID, utilizando a API pública do ORCID.

## Pré-requisitos
- Python 3.7 ou superior
- Biblioteca `requests` instalada

Você pode instalar a biblioteca `requests` com o comando:
```bash
pip install requests
```

## Como usar

### 1. Pesquisa por Nome

O script `api_orcid_nome.py` permite buscar informações a partir do **nome e sobrenome** do pesquisador.

**Como executar:**
```bash
python api_orcid_nome.py
```
Você será solicitado a digitar o primeiro nome e o sobrenome.
O script irá buscar o primeiro resultado correspondente na base ORCID e **retornará um objeto estruturado no modelo esperado pelo banco de dados**, preenchendo os campos possíveis com os dados públicos disponíveis na API ORCID.

O objeto retornado segue o modelo:
- Campos como `banca`, `endereco`, `area`, `grandeArea`, `especialidades` e `usuario` são preenchidos como `None` ou lista vazia, pois não são fornecidos pela API pública.
- Os campos preenchidos são: nome, email (se público), titulação e ano de conclusão (se disponíveis na educação), e produções científicas.

---
## Endpoints da API ORCID utilizados

- **Buscar pessoa por nome:**  
  `GET https://pub.orcid.org/v3.0/search/?q=family-name:{sobrenome}+AND+given-names:{nome}`

- **Buscar dados pessoais:**  
  `GET https://pub.orcid.org/v3.0/{orcid_id}/person`

- **Buscar produções científicas:**  
  `GET https://pub.orcid.org/v3.0/{orcid_id}/works`

- **Buscar afiliações (educação):**  
  `GET https://pub.orcid.org/v3.0/{orcid_id}/educations`

- **Buscar afiliações (empregos):**  
  `GET https://pub.orcid.org/v3.0/{orcid_id}/employments`
  
## Observações
- Os scripts retornam apenas informações públicas disponíveis na API do ORCID.
- Alguns campos podem aparecer como "Não disponível" ou `None` caso o pesquisador não tenha tornado a informação pública.
- O script de busca por nome retorna apenas o primeiro resultado encontrado na busca do ORCID.
- O script `api_orcid_nome.py` já retorna o objeto pronto para ser salvo no banco de dados, conforme o modelo esperado pela aplicação.

---

## Estrutura dos arquivos
- `api_orcid_id.py`: Busca por ID ORCID e exibe informações detalhadas.
- `api_orcid_nome.py`: Busca por nome e sobrenome e retorna o objeto no modelo do banco de dados.

---

## Sobre chave de API

> **Atenção:**  
> Esta aplicação utiliza apenas a **API pública do ORCID**, que não exige chave de API, token ou autenticação para acesso aos dados públicos.  
> Caso seja necessário acessar dados privados no futuro, será preciso registrar a aplicação no ORCID e obter credenciais específicas.

---

## Conteinerização com Docker

A aplicação pode ser executada em qualquer ambiente que tenha Docker instalado, sem necessidade de instalar Python ou dependências manualmente.

### Como gerar e rodar a imagem Docker:

1. **Build da imagem:**
   ```sh
   docker build -t orcid-app .

## Executando diretamente pelo Docker Hub

Se preferir, você pode rodar a aplicação sem baixar os arquivos do projeto, utilizando a imagem publicada no Docker Hub:

1. **Baixe a imagem:**
   ```sh
   docker pull rajastx/orcid-app
   ```

2. **Execute o container:**
   ```sh
   docker run -it rajastx/orcid-app
   ```

> O parâmetro `-it` permite interação com o terminal para digitar nome e sobrenome.

## Link de pesquisa da ORCID
https://orcid.org/orcid-search/search
```