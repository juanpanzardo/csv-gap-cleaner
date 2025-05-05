import os
import shutil
import re
from mutagen import File

# === CONFIGURACIÓN ===
ORIGEN = os.path.expanduser("~/MusicaLimpia")
DESTINO = "/Volumes/ESPARTA/MusicaOrganizadaTest"
EXTENSIONES = [".mp3", ".m4a"]

# === FUNCIONES DE LIMPIEZA ===
def limpiar_texto(texto):
    if not texto:
        return "desconocido"
    texto = texto.lower()
    texto = re.sub(r"\\s*\\(video oficial\\)|\\(official video\\)|\\(official music video\\)|\\(live.*?\\)", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"[\\U0001F600-\\U0001F64F\\U0001F300-\\U0001F5FF\\U0001F680-\\U0001F6FF]+", "-", texto)
    texto = re.sub(r"[\"'!?¿¡,:;\[\]{}|<>#%&=*~`^@]", "", texto)
    texto = texto.strip()
    return texto if texto else "desconocido"

def obtener_metadata(ruta):
    audio = File(ruta, easy=True)
    if not audio:
        return None
    genero = limpiar_texto(audio.get("genre", ["desconocido"])[0])
    artista = limpiar_texto(audio.get("artist", ["desconocido"])[0])
    titulo = limpiar_texto(audio.get("title", [os.path.splitext(os.path.basename(ruta))[0]])[0])
    return genero, artista, titulo

def organizar_archivo(ruta_archivo):
    genero, artista, titulo = obtener_metadata(ruta_archivo)
    extension = os.path.splitext(ruta_archivo)[1].lower()
    nueva_ruta = os.path.join(DESTINO, genero, artista)
    os.makedirs(nueva_ruta, exist_ok=True)
    destino_final = os.path.join(nueva_ruta, f"{titulo}{extension}")

    # evitar sobrescritura
    if os.path.exists(destino_final):
        base, ext = os.path.splitext(destino_final)
        i = 1
        while os.path.exists(f"{base}_{i}{ext}"):
            i += 1
        destino_final = f"{base}_{i}{ext}"

    shutil.copy2(ruta_archivo, destino_final)
    print(f"✔ {ruta_archivo} → {destino_final}")

# === PROCESO PRINCIPAL ===
print("\n📁 Iniciando organización de archivos...")
for carpeta_raiz, _, archivos in os.walk(ORIGEN):
    for archivo in archivos:
        if any(archivo.lower().endswith(ext) for ext in EXTENSIONES):
            ruta_completa = os.path.join(carpeta_raiz, archivo)
            try:
                organizar_archivo(ruta_completa)
            except Exception as e:
                print(f"⚠ Error con {archivo}: {e}")

print("\n✅ Organización completada.")
