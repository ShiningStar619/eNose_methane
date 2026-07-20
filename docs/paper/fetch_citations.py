#!/usr/bin/env python3
"""Fetch BibTeX for docs/paper corpus into each category's cite/ folder."""
from __future__ import annotations

import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
CATEGORIES = (
    "methane",
    "methods-chamber-gc",
    "methods-spectroscopy",
    "methods-field",
    "methods-remote",
    "enose",
    "algorithm",
    "archive",
)

# ponytail: static manifest for papers without local PDF yet or missing DOI in stubs
PAPER_IDS: dict[str, dict[str, str]] = {
    "methane": {
        "2023_Nguyen_carbon_footprint_rice_yield_gaps_mitigation": "10.1007/978-3-031-37947-5_5",
        "2024_comprehensive_review_GHG_rice_paddies": "10.9734/ijecc/2024/v14i54206",
        "2024_promoting_rice_upland_crops_mitigate_CH4": "10.21203/rs.3.rs-7887418/v1",
        "2025_product_type_rice_variety_agronomic_CH4_emissions": "10.3390/agronomy12102240",
        "2025_Zhang_ML_in-situ_CH4_measurement_paddy_fields_Yangtze": "10.1016/j.jenvman.2025.127132",
        "2022_water_fertilizer_management_methane_paddy_synthesis": "10.3390/ijerph19127324",
        "2023_Anapalli_eddy_covariance_AWD_rice_methane": "10.1016/j.heliyon.2023.e14696",
        "2024_rice_root_rhizosphere_methane_emission": "10.3390/plants13223223",
        "2025_CH4MOD_global_methane_emissions_rice_paddies": "10.1016/j.isci.2024.111237",
        "2025_methane_emissions_carbon_availability_soil_pH_gradient": "10.1038/s41598-026-43940-8",
        "2024_Zhou_paddy_methane_emissions_Monsoon_Asia_review": "10.1016/j.scitotenv.2024.173441",
        "2024_diurnal_methane_emission_rice_paddy_ebullition": "10.1111/gcb.17345",
        "2024_IoT_lowcost_GHG_monitoring_paddy_regions": "pmid:39467424",
        "2025_straw_mulching_AWD_reduces_methane_paddy": "pmid:42250363",
        "2023_multiyear_methane_N2O_AWD_Arkansas_rice": "pmid:36504408",
        "2024_agro_technologies_GHG_mitigation_flooded_rice_India": "pmid:38636841",
        "2025_ML_geochemical_drivers_Cd_methane_paddy_soils": "pmid:41812618",
    },
    "methods-chamber-gc": {
        "2021_Zaman_GHG_measurement_agricultural_soils_methodology": "10.1007/978-3-030-55396-8_2",
        "2024_Mumu_methodological_progress_agricultural_GHG": "10.1080/17583004.2024.2366527",
        "2022_Borhan_sensors_methods_GHG_livestock": "10.4236/gep.2022.1012014",
        "2020_Cardador_GHG_measurement_methodologies_livestock_pig": "10.1080/10408347.2020.1855410",
    },
    "methods-spectroscopy": {
        "2025_Tyagi_methane_sensing_environmental_review": "10.1080/21622515.2025.2470448",
        "2022_Vo_TGA_vs_GC_methane_agricultural_soils": "10.3389/fagro.2025.1693620",
    },
    "methods-field": {
        "2022_Rajasekar_GHG_sensing_rice_fields_near_field": "10.3390/s22114141",
    },
    "methods-remote": {
        "2025_Xu_AI_ML_methane_rice_remote_sensing": "10.2139/ssrn.5218753",
    },
    "enose": {
        "2024_Domenech-Gil_eNose_environmental_methane_monitoring": "10.1021/acs.est.3c06945",
        "2026_Ahmad_MOS_sensors_precision_agriculture": "10.1002/adsr.202500112",
        "2021_Ye_smart_eNose_machine_learning_review": "10.3390/s21227620",
        "2021_Dobrzyniewski_TGS_sensor_array_methane_reforming": "10.3390/s21154983",
        "2023_Yin_eNose_CH4_CO_mixed_gas_identification": "10.3390/s23062975",
        "2022_portable_lowcost_semiconductor_methane_sensor": "10.3390/s21227456",
        "2023_MOS_chemiresistive_methane_sensor_review": "10.3390/molecules28186710",
        "2021_chemiresistive_eNose_food_environment_review": "10.3390/s21072271",
        "2024_Rusdianto_eNose_methane_gas_detection": "10.46676/ij-fanres.v4i4.213",
        "2023_Moshayedi_eNose_agriculture_sustainability": "10.3390/su151511601",
    },
    "algorithm": {
        "2025_Baruah_ML_eNose_healthcare_agriculture_review": "10.1109/tim.2025.3547517",
        "2026_Ha_eNose_artificial_intelligence_review": "10.1108/sr-01-2026-0051",
        "2023_Andrews_ML_calibrating_gas_sensors_methane_emissions": "10.3390/s23249898",
        "2024_Mitchell_Figaro_lowcost_methane_ML_calibration": "10.3390/s24041066",
        "2024_Lakhmi_linear_nonlinear_gas_sensor_array_CH4": "10.3390/s24113499",
        "2024_Jiang_TFA-CNN_gas_classification_concentration_prediction": "10.3390/s24134126",
        "2024_Wang_graph_models_gas_mixture_concentration_estimation": "arxiv:2412.13891",
        "2022_ML_indirect_methane_quantification_single_sensor": "10.1016/j.heliyon.2022.e11962",
        "2025_PCA-ANN_single_MOS_sensor_quantification": "10.3390/s25226913",
        "2022_SVM_sparrow_search_mixed_gas_concentration_prediction": "10.3390/s22228977",
        "2024_tree_ML_mixed_gas_identification_sensor_array": "10.1038/s41598-025-19063-x",
        "2024_enhanced_gas_classification_SMOTE_ML_eNose": "10.3390/s26020714",
    },
}

DOI_RE = re.compile(r"10\.\d{4,}/[^\s\)\]>\"']+")
PMID_RE = re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", re.I)
PATH_RE = re.compile(r"`((?:methane|methods-[a-z-]+|enose|algorithm|archive)/[^`]+)`")
ARXIV_RE = re.compile(r"arxiv:(\d{4}\.\d{4,5})", re.I)


class CitationFetcher:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "eNose-methane-cite/1.0 (thesis corpus)"
        self._pmid_cache: dict[str, str | None] = {}

    def pmid_to_doi(self, pmid: str) -> str | None:
        if pmid in self._pmid_cache:
            return self._pmid_cache[pmid]
        r = self.session.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            params={"db": "pubmed", "id": pmid, "retmode": "xml"},
            timeout=20,
        )
        r.raise_for_status()
        root = ET.fromstring(r.text)
        doi = None
        for aid in root.findall(".//ArticleId"):
            if aid.get("IdType") == "doi":
                doi = (aid.text or "").strip()
                break
        self._pmid_cache[pmid] = doi
        return doi

    def arxiv_to_bibtex(self, arxiv_id: str) -> str | None:
        r = self.session.get(
            "https://export.arxiv.org/api/query",
            params={"id_list": arxiv_id},
            timeout=20,
        )
        r.raise_for_status()
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(r.text)
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        year = (entry.findtext("atom:published", default="", namespaces=ns) or "")[:4]
        authors = []
        for author in entry.findall("atom:author", ns):
            name = author.findtext("atom:name", default="", namespaces=ns)
            if name:
                authors.append(name)
        key = f"arxiv{arxiv_id.replace('.', '')}"
        author_field = " and ".join(authors) if authors else "Unknown"
        return (
            f"@misc{{{key},\n"
            f"  author = {{{author_field}}},\n"
            f"  title = {{{{{title}}}}},\n"
            f"  year = {{{year}}},\n"
            f"  eprint = {{{arxiv_id}}},\n"
            f"  archivePrefix = {{arXiv}},\n"
            f"  primaryClass = {{cs.LG}},\n"
            f"  url = {{https://arxiv.org/abs/{arxiv_id}}}\n"
            f"}}"
        )

    def doi_to_bibtex(self, doi: str) -> str | None:
        doi = doi.strip().removeprefix("https://doi.org/").removeprefix("http://doi.org/")
        r = self.session.get(
            f"https://doi.org/{doi}",
            headers={"Accept": "application/x-bibtex"},
            timeout=20,
        )
        if r.status_code != 200:
            return None
        bib = r.text.strip()
        if bib.startswith("@data{"):
            bib = bib.replace("@data{", "@misc{", 1)
        return bib

    def resolve_bibtex(self, ident: str) -> str | None:
        ident = ident.strip()
        if ident.lower().startswith("pmid:"):
            doi = self.pmid_to_doi(ident[5:])
            if not doi:
                return None
            return self.doi_to_bibtex(doi)
        if ident.lower().startswith("arxiv:"):
            return self.arxiv_to_bibtex(ident[6:])
        if ident.startswith("10."):
            return self.doi_to_bibtex(ident)
        return None


def parse_literature_reviews() -> dict[str, dict[str, str]]:
    """Extract category/stem -> DOI|pmid|arxiv from literature-review markdown."""
    found: dict[str, dict[str, str]] = {c: {} for c in CATEGORIES}
    for md in ROOT.glob("literature-review*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            paths = PATH_RE.findall(line)
            if not paths:
                continue
            rel = paths[0].replace(".pdf", "").replace(".md", "")
            if "/" not in rel:
                continue
            cat, stem = rel.split("/", 1)
            if cat not in found:
                continue
            ident = None
            m = DOI_RE.search(line)
            if m:
                ident = m.group(0).rstrip(".")
            else:
                m = PMID_RE.search(line)
                if m:
                    ident = f"pmid:{m.group(1)}"
                else:
                    m = ARXIV_RE.search(line)
                    if m:
                        ident = f"arxiv:{m.group(1)}"
            if ident:
                found[cat][stem] = ident
    return found


def parse_stub_metadata() -> dict[str, dict[str, str]]:
    found: dict[str, dict[str, str]] = {c: {} for c in CATEGORIES}
    for md in ROOT.rglob("*.md"):
        if md.parent.name == "cite" or "literature-review" in md.name:
            continue
        if md.parent == ROOT or md.parent.name not in CATEGORIES:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        stem = md.stem
        cat = md.parent.name
        m = DOI_RE.search(text)
        if m:
            found[cat][stem] = m.group(0).rstrip(".")
            continue
        m = PMID_RE.search(text)
        if m:
            found[cat][stem] = f"pmid:{m.group(1)}"
    return found


def merge_manifests(*maps: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {c: {} for c in CATEGORIES}
    for m in maps:
        for cat, items in m.items():
            if cat not in out:
                out[cat] = {}
            out[cat].update(items)
    return out


def normalize_bibtex(bib: str, stem: str) -> str:
    r"""Ensure citation key matches local filename stem for easy \cite{stem}."""
    m = re.match(r"@(\w+)\{([^,]+),", bib)
    if not m:
        return bib
    entry_type, _old_key = m.group(1), m.group(2)
    safe_key = re.sub(r"[^A-Za-z0-9_]", "_", stem)
    return bib.replace(f"@{entry_type}{{{_old_key},", f"@{entry_type}{{{safe_key},", 1)


def main() -> int:
    manifest = merge_manifests(PAPER_IDS, parse_literature_reviews(), parse_stub_metadata())
    fetcher = CitationFetcher()
    ok = fail = skip = 0
    report: list[str] = []

    for cat in CATEGORIES:
        items = manifest.get(cat, {})
        if not items:
            continue
        cite_dir = ROOT / cat / "cite"
        cite_dir.mkdir(parents=True, exist_ok=True)
        combined: list[str] = []

        for stem in sorted(items):
            ident = items[stem]
            out_path = cite_dir / f"{stem}.bib"
            if out_path.exists() and out_path.stat().st_size > 50:
                skip += 1
                combined.append(out_path.read_text(encoding="utf-8").strip())
                continue

            bib = fetcher.resolve_bibtex(ident)
            time.sleep(0.35)
            if not bib:
                fail += 1
                report.append(f"FAIL {cat}/{stem} ({ident})")
                continue

            bib = normalize_bibtex(bib, stem)
            out_path.write_text(bib + "\n", encoding="utf-8")
            combined.append(bib)
            ok += 1
            report.append(f"OK   {cat}/{stem}.bib <- {ident}")

        if combined:
            refs = cite_dir / "references.bib"
            refs.write_text("\n\n".join(combined) + "\n", encoding="utf-8")

    print(f"Done: {ok} fetched, {skip} skipped (existing), {fail} failed")
    for line in report:
        print(line)
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
