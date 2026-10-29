#!/usr/bin/env python3
"""Decode a Google Drive MCP download_file_content result (JSON with base64
`content`) and write the bytes to the destination path recorded in
drive_inventory.json. Verifies magic bytes and appends to manifest.json.

Usage:
  python3 -I save_drive_result.py <tool-result.json> <driveId>
  python3 -I save_drive_result.py --text <path-to-text-file> <driveId-or-label> <localPath> <mimeType>
  python3 -I save_drive_result.py --finalize
"""
import base64
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
INV = os.path.join(HERE, "drive_inventory.json")
MANIFEST = os.path.join(DATA, "manifest.json")

MAGIC = {
    "application/pdf": b"%PDF",
    "image/png": b"\x89PNG\r\n\x1a\n",
}


def load_manifest():
    if os.path.exists(MANIFEST):
        with open(MANIFEST) as f:
            return json.load(f)
    return []


def save_manifest(m):
    os.makedirs(DATA, exist_ok=True)
    with open(MANIFEST, "w") as f:
        json.dump(m, f, indent=2)


def upsert(m, entry):
    m[:] = [e for e in m if e["driveId"] != entry["driveId"]]
    m.append(entry)


def main():
    args = sys.argv[1:]
    manifest = load_manifest()

    if args and args[0] == "--finalize":
        manifest.sort(key=lambda e: (e["folder"], e["title"]))
        save_manifest(manifest)
        print(json.dumps({"total": len(manifest), "ok": sum(1 for e in manifest if e["ok"])}))
        return

    if args and args[0] == "--text":
        _, src, drive_id, local_path, mime = args[:5]
        dest = os.path.join(DATA, local_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(src, "rb") as f:
            data = f.read()
        with open(dest, "wb") as f:
            f.write(data)
        entry = {"driveId": drive_id, "title": os.path.basename(local_path),
                 "folder": os.path.dirname(local_path), "localPath": "data/" + local_path,
                 "bytes": len(data), "mimeType": mime, "ok": len(data) > 0}
        upsert(manifest, entry)
        save_manifest(manifest)
        print(json.dumps(entry))
        return

    with open(INV) as f:
        inv = {e["driveId"]: e for e in json.load(f)}

    if args and args[0] == "--sweep":
        # Process every tool-result file in a directory whose id is in the inventory.
        d = args[1]
        done = {e["driveId"] for e in manifest if e["ok"]}
        for name in sorted(os.listdir(d)):
            if "download_file_content" not in name and not name.startswith("toolu_"):
                continue
            p = os.path.join(d, name)
            try:
                with open(p) as f:
                    res = json.load(f)
            except Exception:
                continue
            if isinstance(res, list):
                # MCP envelope: [{type:text,text:"{...}"}]
                res = next((x for x in res if isinstance(x, dict) and x.get("type") == "text"), None)
                if res is None:
                    continue
                try:
                    res = json.loads(res["text"])
                except Exception:
                    continue
            if "content" in res and isinstance(res["content"], list):
                res = json.loads(res["content"][0]["text"])
            if not isinstance(res, dict):
                continue
            fid = res.get("id")
            if fid in inv and fid not in done:
                entry = save_one(inv[fid], res, fid)
                upsert(manifest, entry)
                done.add(fid)
                print(json.dumps(entry))
        save_manifest(manifest)
        missing = [e["title"] for i, e in inv.items() if i not in done]
        print(json.dumps({"saved": len(done), "missing": missing}))
        return

    src, drive_id = args[0], args[1]
    meta = inv[drive_id]
    with open(src) as f:
        res = json.load(f)
    if isinstance(res, list):
        res = next(x for x in res if isinstance(x, dict) and "content" in x)
    if "content" in res and isinstance(res["content"], list):
        res = json.loads(res["content"][0]["text"])
    entry = save_one(meta, res, drive_id)
    upsert(manifest, entry)
    save_manifest(manifest)
    print(json.dumps(entry))


def save_one(meta, res, drive_id):
    data = base64.b64decode(res["content"])
    if res.get("id") and res["id"] != drive_id:
        raise SystemExit(f"id mismatch: result {res['id']} != {drive_id}")
    mime = res.get("mimeType") or meta["mimeType"]
    magic = MAGIC.get(meta["mimeType"])
    ok = True
    if magic is not None:
        ok = data.startswith(magic)
    elif meta["mimeType"] == "application/json":
        try:
            json.loads(data)
        except Exception:
            ok = False
    rel = os.path.join(meta["folder"], meta["title"])
    dest = os.path.join(DATA, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    return {"driveId": drive_id, "title": meta["title"], "folder": meta["folder"],
            "localPath": "data/" + rel, "bytes": len(data), "mimeType": mime, "ok": bool(ok)}


if __name__ == "__main__":
    main()
