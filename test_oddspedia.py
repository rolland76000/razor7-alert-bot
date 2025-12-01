import requests
from datetime import datetime, timezone

URL = "https://oddspedia.com/fr/u/razor7"

def main():
    now = datetime.now(timezone.utc).isoformat()
    print("=" * 60)
    print(f"[{now}] Test d'accès à {URL}")
    print("-" * 60)

    try:
        resp = requests.get(URL, timeout=20)
        status = resp.status_code

        print(f"Statut HTTP : {status}")
        print(f"Content-Type : {resp.headers.get('content-type')}")
        print(f"Taille de la réponse : {len(resp.text)} caractères")

        if 200 <= status < 300:
            print("\n➡️ Interprétation : accès OK (2xx). On pourra construire un script par-dessus.")
        elif 300 <= status < 400:
            print("\n➡️ Interprétation : redirection (3xx).")
            print(f"Location : {resp.headers.get('location')}")
        elif status == 403:
            print("\n❌ Interprétation : 403 Forbidden.")
            print("   - Probable blocage côté Oddspedia pour ce type de requête / IP.")
            print("   - Dans ce cas, on n'insistera pas depuis GitHub (respect du site).")
        elif status == 429:
            print("\n⚠️ Interprétation : 429 Too Many Requests (rate limit).")
            print("   - Il faut réduire fortement la fréquence ou arrêter.")
        else:
            print("\n⚠️ Interprétation : statut inattendu, à analyser manuellement.")

        print("\n--- Aperçu des 500 premiers caractères du HTML ---")
        print(resp.text[:500])

    except Exception as e:
        print("\n❌ Erreur lors de la requête :")
        print(repr(e))

if __name__ == "__main__":
    main()

