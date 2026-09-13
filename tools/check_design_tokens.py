"""Measure declared opaque token pairings; no claims about whole-screen WCAG conformance."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def luminance(value):
    channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return sum(c * w for c, w in zip(linear, (0.2126, 0.7152, 0.0722)))


def ratio(first, second):
    bright, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (bright + 0.05) / (dark + 0.05)


def report():
    data = json.loads((ROOT / "docs/design/tokens.json").read_text(encoding="utf8"))
    results = []
    for theme, colors in data["themes"].items():
        pairs = [(fg, bg, 4.5) for bg in ("background", "surface", "surfaceTint")
                 for fg in ("textPrimary", "textSecondary", "textTertiary", "primary", "success", "warning", "error", "info")]
        pairs += [("onPrimary", "primary", 4.5), ("primary", "primarySoft", 4.5)]
        pairs += [(fg, bg, 3.0) for fg in ("focus", "controlBorder")
                  for bg in ("background", "surface", "surfaceTint")]
        for fg, bg, minimum in pairs:
            actual = ratio(colors[fg], colors[bg])
            results.append({"theme": theme, "foreground": fg, "background": bg,
                            "ratio": round(actual, 3), "minimum": minimum, "pass": actual >= minimum})
    return {"method": "WCAG relative luminance, opaque sRGB token pairs only", "checks": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = report()
    if args.write:
        (ROOT / "docs/design/contrast-evidence.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf8")
    failed = [item for item in result["checks"] if not item["pass"]]
    for failure in failed:
        print(failure)
    print(f"{len(result['checks']) - len(failed)}/{len(result['checks'])} declared contrast pairs passed")
    raise SystemExit(bool(failed))
