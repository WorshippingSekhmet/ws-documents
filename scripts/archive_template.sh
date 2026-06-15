#!/bin/bash
set -euo pipefail

# ------------------------------------------------------------
# Archiviert die aktive Template-Datei in das archive/ Verzeichnis,
# prüft zuvor die konfigurierten Abhängigkeiten und setzt einen Git-Tag.
# 
# In CI-Umgebungen (CI=true) läuft das Skript vollautomatisch ohne interaktive Prompts.
# 
# Nutzung: ./scripts/archive_template.sh <version> [template_path] [deps_path]
# Beispiel: ./scripts/archive_template.sh v8.7
# ------------------------------------------------------------

# ---------- Parameter ----------
VERSION="${1:-}"
TEMPLATE_PATH="${2:-docs/vas/templates/vas_adt_companion_template_wlk_adt.md}"
DEPS_FILE="${3:-docs/vas/dependencies.cfg}"

if [ -z "$VERSION" ]; then
    echo "❌ Fehler: Bitte Version angeben, z.B. v8.7"
    exit 1
fi

# ---------- CI-Erkennung ----------
CI="${CI:-false}"
if [ "$CI" = "true" ]; then
    echo "🤖 CI-Umgebung erkannt – Überspringe interaktive Abfragen."
    AUTO_OVERWRITE="${AUTO_OVERWRITE:-false}"   # Standard: nicht überschreiben
    AUTO_PUSH_TAG="${AUTO_PUSH_TAG:-true}"      # Standard: Tag automatisch pushen
else
    AUTO_OVERWRITE=""   # später interaktiv
    AUTO_PUSH_TAG=""
fi

# ---------- Pfade normalisieren ----------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

ACTIVE_FILE="$TEMPLATE_PATH"
ARCHIVE_DIR="$(dirname "$ACTIVE_FILE")/archive"
ARCHIVE_FILE="$ARCHIVE_DIR/$(basename "$ACTIVE_FILE" .md)_$VERSION.md"

# ---------- Prüfen, ob aktive Datei existiert ----------
if [ ! -f "$ACTIVE_FILE" ]; then
    echo "❌ Aktive Template-Datei nicht gefunden: $ACTIVE_FILE"
    exit 1
fi

# ---------- Abhängigkeitsprüfung ----------
check_dependencies() {
    local template_file="$1"
    local deps_file="$2"
    
    if [ ! -f "$deps_file" ]; then
        echo "⚠️ Keine Abhängigkeitsdatei gefunden: $deps_file → Überspringe Prüfung."
        return 0
    fi
    
    echo "🔍 Prüfe Abhängigkeiten gegen $deps_file ..."
    
    set -a
    source "$deps_file"
    set +a
    
    local template_vas_version
    template_vas_version=$(grep -Eo 'VAS v[0-9]+\.[0-9]+' "$template_file" | head -1 | tr -d ' ')
    
    local template_ws_vic_hash
    template_ws_vic_hash=$(grep -E 'WS-ViC-001' -A1 "$template_file" | tail -1 | grep -Eo '[a-fA-F0-9]{64}' | head -1)
    
    local template_framework_hash
    template_framework_hash=$(grep -E 'WS-Framework-Charter' -A1 "$template_file" | tail -1 | grep -Eo '[a-fA-F0-9]{64}' | head -1)
    
    local failed=0
    if [ -n "${VAS_VERSION:-}" ] && [ "$template_vas_version" != "$VAS_VERSION" ]; then
        echo "❌ VAS-Version mismatch: Template '$template_vas_version' vs. erwartet '$VAS_VERSION'"
        failed=1
    fi
    
    if [ -n "${WS_VIC_001_HASH:-}" ] && [ "$template_ws_vic_hash" != "$WS_VIC_001_HASH" ]; then
        echo "❌ WS-ViC-001 Hash mismatch: Template '$template_ws_vic_hash' vs. erwartet '$WS_VIC_001_HASH'"
        failed=1
    fi
    
    if [ -n "${WS_FRAMEWORK_CHARTER_HASH:-}" ] && [ "$template_framework_hash" != "$WS_FRAMEWORK_CHARTER_HASH" ]; then
        echo "❌ WS-Framework-Charter Hash mismatch: Template '$template_framework_hash' vs. erwartet '$WS_FRAMEWORK_CHARTER_HASH'"
        failed=1
    fi
    
    if [ $failed -eq 1 ]; then
        echo "❌ Abhängigkeitsprüfung fehlgeschlagen. Archivierung abgebrochen."
        exit 1
    fi
    
    echo "✅ Alle Abhängigkeiten erfüllt."
}

check_dependencies "$ACTIVE_FILE" "$DEPS_FILE"

# ---------- Archivieren ----------
mkdir -p "$ARCHIVE_DIR"

if [ -f "$ARCHIVE_FILE" ]; then
    if [ "$CI" = "true" ]; then
        if [ "$AUTO_OVERWRITE" = "true" ]; then
            echo "⚠️ Archivdatei existiert: $ARCHIVE_FILE (überschreibe automatisch)"
        else
            echo "❌ Archivdatei existiert bereits: $ARCHIVE_FILE (AUTO_OVERWRITE nicht gesetzt) → Abbruch."
            exit 1
        fi
    else
        read -p "Archivdatei existiert bereits. Überschreiben? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Abgebrochen."
            exit 1
        fi
    fi
fi

cp "$ACTIVE_FILE" "$ARCHIVE_FILE"
echo "✅ Kopiert nach: $ARCHIVE_FILE"

ARCHIVE_HASH=$(sha256sum "$ARCHIVE_FILE" | cut -d ' ' -f1)
echo "📦 SHA-256 der archivierten Datei: $ARCHIVE_HASH"

# ---------- Git-Tag setzen ----------
TAG_NAME="template/adt-wlk/$VERSION"

tag_exists=false
if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    tag_exists=true
fi

if [ "$tag_exists" = true ]; then
    if [ "$CI" = "true" ]; then
        if [ "${AUTO_OVERWRITE_TAG:-false}" = "true" ]; then
            echo "⚠️ Git-Tag $TAG_NAME existiert – wird überschrieben (AUTO_OVERWRITE_TAG=true)"
            git tag -d "$TAG_NAME"
            git push origin ":refs/tags/$TAG_NAME" 2>/dev/null || true
        else
            echo "❌ Git-Tag $TAG_NAME existiert bereits. Setze AUTO_OVERWRITE_TAG=true zum Überschreiben. Abbruch."
            exit 1
        fi
    else
        echo "⚠️ Git-Tag $TAG_NAME existiert bereits."
        read -p "Tag überschreiben und neu setzen? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "⏩ Tag übersprungen."
            exit 0
        else
            git tag -d "$TAG_NAME"
            git push origin ":refs/tags/$TAG_NAME" 2>/dev/null || true
        fi
    fi
fi

git tag -a "$TAG_NAME" -m "Archive Template $VERSION (Hash: $ARCHIVE_HASH)"
echo "✅ Tag gesetzt: $TAG_NAME"

# ---------- Tag pushen ----------
if [ "$CI" = "true" ]; then
    if [ "$AUTO_PUSH_TAG" = "true" ]; then
        git push origin "$TAG_NAME"
        echo "✅ Tag gepusht (automatisch)."
    else
        echo "⏩ Tag nicht gepusht (AUTO_PUSH_TAG=false)."
    fi
else
    read -p "Tag jetzt pushen? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin "$TAG_NAME"
        echo "✅ Tag gepusht."
    else
        echo "⏩ Tag nicht gepusht. Du kannst später 'git push origin $TAG_NAME' ausführen."
    fi
fi

echo "🎉 Archivierung abgeschlossen."