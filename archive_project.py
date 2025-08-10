import os, textwrap, zipfile, pathlib, json, shutil, datetime, io, sys, functools

@functools.lru_cache()
def project_root() -> pathlib.Path:
    """Return repository root path."""
    return pathlib.Path(__file__).resolve().parent

def collect_metadata(base: pathlib.Path) -> dict:
    """Gather simple metadata for files under *base*.

    Respects optional environment variable ARCHIVER_IGNORE which should
    contain colon-separated folder names to skip.
    """
    meta = {"generated_at": datetime.datetime.utcnow().isoformat() + "Z", "files": []}
    ignore = set(filter(None, os.environ.get("ARCHIVER_IGNORE", "").split(":")))
    for path in base.rglob("*"):
        if any(part in ignore for part in path.parts):
            continue
        if path.is_file():
            meta["files"].append(str(path.relative_to(base)))
    return meta

def create_archive(output: pathlib.Path) -> None:
    base = project_root()
    metadata = collect_metadata(base)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in base.rglob("*"):
            if file_path.is_file():
                zf.write(file_path, file_path.relative_to(base))
        zf.writestr("metadata.json", json.dumps(metadata, indent=2))
    output.write_bytes(buffer.getvalue())

def main(argv: list[str]) -> None:
    out_file = pathlib.Path(argv[1]) if len(argv) > 1 else project_root() / "project.zip"
    if out_file.exists():
        backup = out_file.with_suffix(".bak.zip")
        shutil.move(out_file, backup)
    create_archive(out_file)
    with zipfile.ZipFile(out_file) as zf:
        meta = json.loads(zf.read("metadata.json"))
    message = textwrap.dedent(f"""\
        Archivo zip creado en: {out_file}
        Archivos incluidos: {len(meta['files'])}
    """)
    sys.stdout.write(message)

if __name__ == "__main__":
    main(sys.argv)
