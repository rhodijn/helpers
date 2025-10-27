import paramiko
from dotenv import dotenv_values
from pathlib import Path

SECRETS = dotenv_values('.env')


def list_remote_dir(
    hostname: str,
    username: str,
    password: str | None = None,
    key_path: str | None = None,
    remote_dir: str = ".",
) -> list[Path]:
    """
    Stellt per SSH eine Verbindung zum Server her und gibt die Einträge
    des angegebenen Verzeichnisses als pathlib.Path‑Objekte zurück.

    Parameters
    ----------
    hostname:   Ziel‑Hostname oder IP‑Adresse
    username:   SSH‑Benutzername
    password:   Passwort (wenn kein Schlüssel verwendet wird)
    key_path:   Pfad zu einer privaten Schlüsseldatei (optional)
    remote_dir: Pfad des Remote‑Verzeichnisses, das gelistet werden soll

    Returns
    -------
    List von pathlib.Path‑Objekten (Datei‑ und Ordnernamen)
    """
    # --- 1. Transport / Authentifizierung vorbereiten --------------------
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Authentifizierung: entweder Passwort oder privater Schlüssel
    if key_path:
        pkey = paramiko.RSAKey.from_private_key_file(key_path)
        client.connect(hostname, username=username, pkey=pkey)
    else:
        client.connect(hostname, username=username, password=password)

    # --- 2. SFTP‑Session öffnen -----------------------------------------
    sftp = client.open_sftp()

    # --- 3. Verzeichnisinhalt abfragen ----------------------------------
    entries = sftp.listdir_attr(remote_dir)   # liefert SFTPAttributes
    paths = [Path(entry.filename) for entry in entries]

    # Optional: nur Dateien anzeigen (keine Unterordner)
    # paths = [p for p, e in zip(paths, entries) if not e.st_mode & 0o040000]

    # --- 4. Aufräumen ----------------------------------------------------
    sftp.close()
    client.close()

    return paths


# ----------------------------------------------------------------------
# Beispielaufruf
if __name__ == "__main__":
    HOST = SECRETS['FTP_URL']
    USER = SECRETS['FTP_USER']
    PASS = SECRETS['FTP_PASS']         # oder setze `key_path` statt PASS
    REMOTE_DIR = "public/swisscovery/inhaltsverzeichnis/"

    try:
        files = list_remote_dir(HOST, USER, password=PASS, remote_dir=REMOTE_DIR)
        print(f"Inhalt von {REMOTE_DIR} auf {HOST}:")
        for f in files:
            print(" -", f)
    except Exception as e:
        print("Fehler beim Zugriff:", e)