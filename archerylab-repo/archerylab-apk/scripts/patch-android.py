#!/usr/bin/env python3
"""Προσθέτει permissions κάμερας/μικροφώνου στο AndroidManifest και ορίζει versionCode/versionName."""
import os, re, pathlib

root = pathlib.Path("android/app")
mf = root / "src/main/AndroidManifest.xml"
xml = mf.read_text(encoding="utf-8")

perms = [
    '<uses-permission android:name="android.permission.CAMERA" />',
    '<uses-permission android:name="android.permission.RECORD_AUDIO" />',
    '<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />',
    '<uses-feature android:name="android.hardware.camera" android:required="false" />',
    '<uses-feature android:name="android.hardware.camera.autofocus" android:required="false" />',
    '<uses-feature android:name="android.hardware.microphone" android:required="false" />',
]
add = [p for p in perms if p.split('"')[1] not in xml]
if add:
    block = "\n    ".join(add) + "\n\n    "
    xml = xml.replace("<application", block + "<application", 1)
    mf.write_text(xml, encoding="utf-8")
    print("Manifest: added", len(add), "entries")

gr = root / "build.gradle"
g = gr.read_text(encoding="utf-8")
code = os.environ.get("VERSION_CODE", "1")
name = os.environ.get("VERSION_NAME", "1.0")
g = re.sub(r"versionCode\s+\d+", f"versionCode {code}", g, count=1)
g = re.sub(r'versionName\s+"[^"]*"', f'versionName "{name}"', g, count=1)
gr.write_text(g, encoding="utf-8")
print(f"build.gradle: versionCode={code} versionName={name}")
