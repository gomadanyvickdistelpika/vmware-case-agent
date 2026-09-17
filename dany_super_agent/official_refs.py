"""Narrow, explainable official-reference candidates; never claims automatic applicability."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OfficialReference:
    title: str
    url: str
    match_reason: str


RULES = (
    (("unsupported hardware", "compatibility guide"), OfficialReference(
        "KB 381824: Checking Host Compatibility Before Upgrade Using the Broadcom Compatibility Guide",
        "https://knowledge.broadcom.com/external/article/381824/checking-vmware-esxi-host-compatibility.html",
        "The prompt explicitly concerns host support/upgrade compatibility.",
    )),
    (("custom vib", "missing dependencies"), OfficialReference(
        "KB 412258: ESXi remediation from 7.x to 8.x fails with software or system configuration incompatible",
        "https://knowledge.broadcom.com/external/article/412258/esxi-remediation-fails-from-7x-to-8x-fai.html",
        "The prompt reports vendor VIB dependency failure while applying a standard image.",
    )),
    (("patching_backup_config.json", "checksum mismatch"), OfficialReference(
        "KB 399833: Error [Errno 2] patching_backup_config.json - vCenter Server Appliance",
        "https://knowledge.broadcom.com/external/article/399833/vcenter-server-update-fails-with-error-i.html",
        "The exact missing staging file and checksum mismatch are both present.",
    )),
    (("cpu incompatibility", "evc"), OfficialReference(
        "KB 390403: vMotion failed due to EVC settings",
        "https://knowledge.broadcom.com/external/article/390403",
        "The prompt contains the documented vMotion CPU/EVC symptom.",
    )),
)


def match_official_references(text: str) -> list[OfficialReference]:
    lowered = text.lower()
    return [reference for terms, reference in RULES if all(term in lowered for term in terms)]

