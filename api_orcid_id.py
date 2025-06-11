import requests
import json

orcid_id = input("Digite o ID do ORCID: ").strip()  #solicita o ID ao usuário
url = f"https://pub.orcid.org/v3.0/{orcid_id}"

headers = {
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print("Não foi possível coletar os dados.")
    exit()

data = response.json()

try:
    # Nome completo
    nome = data["person"]["name"]
    nome_completo = f"{nome['given-names']['value']} {nome['family-name']['value']}"

    # E-mails (se públicos)
    emails = [e.get("email") for e in data["person"].get("emails", {}).get("email", [])]
    emails = emails if emails else ["Não disponível"]

    # Biografia
    bio_obj = data["person"].get("biography")
    biografia = bio_obj.get("content") if bio_obj else "Não disponível"

    # Palavras-chave
    keywords = data["person"].get("keywords", {}).get("keyword", [])
    palavras_chave = [k.get("content", "") for k in keywords]

    # Outros nomes
    outros_nomes = [n.get("content", "") for n in data["person"].get("other-names", {}).get("other-name", [])]

    # País (primeiro endereço, se existir)
    pais = None
    addresses = data["person"].get("addresses", {}).get("address", [])
    if addresses:
        pais = addresses[0].get("country", {}).get("value", None)

    # URLs de pesquisa
    urls = [u.get("url", {}).get("value", "") for u in data["person"].get("researcher-urls", {}).get("researcher-url", [])]

    # Instituições/afiliações (empregos)
    emp_url = f"https://pub.orcid.org/v3.0/{orcid_id}/employments"
    emp_resp = requests.get(emp_url, headers=headers)
    empregos = []
    if emp_resp.status_code == 200:
        emp_data = emp_resp.json()
        for emp in emp_data.get("employment-summary", []):
            empregos.append({
                "instituicao": emp.get("organization", {}).get("name"),
                "departamento": emp.get("department-name"),
                "cargo": emp.get("role-title"),
                "inicio": emp.get("start-date", {}),
                "fim": emp.get("end-date", {}),
                "cidade": emp.get("organization", {}).get("address", {}).get("city"),
                "pais": emp.get("organization", {}).get("address", {}).get("country")
            })

    # Instituições/afiliações (educação)
    edu_url = f"https://pub.orcid.org/v3.0/{orcid_id}/educations"
    edu_resp = requests.get(edu_url, headers=headers)
    educacoes = []
    if edu_resp.status_code == 200:
        edu_data = edu_resp.json()
        for edu in edu_data.get("education-summary", []):
            educacoes.append({
                "instituicao": edu.get("organization", {}).get("name"),
                "departamento": edu.get("department-name"),
                "curso": edu.get("role-title"),
                "inicio": edu.get("start-date", {}),
                "fim": edu.get("end-date", {}),
                "cidade": edu.get("organization", {}).get("address", {}).get("city"),
                "pais": edu.get("organization", {}).get("address", {}).get("country")
            })

    # Produções científicas
    works_url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    works_resp = requests.get(works_url, headers=headers)
    producoes = []
    if works_resp.status_code == 200:
        works_data = works_resp.json()
        for group in works_data.get("group", []):
            work = group.get("work-summary", [])[0]
            producoes.append({
                "titulo": work.get("title", {}).get("title", {}).get("value"),
                "ano": work.get("publication-date", {}).get("year", {}).get("value"),
                "tipo": work.get("type"),
                "doi": next((extid.get("value") for extid in work.get("external-ids", {}).get("external-id", []) if extid.get("external-id-type") == "doi"), None),
                "url": work.get("url", {}).get("value"),
                "fonte": work.get("source", {}).get("source-name", {}).get("value"),
            })

    print(f"\nNome completo: {nome_completo}")
    print(f"\nE-mails: {', '.join(emails)}")
    print(f"\nBiografia: {biografia}")
    print("\nPalavras-chave:")
    for k in palavras_chave:
        print("\n-", k)
    print("\nOutros nomes:")
    for n in outros_nomes:
        print("\n-", n)
    print(f"\nPaís: {pais if pais else 'Não disponível'}")
    print("\nURLs de pesquisa:")
    for u in urls:
        print("\n-", u)
    print("\nEmpregos:")
    for emp in empregos:
        print("\n-", emp)
    print("\nEducação:")
    for edu in educacoes:
        print("\n-", edu)
    print("\nProduções científicas:")
    for prod in producoes:
        print("\n-", prod)

except Exception as e:
    print("\nNão foi possível coletar os dados.")
    print("\nErro:", e)