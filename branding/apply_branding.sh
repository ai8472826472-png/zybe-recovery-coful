#!/bin/bash
# Zybe Recovery branding for OrangeFox fox_12.1. Never fails the build:
# any problem restores the stock theme and exits 0.
SRC="$1"; HERE="$(cd "$(dirname "$0")" && pwd)"
REC="$SRC/bootable/recovery"; T="$REC/gui/theme"
[ -d "$T" ] || { echo "branding: theme dir missing, skipped"; exit 0; }
restore() { echo "branding: problem ($1), restoring stock theme"; (cd "$REC" && git checkout -- gui/theme) || true; exit 0; }

# 1) name
for f in "$T/common/languages/en.xml" "$T/common/languages/hi_IN.xml"; do
  [ -f "$f" ] && sed -i -e 's/OrangeFox Recovery/Zybe Recovery/g' -e 's/OrangeFox/Zybe Recovery/g' "$f"
done
for f in "$T/portrait_hdpi/splash.xml" "$T/portrait_hdpi/themes/sed/splash.xml"; do
  [ -f "$f" ] && sed -i 's#<text>OrangeFox</text>#<text>Zybe</text>#g' "$f"
done
# 2) blue accent instead of orange (theme xml + any C++ default with the same literal)
grep -rIl -i -e 'ed6f02' -e 'D86100' "$REC" --include=*.xml --include=*.cpp --include=*.h --include=*.hpp 2>/dev/null | while read -r f; do
  echo "branding: accent in $f"; sed -i -e 's/#ed6f02/#2F80FF/Ig' -e 's/#D86100/#1E63D6/Ig' "$f"
done
# 3) logo (blue ring + white Z)
for l in logo_o logo_w logo_d; do
  [ -f "$T/portrait_hdpi/images/SVG/Logos/$l.svg" ] && cp "$HERE/logo_z.svg" "$T/portrait_hdpi/images/SVG/Logos/$l.svg"
done
# validate the real (non-template) xml files we touched
for f in "$T/common/languages/en.xml" "$T/common/languages/hi_IN.xml" "$T/portrait_hdpi/splash.xml" "$T/portrait_hdpi/themes/accent.xml" "$T/portrait_hdpi/images/SVG/Logos/logo_o.svg"; do
  [ -f "$f" ] || continue
  xmllint --noout "$f" || restore "$f is not valid xml"
done
(cd "$REC" && git --no-pager diff --stat -- gui/theme) || true
echo "branding: applied"
exit 0
