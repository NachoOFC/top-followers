"""
Actualiza el README.md con los seguidores mas seguidos (top N),
usando la API oficial de GitHub en vez de scraping/Selenium.
"""

import os
import sys
import time
import urllib.request
import urllib.error
import json
from datetime import datetime, timezone

API_URL = "https://api.github.com"
START_MARKER = "<!-- FOLLOWERS_LIST_START -->"
END_MARKER = "<!-- FOLLOWERS_LIST_END -->"


def gh_request(path, token):
    """Hace un GET a la API de GitHub y devuelve el JSON parseado."""
    req = urllib.request.Request(
        f"{API_URL}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "readme-top-followers-script",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode()), resp.headers
    except urllib.error.HTTPError as e:
        print(f"Error {e.code} pidiendo {path}: {e.read().decode()}", file=sys.stderr)
        raise


def get_all_followers(username, token):
    """Trae TODOS los seguidores del usuario, paginando de 100 en 100."""
    followers = []
    page = 1
    while True:
        data, _ = gh_request(
            f"/users/{username}/followers?per_page=100&page={page}", token
        )
        if not data:
            break
        followers.extend(data)
        page += 1
    return followers


def get_follower_counts(followers, token):
    """Para cada seguidor, consulta su cantidad de seguidores propia."""
    enriched = []
    total = len(followers)
    for i, f in enumerate(followers, start=1):
        login = f["login"]
        try:
            profile, headers = gh_request(f"/users/{login}", token)
        except urllib.error.HTTPError:
            continue

        enriched.append(
            {
                "login": login,
                "name": profile.get("name") or login,
                "followers": profile.get("followers", 0),
                "avatar_url": profile.get("avatar_url", ""),
                "html_url": profile.get("html_url", f"https://github.com/{login}"),
            }
        )

        # Cortesia con el rate limit: si queda poco margen, esperamos.
        remaining = headers.get("X-RateLimit-Remaining")
        if remaining is not None and int(remaining) < 50:
            reset = int(headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset - time.time(), 0) + 1
            print(f"Cerca del rate limit, esperando {wait:.0f}s...")
            time.sleep(wait)

        if i % 100 == 0:
            print(f"Procesados {i}/{total} seguidores...")

    return enriched


def build_table(top_followers):
    lines = [
        "### My Most Famous Followers",
        "",
        "| Profile | Name | Followers |",
        "| --- | --- | --- |",
    ]
    for f in top_followers:
        avatar = f'<img src="{f["avatar_url"]}" width="40" height="40">'
        profile_link = f'[{avatar}]({f["html_url"]})'
        name_link = f'[{f["name"]}]({f["html_url"]})'
        lines.append(f'| {profile_link} | {name_link} | {f["followers"]} |')

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.append("")
    lines.append(f"*Última actualización: {now}*")
    return "\n".join(lines)


def update_readme(table_md, readme_path="README.md"):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER not in content or END_MARKER not in content:
        print(
            f"ERROR: No encontre los marcadores {START_MARKER} / {END_MARKER} "
            f"en {readme_path}. Agregalos donde quieras que aparezca la tabla.",
            file=sys.stderr,
        )
        sys.exit(1)

    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]

    new_content = f"{before}{START_MARKER}\n{table_md}\n{END_MARKER}{after}"

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)


def main():
    username = os.environ["GITHUB_USER_NAME"]
    max_count = int(os.environ.get("MAX_FOLLOWER_COUNT", "10"))
    token = os.environ["GH_TOKEN"]

    print(f"Buscando seguidores de {username}...")
    followers = get_all_followers(username, token)
    print(f"Encontrados {len(followers)} seguidores. Consultando sus perfiles...")

    enriched = get_follower_counts(followers, token)
    enriched.sort(key=lambda f: f["followers"], reverse=True)
    top = enriched[:max_count]

    table_md = build_table(top)
    update_readme(table_md)
    print("README.md actualizado correctamente.")


if __name__ == "__main__":
    main()
