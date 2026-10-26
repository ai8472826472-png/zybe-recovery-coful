#!/usr/bin/env python3
"""Repack a header-v2 boot image so it fits the Moto G31 32 MiB boot partition.

- keeps kernel, dtb, cmdline, offsets, os version/patch exactly
- ramdisk stays gzip (the stock kernel only has CONFIG_RD_GZIP)
- if too big: drops the AOSP stock-recovery text bitmaps (res/images/*_text.png),
  which TWRP/OrangeFox do not draw, then recompresses with zopfli (or gzip -9)
- adds an unsigned AVB hash footer for a 32 MiB 'boot' partition when avbtool is present
Usage: fit_boot.py IN.img OUT.img --src ANDROID_SRC [--limit 33554432]
"""
import argparse, gzip, os, re, shutil, struct, subprocess, sys, tempfile

def read_cpio(data):
    out = []; i = 0
    while i < len(data):
        h = data[i:i+110]
        if h[:6] not in (b"070701", b"070702"): break
        f = [int(h[6+8*k:14+8*k], 16) for k in range(13)]
        nsize, fsize = f[11], f[6]
        name = data[i+110:i+110+nsize-1]
        j = (i + 110 + nsize + 3) & ~3
        out.append((h, name, data[j:j+fsize]))
        i = (j + fsize + 3) & ~3
        if name == b"TRAILER!!!": break
    return out

def write_cpio(entries):
    b = bytearray()
    for h, name, body in entries:
        nsize = len(name) + 1
        hh = bytearray(h)
        hh[6+8*6:14+8*6] = b"%08X" % len(body)
        hh[6+8*11:14+8*11] = b"%08X" % nsize
        b += hh + name + b"\0"
        while len(b) % 4: b += b"\0"
        b += body
        while len(b) % 4: b += b"\0"
    return bytes(b)

def gz(data, tmp):
    raw = os.path.join(tmp, "rd.cpio"); open(raw, "wb").write(data)
    if shutil.which("zopfli"):
        subprocess.run(["zopfli", "--gzip", "--i5", "-c", raw], check=True, stdout=open(raw + ".gz", "wb"))
        return open(raw + ".gz", "rb").read()
    return gzip.compress(data, 9)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--src", required=True); ap.add_argument("--limit", type=int, default=33554432)
    a = ap.parse_args()
    mk = os.path.join(a.src, "system/tools/mkbootimg")
    tmp = tempfile.mkdtemp()
    r = subprocess.run([sys.executable, os.path.join(mk, "unpack_bootimg.py"), "--boot_img", a.inp,
                        "--out", tmp + "/u", "--format", "mkbootimg"], capture_output=True, text=True, check=True)
    args = r.stdout.strip()
    print("mkbootimg args:", args)
    rd = open(tmp + "/u/ramdisk", "rb").read()
    if rd[:2] != b"\x1f\x8b": sys.exit("ramdisk is not gzip: the stock kernel cannot unpack it (CONFIG_RD_GZIP only)")
    cp = gzip.decompress(rd)
    ents = read_cpio(cp)
    k = os.path.getsize(tmp + "/u/kernel"); d = os.path.getsize(tmp + "/u/dtb") if os.path.exists(tmp + "/u/dtb") else 0
    budget = a.limit - k - d - 2048*8 - 1024*1024  # header/pages/padding + 1 MiB for the AVB footer
    print(f"kernel {k}  dtb {d}  ramdisk(gz) {len(rd)}  budget for ramdisk {budget}")
    new_rd = rd
    if len(rd) > budget:
        drop = [e for e in ents if re.match(rb"^res/images/.*_text\.png$", e[1])]
        print("dropping", len(drop), "stock-recovery text bitmaps,", sum(len(e[2]) for e in drop), "bytes")
        ents = [e for e in ents if e not in drop]
        new_rd = gz(write_cpio(ents), tmp)
        print("ramdisk(gz) after trim+recompress:", len(new_rd))
    elif shutil.which("zopfli"):
        new_rd = gz(cp, tmp); print("ramdisk(gz) recompressed:", len(new_rd))
        if len(new_rd) > len(rd): new_rd = rd
    open(tmp + "/rd.gz", "wb").write(new_rd)
    import shlex
    toks = shlex.split(args)
    for i, t in enumerate(toks):
        if t == "--ramdisk": toks[i+1] = tmp + "/rd.gz"
    subprocess.run([sys.executable, os.path.join(mk, "mkbootimg.py")] + toks + ["--output", a.out], check=True)
    size = os.path.getsize(a.out)
    print("repacked size", size, "limit", a.limit)
    if size > a.limit:
        sys.exit(f"STILL TOO BIG: {size} > {a.limit} bytes (over by {size - a.limit})")
    avb = os.path.join(a.src, "external/avb/avbtool.py")
    if os.path.exists(avb):
        rr = subprocess.run([sys.executable, avb, "add_hash_footer", "--image", a.out, "--partition_size", str(a.limit),
                             "--partition_name", "boot"], capture_output=True, text=True)
        print("avb footer:", "ok" if rr.returncode == 0 else ("skipped: " + rr.stderr[-300:]))
    print("final size", os.path.getsize(a.out))

if __name__ == "__main__":
    main()
