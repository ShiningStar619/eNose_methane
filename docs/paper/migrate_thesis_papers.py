#!/usr/bin/env python3
"""One-shot: move thesis papers into docs/paper with canonical names."""
from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

THESIS = Path(r"G:\Other computers\My Computer\E\year 6\thesis\paper")
ROOT = Path(__file__).resolve().parent

# (source relative to THESIS, target category, target filename)
MOVES: list[tuple[str, str, str]] = [
    # methane in rice field
    (
        r"methane in rice field\product-type-rice-variety-and-agronomic-measures-determined-13o58hmn.pdf",
        "methane",
        "2025_product_type_rice_variety_agronomic_CH4_emissions.pdf",
    ),
    (
        r"methane in rice field\a-comprehensive-review-on-greenhouse-gas-emissions-in-27c96przp7.pdf",
        "methane",
        "2024_comprehensive_review_GHG_rice_paddies.pdf",
    ),
    (
        r"methane in rice field\carbon-footprint-research-and-mitigation-strategies-for-rice-37sa4vmwmk.pdf",
        "methane",
        "2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation.pdf",
    ),
    (
        r"methane in rice field\promoting-rice-upland-crops-systems-to-mitigate-direct-s47a0zmjq7po.pdf",
        "methane",
        "2024_promoting_rice_upland_crops_mitigate_CH4.pdf",
    ),
    (
        r"methane in rice field\sustainability-16-04789-v2.pdf",
        "methane",
        "2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze.pdf",
    ),
    # methods-chamber-gc
    (
        r"method to detect climate change gas\1-chamber-GC-flux-methods\methodology-for-measuring-greenhouse-gas-emissions-from-prs0q2oh0r.pdf",
        "methods-chamber-gc",
        "2021_Zaman_GHG_measurement_agricultural_soils_methodology.pdf",
    ),
    (
        r"method to detect climate change gas\1-chamber-GC-flux-methods\Methodological progress in the measurement of agricultural greenhouse gases.pdf",
        "methods-chamber-gc",
        "2024_Mumu_methodological_progress_agricultural_GHG.pdf",
    ),
    (
        r"method to detect climate change gas\1-chamber-GC-flux-methods\Sensors_and_Methods_for_Measuring_Greenh.pdf",
        "methods-chamber-gc",
        "2022_Borhan_sensors_methods_GHG_livestock.pdf",
    ),
    (
        r"method to detect climate change gas\1-chamber-GC-flux-methods\Review of the Methodologies for Measurement of Greenhouse Gas Emissions in Livestock Farming  Pig Farms as a Case of Study.pdf",
        "methods-chamber-gc",
        "2020_Cardador_GHG_measurement_methodologies_livestock_pig.pdf",
    ),
    # methods-spectroscopy
    (
        r"method to detect climate change gas\2-spectroscopy-TDLAS-TGA-FTIR\Environmental impacts and recent advancements in the sensing of methane  a review.pdf",
        "methods-spectroscopy",
        "2025_Tyagi_methane_sensing_environmental_review.pdf",
    ),
    (
        r"method to detect climate change gas\2-spectroscopy-TDLAS-TGA-FTIR\fagro-7-1693620.pdf",
        "methods-spectroscopy",
        "2022_Vo_TGA_vs_GC_methane_agricultural_soils.pdf",
    ),
    # methods-field (Rajasekar duplicate of enose/ — skip if same hash)
    (
        r"method to detect climate change gas\3-auto-chamber-field-sensors\sensing-and-analysis-of-greenhouse-gas-emissions-from-rice-5p5fl6u4.pdf",
        "methods-field",
        "2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf",
    ),
    # enose + algorithm (thesis 4-enose-MOS-ML)
    (
        r"method to detect climate change gas\4-enose-MOS-ML\Advanced Sensor Research - 2026 - Ahmad - The Promise of Low?Cost Metal?Oxide Semiconductor Gas Sensors for Precision.pdf",
        "enose",
        "2026_Ahmad_MOS_sensors_precision_agriculture.pdf",
    ),
    (
        r"method to detect climate change gas\4-enose-MOS-ML\A_Review_on_Application_of_Machine_Learning_Techniques_Coupled_With_E-Nose_in_Healthcare_Agriculture_and_Allied_Domains.pdf",
        "algorithm",
        "2025_Baruah_ML_eNose_healthcare_agriculture_review.pdf",
    ),
    (
        r"method to detect climate change gas\4-enose-MOS-ML\ea61683a178c1126862b6b7d9bc925a233f7.pdf",
        "enose",
        "2024_Rusdianto_eNose_methane_gas_detection.pdf",
    ),
    (
        r"method to detect climate change gas\4-enose-MOS-ML\sr-01-2026-0051en.pdf",
        "algorithm",
        "2026_Ha_eNose_artificial_intelligence_review.pdf",
    ),
    (
        r"method to detect climate change gas\4-enose-MOS-ML\sustainability-15-11601.pdf",
        "enose",
        "2023_Moshayedi_eNose_agriculture_sustainability.pdf",
    ),
    # methods-remote
    (
        r"method to detect climate change gas\5-remote-sensing-AI-modeling\ssrn-5218753.pdf",
        "methods-remote",
        "2025_Xu_AI_ML_methane_rice_remote_sensing.pdf",
    ),
    # archive — peripheral eNose (food / plant VOC, not CH4 rice)
    (
        r"method to detect climate change gas\_misc-related\fpls-15-1323296.pdf",
        "archive",
        "2024_Herrmann_eNose_soybean_water_stress.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\1-s2.0-S0022474X25002991-main.pdf",
        "archive",
        "2025_eNose_peripheral_S0022474X25002991.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\Development_of_an_Integrated_Soft_E-Nose_for_Food_Quality_Assessment.pdf",
        "archive",
        "2024_soft_eNose_food_quality_assessment.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\agriculture-12-01359 (1).pdf",
        "archive",
        "2022_eNose_agriculture_peripheral.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\1-s2.0-S2772375524001631-main.pdf",
        "archive",
        "2024_eNose_peripheral_S2772375524001631.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\s11694-024-02980-2.pdf",
        "archive",
        "2024_eNose_peripheral_s11694.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\Comp Rev Food Sci Food Safe - 2023 - Ali - Electronic nose as a tool for early detection of diseases and quality monitoring.pdf",
        "archive",
        "2023_Ali_eNose_food_disease_quality_review.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\d3ay01192e.pdf",
        "archive",
        "2023_Ferreira_lowcost_eNose_plantation_fruit_crops.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\J Sci Food Agric - 2023 - Bianchi - Assessment of fruity aroma intensity in olive oils from different Spanish regions using.pdf",
        "archive",
        "2023_Bianchi_eNose_olive_oil_aroma.pdf",
    ),
    (
        r"method to detect climate change gas\eNose\horticulturae-08-00386-v4.pdf",
        "archive",
        "2022_eNose_horticulturae_peripheral.pdf",
    ),
]

# Duplicates: thesis copy removed if identical to existing enose file
DEDUP_SKIP = [
    (
        r"method to detect climate change gas\4-enose-MOS-ML\electronic-nose-for-improved-environmental-methane-monitoring (1).pdf",
        "enose/2024_Domenech-Gil_eNose_environmental_methane_monitoring.pdf",
    ),
]


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


# Existing files to relocate into new category folders
REORGANIZE: list[tuple[str, str]] = [
    (
        "enose/2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf",
        "methods-field/2022_Rajasekar_GHG_sensing_rice_fields_near_field.pdf",
    ),
]


def main() -> int:
    if not THESIS.is_dir():
        print(f"THESIS folder not found: {THESIS}")
        return 1

    moved = skipped = deduped = missing = reorganized = 0

    for src_rel, dest_rel in REORGANIZE:
        src = ROOT / src_rel
        dest = ROOT / dest_rel
        if not src.is_file():
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            print(f"REORG skip (dest exists): {dest_rel}")
            continue
        shutil.move(str(src), str(dest))
        print(f"REORG {src_rel} -> {dest_rel}")
        reorganized += 1

    for rel, existing_rel in DEDUP_SKIP:
        src = THESIS / rel
        existing = ROOT / existing_rel
        if not src.is_file():
            print(f"MISS {rel}")
            missing += 1
            continue
        if existing.is_file() and file_hash(src) == file_hash(existing):
            src.unlink()
            print(f"DEDUP removed thesis duplicate: {src.name}")
            deduped += 1
        elif existing.is_file():
            print(f"WARN duplicate name differs — kept both: {existing_rel}")
            skipped += 1
        else:
            print(f"WARN existing missing for dedup: {existing_rel}")

    for rel, cat, name in MOVES:
        src = THESIS / rel
        dest_dir = ROOT / cat
        dest = dest_dir / name
        dest_dir.mkdir(parents=True, exist_ok=True)

        if not src.is_file():
            print(f"MISS {rel}")
            missing += 1
            continue

        if dest.exists():
            if file_hash(src) == file_hash(dest):
                src.unlink()
                print(f"DEDUP {cat}/{name}")
                deduped += 1
            else:
                print(f"SKIP exists (different): {cat}/{name}")
                skipped += 1
            continue

        # Zhang PDF replaces stub
        stub = dest.with_suffix(".md")
        if stub.exists():
            stub.unlink()
            print(f"  removed stub {stub.name}")

        shutil.move(str(src), str(dest))
        print(f"MOVE -> {cat}/{name}")
        moved += 1

    # Move README-categories into docs/paper as reference
    readme_src = THESIS / r"method to detect climate change gas\README-categories.md"
    if readme_src.is_file():
        readme_dest = ROOT / "archive" / "thesis-README-categories.md"
        readme_dest.parent.mkdir(parents=True, exist_ok=True)
        if not readme_dest.exists():
            shutil.move(str(readme_src), str(readme_dest))

    print(
        f"\nDone: {moved} moved, {reorganized} reorganized, "
        f"{deduped} deduped, {skipped} skipped, {missing} missing"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
