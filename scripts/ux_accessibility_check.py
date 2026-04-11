#!/usr/bin/env python3
"""
Статическая проверка UX/доступности для Tkinter-проекта KitchenMate.
Имитирует идею WCAG/HTML-проверок: подписи к полям, текст на кнопках, контраст базовых цветов.
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path


def relative_luminance(hex_color: str) -> float:
    """WCAG 2.x relative luminance для sRGB hex #RRGGBB."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    R, G, B = lin(r), lin(g), lin(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


def contrast_ratio(fg: str, bg: str) -> float:
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    light, dark = max(l1, l2), min(l1, l2)
    return (light + 0.05) / (dark + 0.05)


def scan_login_labels(screens_dir: Path) -> list[str]:
    """Проверка: у экрана входа есть текстовые метки «Логин» и «Пароль»."""
    issues: list[str] = []
    text = (screens_dir / "login_screen.py").read_text(encoding="utf-8")
    if 'text="Логин:"' not in text and "text='Логин:'" not in text:
        issues.append("login_screen: не найдена метка Логин")
    if 'text="Пароль:"' not in text and "text='Пароль:'" not in text:
        issues.append("login_screen: не найдена метка Пароль")
    if "bind(\"<Return>\"" not in text and "bind('<Return>'" not in text:
        issues.append("login_screen: нет привязки Enter для отправки формы")
    return issues


def scan_icon_only_buttons(screens_dir: Path) -> list[str]:
    """Эвристика: кнопки только с эмодзи без буквенного описания."""
    issues: list[str] = []
    btn_re = re.compile(r"Button\([^)]*text\s*=\s*['\"]([^'\"]+)['\"]")
    for path in sorted(screens_dir.glob("*.py")):
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            m = btn_re.search(line)
            if not m:
                continue
            txt = m.group(1).strip()
            if txt and not any(c.isalpha() for c in txt) and len(txt) <= 3:
                issues.append(f"{path.name}:{i}: кнопка без букв в подписи: {txt!r}")
    return issues


def scan_config_contrast(config_path: Path) -> list[str]:
    """Базовый контраст зелёного/красного текста на белом (AA для крупного текста ≥ 3:1)."""
    issues: list[str] = []
    text = config_path.read_text(encoding="utf-8")
    colors: dict[str, str] = {}
    for name in ("GREEN", "RED", "GRAY"):
        m = re.search(rf"^{name}\s*=\s*[\"'](#[0-9A-Fa-f]{{6}})[\"']", text, re.MULTILINE)
        if m:
            colors[name] = m.group(1)
    bg = "#FFFFFF"
    for name, hx in colors.items():
        cr = contrast_ratio(hx, bg)
        if cr < 3.0:
            issues.append(f"config: {name} {hx} на белом: контраст {cr:.2f}:1 (< 3:1 для крупного UI-текста)")
    return issues


def scan_ui_helpers_exists(code_dir: Path) -> list[str]:
    issues: list[str] = []
    path = code_dir / "ui_helpers.py"
    if not path.exists():
        issues.append("Отсутствует code/ui_helpers.py (кастомные диалоги)")
        return issues
    t = path.read_text(encoding="utf-8")
    if "confirm_destructive" not in t:
        issues.append("ui_helpers: нет confirm_destructive")
    return issues


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    screens = root / "code" / "screens"
    config = root / "code" / "config.py"
    code = root / "code"

    all_issues: list[str] = []
    all_issues.extend(scan_ui_helpers_exists(code))
    all_issues.extend(scan_login_labels(screens))
    all_issues.extend(scan_icon_only_buttons(screens))
    all_issues.extend(scan_config_contrast(config))

    print("KitchenMate — UX / accessibility static check")
    print("=" * 50)
    if not all_issues:
        print("Status: PASS")
        print("Замечаний по выбранным правилам не найдено.")
        return 0

    print("Status: FAIL")
    for x in all_issues:
        print(f"  - {x}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
