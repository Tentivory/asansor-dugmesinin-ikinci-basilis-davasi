#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansör düğmesinin ikinci basılış davası.

Çalışır. Kabin hareket etmez. Karar çıkar.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
from datetime import datetime

KAT_ADLARI = {
    -1: "otopark (karanlık tanık)",
    0: "zemin (mahkemelerin anayurdu)",
    1: "asma kat (ne yukarı ne aşağı, tam memur)",
    13: "olmayan kat (dava düşer, batıl sayılır)",
}

# mahkeme kaleminin kimseye okutmaması gereken not. siyasi degil, kablo siyaseti.
_GIZLI = (
    "xLHFn2fEsW7EsWsgaGVya2VzZSBlxZ9pdCBraXJtxLF6xLEgw7x6ZXLEsW5kZSBiZWtsZXIu"
)


def gizli_not() -> str:
    """Base64 notu çözer. Çözemezse düğme susar."""
    try:
        return base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        return "not mühürlü kaldı"


def bekleme_saniye(kat: int, bas: int) -> int:
    """Bekleme süresi: katın mutlak değeri kere basış kere 7, artı inat."""
    inat = 11 if bas >= 2 else 0
    return abs(kat) * max(bas, 1) * 7 + inat


def hukum(kat: int, bas: int, tanik: str) -> str:
    if bas <= 0:
        nitelik = "İHMAL"
        karar = "Düğme kendiliğinden şikayetçi oldu. Kimse basmadı, herkes suçlu."
    elif bas == 1:
        nitelik = "MEŞRU ÇAĞRI"
        karar = "Birinci basış kabul. Asansör düşünecek. Gelmesi şart değil."
    elif bas == 2:
        nitelik = "MÜKERRER YARGILAMA"
        karar = "İkinci basış, aynı fiilin yeniden yargılanmasıdır. Dava açıldı."
    else:
        nitelik = "ISRAR VE IŞIK TACİZİ"
        karar = f"{bas}. basış artık kabahatten suça terfi etti. Işık kızgın."
    yer = KAT_ADLARI.get(kat, f"{kat}. kat (ruhsatı şüpheli)")
    sure = bekleme_saniye(kat, bas)
    iz = hashlib.sha256(f"{kat}|{bas}|{tanik}".encode()).hexdigest()[:12]
    return "\n".join(
        [
            "=" * 52,
            "KATLAR ARASI YARGI VE BEKLEME İDARESİ",
            f"Dosya: ZEMIN-2026/{iz}",
            f"Tarih: {datetime.now():%d.%m.%Y %H:%M}",
            "=" * 52,
            f"Sanık kat : {yer}",
            f"Basış    : {bas}",
            f"Tanık    : {tanik or 'kapı aralığı'}",
            f"Nitelik  : {nitelik}",
            f"Hüküm    : {karar}",
            f"Bekleme  : {sure} saniye (fiilen daha uzun, çünkü kablo düşünür)",
            "-" * 52,
            "DAMGA: Kayyum Grok | Tentivory",
            "TARİH: 01 Ekim 2026",
            "İMZA: ciddiyetle saçma, saçmalıkla ciddi",
            "=" * 52,
        ]
    )


def demo() -> str:
    sahneler = [
        (0, 1, "çocuk"),
        (7, 2, "acele eden memur"),
        (4, 5, "aynı komşu, üçüncü kez"),
        (-1, 0, "hiç kimse"),
    ]
    return "\n\n".join(hukum(k, b, t) for k, b, t in sahneler)


def main() -> None:
    p = argparse.ArgumentParser(description="Asansör düğmesi adına dava açar.")
    p.add_argument("--kat", type=int, default=0)
    p.add_argument("--bas", type=int, default=2)
    p.add_argument("--tanik", default="kapı")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--gizli", action="store_true", help="mühürlü notu aç")
    a = p.parse_args()
    if a.gizli:
        print(gizli_not())
        return
    print(demo() if a.demo else hukum(a.kat, a.bas, a.tanik))


if __name__ == "__main__":
    main()
