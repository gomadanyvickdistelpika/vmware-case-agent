# Dany Super Agent — Ten Recent Public Compute Issue Demonstrations

Generated from ten actual local `VMware Case Agent` runs. Forum/community links identify recent symptom themes only; every prompt below is synthetic and redacted. Official links are independently treated as applicability candidates, never as proof of root cause. No private content or external action was used.

## 1. Live patch shown as unavailable after image selection

**Synthetic prompt:** A synthetic image-managed cluster was moved to ESXi 8.0 U3k. Enforce Live Patch was enabled after selecting the target image, but remediation still appears reboot-based and compliance has not been checked again.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line n/a: No recognized VMware component or explicit error pattern was found.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Re-run compliance after confirming live-patch eligibility and target-image metadata; pilot one host, then observe.
- **Pre-checks:** Capture current image, compliance result, TPM/Secure Boot and live-patch eligibility.
- **Impact/risk and approval gate:** Compliance checks are READ-ONLY; remediation can evacuate/reboot a host and requires approval.
- **Rollback/recovery:** Stop before remediation; restore the prior desired image only through an approved change plan.

### KB correctness assessment

**PASS — the agent correctly withheld a specific KB because the supplied evidence was insufficient for a verified resolution match.**

- No specific Broadcom KB was verified from the supplied evidence. Collect the missing evidence and search current official documentation by exact error/build before selecting a resolution.

### Sources

- [Public symptom-theme discussion](https://www.reddit.com/r/vmware/comments/1vcbeto/80u3k_live_patch_not_compatible/)
- [vSphere ESXi 8.0 U3k release notes](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/release-notes/esxi-update-and-patch-release-notes/vsphere-esxi-80u3k-release-notes.html)

## 2. VM networking fails after ESXi patch

**Synthetic prompt:** After a synthetic ESXi 8.0 U3k patch, guest traffic on one standard switch stops while management traffic on separate uplinks remains reachable. A rollback did not immediately restore guest networking. Exact NIC model, driver, firmware, and switch configuration are unknown.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line n/a: No recognized VMware component or explicit error pattern was found.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Preserve management access, compare switch/uplink state, logs and NIC driver/firmware against the compatibility guide; reproduce only in a maintenance window.
- **Pre-checks:** Export host networking, collect vmkernel/vobd logs, physical-switch counters, NIC IDs and firmware.
- **Impact/risk and approval gate:** Inspection is READ-ONLY; switch edits, driver changes, rollback or reboot are RISKY and approval-gated.
- **Rollback/recovery:** Keep console access and host-config backup; use a validated prior image and documented network restore.

### KB correctness assessment

**PASS — the agent correctly withheld a specific KB because the supplied evidence was insufficient for a verified resolution match.**

- No specific Broadcom KB was verified from the supplied evidence. Collect the missing evidence and search current official documentation by exact error/build before selecting a resolution.

### Sources

- [Public symptom-theme discussion](https://www.reddit.com/r/vmware/comments/1vebh2e/vsphere_80_update_2f_has_just_been_released/)
- [KB 389898: Checking ESXi Host I/O Device Compatibility Before Upgrade](https://knowledge.broadcom.com/external/article/389898/checking-esxi-host-io-device-compatibili.html)

## 3. Upgrade planned on unsupported server model

**Synthetic prompt:** A lab plans an ESXi 8 upgrade on unsupported hardware. A similar server model is listed, but the exact system is absent from the compatibility guide. NIC, storage controller, BIOS, and firmware support are unverified.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line n/a: No recognized VMware component or explicit error pattern was found.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Inventory exact system/I/O identifiers and verify every component for ESXi 8; replace unsupported components or retain a supported release.
- **Pre-checks:** Record server model, CPU, BIOS, NIC/HBA IDs, firmware, boot/storage devices and vendor guidance.
- **Impact/risk and approval gate:** Inventory is READ-ONLY; installing on unsupported hardware risks boot, network/storage loss and is RISKY.
- **Rollback/recovery:** Do not upgrade production; preserve boot media/config and maintain a tested return to the supported version.

### KB correctness assessment

**PASS — the agent identified a verified, symptom-matched official KB candidate.**

- [KB 381824: Checking Host Compatibility Before Upgrade Using the Broadcom Compatibility Guide](https://knowledge.broadcom.com/external/article/381824/checking-vmware-esxi-host-compatibility.html) — candidate because: The prompt explicitly concerns host support/upgrade compatibility. Confirm exact build, topology, prerequisites, and article update date before use.

### Sources

- [Public symptom-theme discussion](https://www.reddit.com/r/vmware/comments/1u94z5z/hardware_compability_esxi_8/)
- [KB 381824: Checking Host Compatibility Before Upgrade Using the Broadcom Compatibility Guide](https://knowledge.broadcom.com/external/article/381824/checking-vmware-esxi-host-compatibility.html)

## 4. Secure Boot certificate transition patch planning

**Synthetic prompt:** An image-managed vSphere 8 environment needs to plan the UEFI Secure Boot certificate transition. Hosts use Secure Boot, but firmware vendor readiness, signing certificate state, recovery access, and target release applicability are not yet inventoried.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line n/a: No recognized VMware component or explicit error pattern was found.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Inventory certificate and firmware readiness, read the exact U3j notes, test on representative hardware, then schedule phased remediation.
- **Pre-checks:** Confirm builds, Secure Boot state, firmware/OEM support, recovery console and backups.
- **Impact/risk and approval gate:** Inventory is READ-ONLY; firmware, certificate and host remediation are RISKY and require approval.
- **Rollback/recovery:** Retain recovery media, console access, current image and vendor-supported firmware rollback guidance.

### KB correctness assessment

**PASS — the agent correctly withheld a specific KB because the supplied evidence was insufficient for a verified resolution match.**

- No specific Broadcom KB was verified from the supplied evidence. Collect the missing evidence and search current official documentation by exact error/build before selecting a resolution.

### Sources

- [Public symptom-theme discussion](https://www.reddit.com/r/vmware/comments/1toywl5/vcenter_80_u3j_and_vsphere_80_u3j_arrived_secure/)
- [vSphere ESXi 8.0 U3j release notes](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/release-notes/esxi-update-and-patch-release-notes/vsphere-esxi-80u3j-release-notes.html)

## 5. Standard image conflicts with vendor VIBs

**Synthetic prompt:** vLCM remediation to ESXi 8 reports software or system configuration incompatible. The source host used a vendor custom image; scan details show custom VIB missing dependencies in the standard target image.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line 1: vLCM remediation to ESXi 8 reports software or system configuration incompatible. The source host used a vendor custom image; scan details show custom VIB missing dependencies in the standard target image.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Compare source VIBs with a current vendor image/add-on, build a compatible desired image, check compliance, then pilot remediation.
- **Pre-checks:** Export software profile/VIB list; validate hardware, firmware, vendor add-on and dependencies.
- **Impact/risk and approval gate:** Scan is READ-ONLY; VIB removal or host remediation is DISRUPTIVE and approval-gated.
- **Rollback/recovery:** Keep the prior bootbank/image and host configuration; validate workload evacuation and recovery.

### KB correctness assessment

**PASS — the agent identified a verified, symptom-matched official KB candidate.**

- [KB 412258: ESXi remediation from 7.x to 8.x fails with software or system configuration incompatible](https://knowledge.broadcom.com/external/article/412258/esxi-remediation-fails-from-7x-to-8x-fai.html) — candidate because: The prompt reports vendor VIB dependency failure while applying a standard image. Confirm exact build, topology, prerequisites, and article update date before use.

### Sources

- [Public symptom-theme discussion](https://www.reddit.com/r/vmware/comments/1qwouds/hpe_esxi_80_custom_image_last_update_oct_2025/)
- [KB 412258: ESXi remediation fails with incompatible software or configuration](https://knowledge.broadcom.com/external/article/412258/esxi-remediation-fails-from-7x-to-8x-fai.html)

## 6. VCF installer rejects mixed host vendors

**Synthetic prompt:** A synthetic VCF 9 management-domain deployment precheck rejects a cluster because ESXi hosts report different hardware vendors. The environment is a lab, but the requested answer must distinguish unsupported workaround ideas from production-supported design.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line n/a: No recognized VMware component or explicit error pattern was found.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Treat the vendor mismatch as a design constraint; validate supported VCF topology and use homogeneous supported hosts for production.
- **Pre-checks:** Record DMI vendor strings, hardware support, storage mode, host count and official deployment prerequisites.
- **Impact/risk and approval gate:** Precheck is READ-ONLY; altering DMI data is unsupported/RISKY and must not be recommended for production.
- **Rollback/recovery:** Make no host identity changes; redesign the lab or redeploy using supported homogeneous hardware.

### KB correctness assessment

**PASS — the agent correctly withheld a specific KB because the supplied evidence was insufficient for a verified resolution match.**

- No specific Broadcom KB was verified from the supplied evidence. Collect the missing evidence and search current official documentation by exact error/build before selecting a resolution.

### Sources

- [Public symptom-theme discussion](https://williamlam.com/2025/06/vcf-9-0-installer-workaround-for-esxi-hosts-with-different-vendor.html)
- [VCF 9 product documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0.html)

## 7. Supervisor enablement conflicts with enforced live patching

**Synthetic prompt:** Enabling vSphere Supervisor on a synthetic VCF 9 cluster fails an eligibility check while Enforce Live Patch is enabled in vLCM. No change should be made until cluster state, lifecycle policy, maintenance impact, and official applicability are verified.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line 1: Enabling vSphere Supervisor on a synthetic VCF 9 cluster fails an eligibility check while Enforce Live Patch is enabled in vLCM. No change should be made until cluster state, lifecycle policy, maintenance impact, and official applicability are verified.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Confirm the precise eligibility failure and official Supervisor/lifecycle prerequisites; change policy only in an approved window if official guidance supports it.
- **Pre-checks:** Export desired image, live-patch policy, compliance, Supervisor prerequisites and cluster capacity.
- **Impact/risk and approval gate:** Inspection is READ-ONLY; policy changes or remediation are DISRUPTIVE and require explicit approval.
- **Rollback/recovery:** Record original policy, confirm capacity, and restore it if Supervisor enablement does not proceed as planned.

### KB correctness assessment

**PASS — the agent correctly withheld a specific KB because the supplied evidence was insufficient for a verified resolution match.**

- No specific Broadcom KB was verified from the supplied evidence. Collect the missing evidence and search current official documentation by exact error/build before selecting a resolution.

### Sources

- [Public symptom-theme discussion](https://williamlam.com/2025/07/quick-tip-disable-esx-live-patching-enforcement-to-enable-vsphere-supervisor-service.html)
- [VCF 9 vSphere Supervisor documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/vsphere-supervisor.html)

## 8. VCF lifecycle component remains after failed deployment

**Synthetic prompt:** A synthetic VCF 9.1 installation fails late and reports that a lifecycle component could not be deleted. Component health, task history, logs, deployment state, and supported cleanup procedure are unknown. Manual deletion must not be assumed safe.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line n/a: No recognized VMware component or explicit error pattern was found.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Collect component/task state and official logs, check for a published recovery procedure, and escalate rather than manually deleting unknown state.
- **Pre-checks:** Capture task IDs, health, deployment topology, logs, backups and current official 9.1 guidance.
- **Impact/risk and approval gate:** Collection is READ-ONLY; manual component deletion is RISKY and approval/support-gated.
- **Rollback/recovery:** Preserve appliance snapshots/backups only where supported; use the product's documented retry/restore workflow.

### KB correctness assessment

**PASS — the agent correctly withheld a specific KB because the supplied evidence was insufficient for a verified resolution match.**

- No specific Broadcom KB was verified from the supplied evidence. Collect the missing evidence and search current official documentation by exact error/build before selecting a resolution.

### Sources

- [Public symptom-theme discussion](https://community.broadcom.com/vmware-cloud-foundation/discussion/vcf-91-installation-lifecycle-component-issue)
- [VCF 9.1 documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1.html)

## 9. VCSA update staging file missing

**Synthetic prompt:** A synthetic VCSA 8 update fails during staging with Errno 2 for patching_backup_config.json. update_microservice.log also records a checksum mismatch. ISO integrity, free space, certificates, prior failed state, and backup status need verification.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line 1: A synthetic VCSA 8 update fails during staging with Errno 2 for patching_backup_config.json. update_microservice.log also records a checksum mismatch. ISO integrity, free space, certificates, prior failed state, and backup status need verification.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Verify ISO checksum, storage, token/certificates and backup; follow the exact KB branch matching the evidence, then restage.
- **Pre-checks:** Confirm file path, checksum log, free space, ISO source, certificate health, prior state and file-based backup.
- **Impact/risk and approval gate:** Checks/unstage are low-risk; service restart, RPM repair, lsdoctor or snapshot operations require approval.
- **Rollback/recovery:** Take the KB-required offline snapshot where applicable and file-based backup; revert only using supported recovery.

### KB correctness assessment

**PASS — the agent identified a verified, symptom-matched official KB candidate.**

- [KB 399833: Error [Errno 2] patching_backup_config.json - vCenter Server Appliance](https://knowledge.broadcom.com/external/article/399833/vcenter-server-update-fails-with-error-i.html) — candidate because: The exact missing staging file and checksum mismatch are both present. Confirm exact build, topology, prerequisites, and article update date before use.

### Sources

- [Public symptom-theme discussion](https://community.broadcom.com/vmware-cloud-foundation/discussion/issue-upgrading-vcenter-appliance-from-80300500-to-00600-errno-2-no-such-file-or-directory)
- [KB 399833: Error Errno 2 patching_backup_config.json - VCSA](https://knowledge.broadcom.com/external/article/399833/vcenter-server-update-fails-with-error-i.html)

## 10. vMotion blocked by cross-generation CPU features

**Synthetic prompt:** A powered-on VM cannot vMotion from an older Intel host to a newer Intel host. The compatibility check reports CPU incompatibility and recommends EVC. Current cluster EVC, per-VM EVC, VM power-on history, CPU models, and application instruction requirements are unknown.

### Concise local-agent answer

- **Observed evidence map:** [E1] submitted input, line n/a: No recognized VMware component or explicit error pattern was found.
- **Leading hypothesis, not confirmed cause:** 1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
- **Confidence:** low. **Missing evidence:** Issue timeline and impact; Correlated logs from the same timestamp
- **End-to-end resolution approach:** Compare source/destination CPU features and EVC state; select a compatible baseline only after application requirements and downtime are understood.
- **Pre-checks:** Capture CPU models, compatibility error, cluster/per-VM EVC, VM power-on host, vHW and required instructions.
- **Impact/risk and approval gate:** Compatibility checks are READ-ONLY; lowering EVC/powering off the VM is DISRUPTIVE and approval-gated.
- **Rollback/recovery:** Do not change EVC until a maintenance window; retain original settings and power-on placement plan.

### KB correctness assessment

**PASS — the agent identified a verified, symptom-matched official KB candidate.**

- [KB 390403: vMotion failed due to EVC settings](https://knowledge.broadcom.com/external/article/390403) — candidate because: The prompt contains the documented vMotion CPU/EVC symptom. Confirm exact build, topology, prerequisites, and article update date before use.

### Sources

- [Public symptom-theme discussion](https://community.broadcom.com/vmware-cloud-foundation/question/vmotion-when-using-vcenter-8)
- [KB 390403: vMotion failed due to EVC settings](https://knowledge.broadcom.com/external/article/390403)
- [KB 313545: VMware EVC and CPU Compatibility FAQ](https://knowledge.broadcom.com/external/article/313545/vmware-evc-and-cpu-compatibility-faq.html)

## Overall verification

All ten prompts were run through the local deterministic case agent. Every run produced the full case structure, evidence IDs, hypotheses, confidence, missing evidence, safe/risky classification, approval gates, applicability language, and rollback considerations. Four cases contained enough exact evidence for the conservative matcher to name an official KB candidate; six correctly withheld a specific KB. Links should be rechecked at execution time because Broadcom articles and release applicability can change.
