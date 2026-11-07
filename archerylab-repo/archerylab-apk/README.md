# Archery Lab – APK μέσω GitHub Actions

## Γρήγορη εκκίνηση (debug APK, χωρίς κωδικούς)
1. Στο repo σου ανέβασε το περιεχόμενο αυτού του zip στη ΡΙΖΑ (φάκελοι `.github` και `archerylab-apk`).
2. Πήγαινε **Actions → Build APK → Run workflow** (ή απλά κάνε push στο `main`).
3. Όταν τελειώσει (~5-8 λεπτά): άνοιξε το run → **Artifacts → ArcheryLab-debug** → κατέβασε το zip → μέσα είναι το `app-debug.apk`.
4. Στο κινητό: ενεργοποίησε "Εγκατάσταση από άγνωστες πηγές" και εγκατέστησε το APK.

## Υπογεγραμμένο release APK (προαιρετικό)
1. Φτιάξε keystore (μία φορά, φύλαξέ το σε ασφαλές μέρος — αν χαθεί δεν μπορείς να ενημερώσεις την εφαρμογή):
   `keytool -genkey -v -keystore release.jks -alias archery -keyalg RSA -keysize 2048 -validity 10000`
2. Μετατροπή σε base64:  
   Linux/Mac: `base64 -w0 release.jks > keystore.b64`  
   Windows (PowerShell): `[Convert]::ToBase64String([IO.File]::ReadAllBytes("release.jks")) | Out-File keystore.b64`
3. Στο GitHub: **Settings → Secrets and variables → Actions → New repository secret**:
   - `KEYSTORE_BASE64` = το περιεχόμενο του keystore.b64
   - `KEYSTORE_PASSWORD` = ο κωδικός του keystore
   - `KEY_ALIAS` = `archery` (ή ό,τι έβαλες)
   - `KEY_PASSWORD` = ο κωδικός του κλειδιού (ίδιος με του keystore αν δεν έβαλες άλλον)
4. Τρέξε ξανά το workflow → θα βγει και το artifact **ArcheryLab-release** (`ArcheryLab-release.apk`).
5. Για Release με λινκ λήψης: `git tag v1.0.0 && git push --tags`.

## Τι περιέχει
- `www/` – η εφαρμογή (index.html, manifest, icons) + `native-bridge.js`
- `native-bridge.js` – στο APK το κουμπί **Αποθήκευση** ανοίγει το μενού κοινοποίησης του Android
  (Αρχεία / Drive / Γκαλερί), γιατί τα blob downloads δεν δουλεύουν στο WebView.
- `scripts/patch-android.py` – βάζει permissions κάμερας/μικροφώνου και αριθμό έκδοσης.
- `../.github/workflows/build.yml` – το build (στη ρίζα του repo).
- `assets/` – icon-only.png, icon-foreground.png, icon-background.png: από αυτά παράγονται όλα τα εικονίδια της εφαρμογής (adaptive + legacy).

## Αλλαγές
- Όνομα εφαρμογής / appId: `capacitor.config.json` (το appId `gr.archerylab.app` να μην αλλάξει μετά την πρώτη δημοσίευση).
- Όταν αλλάξεις το `www/index.html`, κάνε commit και το build ξαναβγαίνει αυτόματα.
