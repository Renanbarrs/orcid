import requests
import json
from datetime import datetime, timezone

def buscar_dados_orcid_modelo(orcid_id, headers):
    # Busca dados básicos
    url_person = f"https://pub.orcid.org/v3.0/{orcid_id}/person"
    resp_person = requests.get(url_person, headers=headers)
    person = resp_person.json() if resp_person.status_code == 200 else {}

    # Busca produções científicas
    url_works = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    resp_works = requests.get(url_works, headers=headers)
    works = resp_works.json() if resp_works.status_code == 200 else {}

    # Busca afiliações (educação)
    url_edu = f"https://pub.orcid.org/v3.0/{orcid_id}/educations"
    resp_edu = requests.get(url_edu, headers=headers)
    educations = resp_edu.json() if resp_edu.status_code == 200 else {}

    # Busca afiliações (empregos)
    url_emp = f"https://pub.orcid.org/v3.0/{orcid_id}/employments"
    resp_emp = requests.get(url_emp, headers=headers)
    employments = resp_emp.json() if resp_emp.status_code == 200 else {}

    # Nome e email
    nome = person.get("name", {}).get("given-names", {}).get("value", "")
    sobrenome = person.get("name", {}).get("family-name", {}).get("value", "")
    email = None
    emails = person.get("emails", {}).get("email", [])
    if emails:
        email = emails[0].get("email")

    # Produções científicas
    producoes = []
    if works.get("group"):
        for group in works["group"]:
            work = group.get("work-summary", [])[0]
            producoes.append({
                "id": None,
                "titulo": work.get("title", {}).get("title", {}).get("value"),
                "ano": work.get("publication-date", {}).get("year", {}).get("value"),
                "tipo": work.get("type"),
                "fonte": "ORCID",
                "autores": None,  # Não disponível na API pública
                "doi": next((extid.get("value") for extid in work.get("external-ids", {}).get("external-id", []) if extid.get("external-id-type") == "doi"), None),
                "citacoes": None  # Não disponível na API pública
            })

    # Educação (primeira, se existir)
    titulacao = None
    anoConclusao = None
    if educations.get("education-summary"):
        edu = educations["education-summary"][0]
        titulacao = edu.get("role-title")
        end_date = edu.get("end-date", {})
        anoConclusao = end_date.get("year", {}).get("value")

    # Gênero não disponível na API pública
    genero = None

    # Monta o objeto no modelo solicitado
    objeto = {
        "id": None,
        "criado": datetime.now(timezone.utc).isoformat(),
        "atualizado": datetime.now(timezone.utc).isoformat(),
        "egresso": {
            "id": None,
            "nome": f"{nome} {sobrenome}".strip(),
            "email": email,
            "titulacao": titulacao,
            "genero": genero,
            "anoConclusao": anoConclusao
        },
        "banca": None,  # Não disponível
        "endereco": None,  # Não disponível
        "area": None,  # Não disponível
        "grandeArea": None,  # Não disponível
        "especialidades": [],  # Não disponível
        "producoesCientificas": producoes,
        "usuario": None  # Não preencher
    }
    return objeto

# Solicita nome e sobrenome do usuário
nome = input("Digite o primeiro nome da pessoa: ").strip()
sobrenome = input("Digite o sobrenome da pessoa: ").strip()

# Monta a query de busca
query = f"family-name:{sobrenome}+AND+given-names:{nome}"
search_url = f"https://pub.orcid.org/v3.0/search/?q={query}"
headers = {"Accept": "application/json"}

# Faz a busca pelo nome e sobrenome
search_resp = requests.get(search_url, headers=headers)
search_data = search_resp.json()

resultados = search_data.get("result", [])
if not resultados:
    print("Nenhum resultado encontrado.")
    exit()

# Usa o primeiro ORCID encontrado
orcid_id = resultados[0]["orcid-identifier"]["path"]

objeto = buscar_dados_orcid_modelo(orcid_id, headers)
print(json.dumps(objeto, indent=4, ensure_ascii=False))