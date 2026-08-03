 

# 

# **Math B \- DMA \- Raw Variation Computation Specific Requirements & Technical Specifications**

## 

## Raw Variation Computation Specific Requirements & Technical Specifications

# 

# **TABLE OF CONTENTS**

[**1\. Document Information	3**](#document-information)

[2\. Definitions & Acronyms	3](#definitions-&-acronyms)

[3\. Referencies	3](#referencies)

[**4\. Introduction (Purpose & Scope)	5**](#introduction-\(purpose-&-scope\))

[**5\. Involved Components	5**](#involved-components)

[**6\. Specific Requirements	5**](#specific-requirements)

[**7\. Technical Specification	6**](#technical-specification)

[**8\. Parameters	6**](#parameters)

[**9\. Document Governance	7**](#document-governance)

[9.1. Revision List & Notes	7](#revision-list-&-notes)

# 

1. # **Document Information** {#document-information}

| Doc. Title. | DMA \- Raw Variation Computation Specific Requirements & Technical Specifications |
| :---- | :---- |
| Doc ID | \#L001-U001-P26.0235 |
| Doc Type | requirements & technical specification |
| Department  &/or Processes Area | R\&D |
| Effective Date | 03 August 2026 |
| Current Revision | 00.01 |
| Short Doc Code | \[RVC\] |

# 

2. # **Definitions & Acronyms**  {#definitions-&-acronyms}

| Def. / Acron. | Description |
| :---- | :---- |
|  Math B | Math Biology |
| DMA  | Deep Metabolic-process Assessment |
| RVC | Raw Variations Computation |
| GR | General Requirement |
| SR | Specific Requirement |
| TS | Technical Specification |
| DTM | Design Traceability Matrix |
| CSV | Comma-Separated Values |
| NaN | Not a Number (missing-value marker) |
| PII | Personally Identifiable Information |

3. # **Referencies** {#referencies}

Unless otherwise specified, definitions and acronyms are defined in DOC-QMS-001 – Definitions, Acronyms & Ontology.

| Ref. | Doc ID | Description or Link |
| :---- | :---- | :---- |
| ref.1 | \#L001-U001-P26.0007 | Math B \- Definitions, Acronyms & Ontology |
| ref.2 | \#L001-U015-P26.0020 | Math B \- DMA \- Hardware & Software Components Tree & Accessory \- Registry |
| ref.3 | \#L001-U015-P26.0018 | Math B \- Procedure \- Protocols & IDs \- Revisions and Versioning and Status |
| ref.4 | \#L001-U015-P26.0039 | Math B \- Procedure Requirements, Technical Specification & Design Traceability Matrix \- Principles |
| ref.5 | \#L001-U015-P26.0035 | Math B \- DMA Screening \- General Hardware & Software Requirements |
| ref.6 | \#L001-U015-P26.0033 | Math B \- DMA Screening \- Design Traceability Matrix (DTM) \- MDR Class I |

4. # **Introduction (Purpose & Scope)** {#introduction-(purpose-&-scope)}

This document defines the Raw Variation Computation Specific Requirements (SR) and Technical Specifications (TS) for the DMA Screening system, a Class I medical device developed by Math Biology S.r.l. for the non-invasive acquisition of quasi-static bioelectrical surface currents. 

The document is produced in accordance with the Quality Management System requirements of ISO 13485:2016 and the applicable provisions of EU Regulation 2017/745 (MDR). It constitutes a formal design output record within the DMA Screening History File and provides the foundational input for the Design Traceability Matrix (DTM, ref.6). Requirements derivation, identifier coding, and traceability rules applied throughout this document follow the procedures defined in ref. 3 and ref. 4\.

Each specific requirement (SR) in this document is formally linked to a higher-level General Requirement (GR), establishing a clear vertical chain of compliance as required by ISO 13485:2016 Clause 7.3. Moreover, in this documentation structure, each SR is defined with enough granularity to concurrently serve as the detailed Technical Specification (TS) for the implementation of the Raw Variation Computation, ensuring direct traceability for subsequent verification and validation activities (MDR Annex II, Section 3).

## 

5. # **Involved Components** {#involved-components}

This document relates to the software components listed in the following table. For additional details about Components see **ref. 2\.**

| Component\_ID | Versioning | Name |
| :---- | :---- | :---- |
| \#L001-U015-P26.0234 | 00.00 | Raw Variation Computation |
|  |  |  |
|  |  |  |

6. # **Specific Requirements** {#specific-requirements}

This section lists all Specific Requirements for the Raw Variation Computation. Each SR is derived from one or more General Requirements (GR) defined in **ref.5**. 

**\[REQ-RVC-P26.0001\]** 

Linked to: **\[REQ-G-P26.0072\]**

**External Configuration Loading**

Requirement: The component shall load all execution parameters at runtime from an external XML configuration file, with no processing parameter hardcoded in the source. The configuration shall provide, as a minimum, the input and output folder paths, the set of numerical processing thresholds, and the output-file label suffixes used to name generated workbooks. A missing or malformed configuration file shall result in a controlled failure of the run.

**\[REQ-RVC-P26.0002\]** 

Linked to: **\[REQ-G-P26.0018\]**

**Baseline Percentage-Variation Computation**

Requirement: For each numerical measurement series in an input sheet, the component shall compute the percentage variation of every observation relative to a per-series baseline, where the baseline is the minimum strictly-positive value of the series. Non-numerical descriptor columns shall be preserved unchanged; null, zero and missing values shall be handled as missing data (NaN) and shall not corrupt the computation of other series.

**\[REQ-RVC-P26.0003\]** 

Linked to: **\[REQ-G-P26.0031\]**

**Batch Orchestration and Per-Sheet Excel Export (Legacy Entry Point)**

Requirement: As a legacy, backward-compatibility capability, the component shall be able to process, in batch, every visit folder under the configured input path and every worksheet of each contained Excel workbook, excluding non-measurement sheets. For each processed worksheet it shall export two Excel files, the unmodified original data and the computed percentage variations, into a dedicated, filesystem-safe output folder, keeping data separated per source sheet/protocol. This entry point is retained for backward compatibility only and is not the path invoked on program execution; the primary execution path is defined in REQ-RVC-P26.0005.

**\[REQ-RVC-P26.0005\]** 

Linked to: **\[REQ-G-P26.0031\]**, **\[REQ-G-P26.0011\]**

**Consolidated Multi-Sheet Visit Ingestion and Batch Orchestration**

Requirement: The component shall provide a primary entry point, invoked automatically on program execution, that ingests a single consolidated multi-sheet Excel workbook (one worksheet per visit) as its principal input. For each visit it shall extract the identifying metadata (patient identifier, visit identifier, visit date) and reconstruct the measurement table of markers versus acquisition points, discarding structural padding and any worksheet that does not contain measurement data. The orchestration shall process all visits in a single batch and shall emit progress information suitable for operator monitoring of long-running executions.

**\[REQ-RVC-P26.0006\]** 

Linked to: **\[REQ-G-P26.0018\]**

**Measurement Value Normalization**

Requirement: Prior to any computation, all measurement values shall be coerced to a numeric representation, and non-informative sentinels (zero, null and missing values) shall be normalized to a single missing-value marker, so that they neither participate in baseline determination nor corrupt the computation of other series.

**\[REQ-RVC-P26.0007\]** 

Linked to: **\[REQ-G-P26.0031\]**

**Consolidated Tidy (Long-Format) Output Generation**

Requirement: The component shall consolidate all processed visits into two global outputs in long (tidy) format — one carrying the original measurements and one carrying the computed percentage variations — where every record is uniquely identified by visit, marker and acquisition point together with the visit metadata. The original output shall retain the baseline row; the variation output shall exclude it.

### 

7. # **Technical Specification** {#technical-specification}

This section provides the Technical Specification for each Specific Requirement defined in Section 6\. 

**\[SPEC-RVC-P26.0001\]**

Linked to: **\[REQ-RVC-P26.0001\]**

**XML Configuration Parsing**

Specification: The load\_config(xml\_file) function parses the XML configuration with xml.etree.ElementTree and returns three dictionaries: (1) file\_config from \<file\_config\> with string values including input\_path and output\_path; (2) visit\_config from \<visit\_config\> with every child converted to float (eight thresholds threshold\_1..threshold\_8 in the delivered config.xml); (3) it\_config from \<it\_config\> with string output-label suffixes including original and percentage\_variation. If the file cannot be located the underlying parser raises FileNotFoundError, aborting the run. Note: the threshold values are loaded and reserved but are not yet consumed by the current processing logic (see section 8, Known Discrepancies).

Verification Method: Automated unit test, pytest class TestLoadConfig (test\_loads\_file\_config, test\_visit\_config\_values\_are\_floats, test\_loads\_it\_config\_suffixes, test\_missing\_file\_raises). Acceptance: paths returned verbatim, threshold values returned as float, suffixes returned verbatim, and FileNotFoundError raised on a missing file.

**\[SPEC-RVC-P26.0002\]**

Linked to: **\[REQ-RVC-P26.0002\]**

**Percentage-Variation Algorithm**

Specification: The compute\_percentage\_variations(df) function processes every column except the first (descriptor/label) column. For each processed column it determines base as the minimum strictly-positive value of the column, then computes, for every row from the second onward, percentage \= (value \- base) / base \* 100\. The first (baseline) row is dropped from the result; the descriptor column is carried through unchanged. Columns containing no strictly-positive value are skipped and left as-is. Upstream, zero, None and pd.NA are replaced by np.nan so that missing values propagate as NaN without affecting other columns.

Verification Method: Automated unit test, pytest class TestComputePercentageVariations (test\_basic\_variation, test\_baseline\_is\_global\_minimum\_not\_row\_0, test\_row\_0\_dropped\_from\_output, test\_label\_column\_not\_processed, test\_column\_with\_no\_positive\_values\_skipped, test\_nan\_in\_data\_propagates\_to\_output, test\_multiple\_columns\_computed\_independently). Acceptance: numeric equality (pytest.approx) to the expected percentages, baseline row removed, descriptor column preserved, and NaN handling as specified.

**\[SPEC-RVC-P26.0003\]**

Linked to: **\[REQ-RVC-P26.0003\]**

**Batch Iteration and Dual-Workbook Export (Legacy)**

Specification: This specification describes the legacy run() path (REQ-RVC-P26.0003), retained for backward compatibility and not invoked on program execution. The run(config\_path) function iterates each sub-folder (visit) of input\_path, and for each Excel file reads all sheets via pandas.read\_excel(sheet\_name=None), discarding the sheets Screening Protocol and Notes. For every retained sheet it creates an output folder named \<visit\>\_\<filename\>\_\<sheet\> under output\_path and writes two workbooks: \<filename\>\_\<sheet\>\_\<original\>.xlsx (raw data, all rows) and \<filename\>\_\<sheet\>\_\<percentage\_variation\>.xlsx (computed variations, baseline row excluded), where the suffixes are taken from it\_config.

Verification Method: Automated integration test, pytest class TestRun (test\_both\_output\_files\_created, test\_percentage\_variation\_values\_correct, test\_original\_file\_contains\_all\_rows, test\_variation\_file\_excludes\_baseline\_row, test\_excluded\_sheets\_produce\_no\_output). Acceptance: both files present for a valid sheet, correct variation values, original retains all rows, variation excludes the baseline row, and excluded sheets produce no output folder.

**\[SPEC-RVC-P26.0004\]**

Linked to: **\[REQ-RVC-P26.0003\]**

**Filename Sanitization**

Specification: The clean\_filename(filename, replacement="\_") function replaces every character in the forbidden set \< \> : " / \\ | ? \* and . with the replacement character (default underscore), guaranteeing that sheet names are converted into filesystem-safe folder and file names before any workbook is written.

Verification Method: Automated unit test, pytest class TestCleanFilename (test\_forbidden\_chars\_replaced, test\_clean\_string\_unchanged, test\_custom\_replacement\_char, test\_empty\_string). Acceptance: all forbidden characters replaced, already-clean strings unchanged, custom replacement honoured, empty string handled.

**\[SPEC-RVC-P26.0005\]**

Linked to: **\[REQ-RVC-P26.0005\]**

**Multi-Sheet Excel Parsing, Metadata Extraction & Table Reconstruction**

Specification: The run\_exported(config\_path) function opens Input/\<exported\_visits\_file\> via pandas.ExcelFile and iterates every sheet in sheet\_names. Sheets with fewer than three rows (df.shape\[0\] \< 3\) are skipped with a console notice. For each retained sheet, visit metadata is read from the first data row df.iloc\[0\]: patient\_id from "Patient ID", visit\_id from int("Visit ID") when present else the sheet name, and visit\_date from "Visit Date". Row df.iloc\[1\] is promoted to column headers, rows df.iloc\[2:\] become the measurement data with a reset index, and every column whose header is NaN (metadata overflow / padding) is dropped; the first surviving column is treated as the marker/descriptor column. The module \_\_main\_\_ guard invokes run\_exported() as the primary execution path, and a progress message is printed every 500 processed sheets.

Verification Method: Automated integration test, pytest class TestRunExported (test\_metadata\_columns\_populated, test\_short\_sheet\_skipped\_without\_error, test\_original\_csv\_has\_required\_columns). Acceptance: metadata columns populated from the first data row, sheets with fewer than three rows excluded from the output, and the marker column preserved as the descriptor.

**\[SPEC-RVC-P26.0006\]**

Linked to: **\[REQ-RVC-P26.0006\]**

**Numeric Coercion & Missing-Value Normalization**

Specification: In run\_exported, every measurement column (all columns after the marker column) is converted with pandas.to\_numeric(errors="coerce"), so non-parseable strings become NaN. The reconstructed table is then processed with df.replace(\{0: np.nan, None: np.nan, pd.NA: np.nan\}), mapping zero, None and pd.NA to np.nan. This guarantees that compute\_percentage\_variations receives numeric input and that zero and missing entries are excluded from the "minimum strictly-positive" baseline selection and propagate as NaN without affecting other series.

Verification Method: Automated tests, pytest TestRunExported.test\_string\_values\_converted\_to\_numeric (output value column has numeric dtype) together with TestComputePercentageVariations.test\_column\_with\_no\_positive\_values\_skipped and test\_nan\_in\_data\_propagates\_to\_output. Acceptance: values stored as numeric, all-missing series skipped, NaN preserved through the computation.

**\[SPEC-RVC-P26.0007\]**

Linked to: **\[REQ-RVC-P26.0007\]**

**Wide-to-Long Melt & Dual Global CSV Export**

Specification: For each visit, run\_exported melts the reconstructed original table with df.melt(id\_vars=\[marker\_col\], var\_name="point", value\_name="value") and the computed-variation table with value\_name="percentage\_variation", inserting the visit\_id, patient\_id and visit\_date columns and renaming the marker column to "marker". Per-visit frames are accumulated and concatenated with pandas.concat(ignore\_index=True). Two CSV files are written under the configured output\_path (created if absent): all\_visits\_\<original\>.csv with columns visit\_id, patient\_id, visit\_date, marker, point, value (Base row retained) and all\_visits\_\<percentage\_variation\>.csv with columns visit\_id, patient\_id, visit\_date, marker, point, percentage\_variation (Base row excluded). The filename suffixes are taken from it\_config. Each written path is echoed to stdout.

Verification Method: Automated integration test, pytest class TestRunExported (test\_original\_csv\_created, test\_variation\_csv\_created, test\_original\_csv\_has\_required\_columns, test\_variation\_csv\_has\_required\_columns, test\_original\_csv\_includes\_base\_row, test\_variation\_csv\_excludes\_base\_row, test\_percentage\_variation\_values\_correct). Acceptance: both CSVs created with the exact column schema, Base row present in the original output and absent in the variation output, and correct percentage values.

8. # **Risk Analysis**

This section provides the Risk Analysis entries for each Specific Requirement, in compliance with ISO 14971 and ref.4. For each risk, severity × probability establishes the initial risk level; the mitigation link identifies the SR/TS providing the control; residual risk is stated after mitigation.

**\[RISK-RVC-P26.0001\]**

Linked to: **\[REQ-RVC-P26.0001\]**

**Risk Name: Silent or Uncontrolled Configuration Failure**

Risk: A missing, malformed or partially-populated configuration file may cause the run to abort with a raw, unhandled exception (FileNotFoundError / ParseError) and no user-facing message, or to proceed with default/empty values, leading the operator to run the component with unknown parameters. Severity: Medium (invalid or absent output, no patient exposure, offline module). Probability: Low-Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0001 mandates controlled failure on a missing/malformed configuration; SPEC-RVC-P26.0001 and test\_missing\_file\_raises verify the failure is raised rather than silently ignored. Residual risk: Low.

**\[RISK-RVC-P26.0002\]**

Linked to: **\[REQ-RVC-P26.0002\]**

**Risk Name: Incorrect Baseline / Missing-Value Misinterpretation**

Risk: Because the baseline is defined as the minimum strictly-positive value of a series rather than the first acquired value, an atypical or artefactual low reading can shift the baseline and distort all reported percentage variations; likewise, unintended NaN propagation could hide values in the output and be misread as valid data. Severity: Medium (misleading non-diagnostic indicators). Probability: Low. Initial risk: Medium. Mitigation: REQ-RVC-P26.0002 fixes the baseline definition and missing-value handling; SPEC-RVC-P26.0002 and the seven TestComputePercentageVariations cases pin the algorithm behaviour, including baseline selection, row dropping and NaN propagation. Residual risk: Low.

**\[RISK-RVC-P26.0003\]**

Linked to: **\[REQ-RVC-P26.0003\]**

**Risk Name: Incorrect Input Selection or Output Overwrite**

Risk: An unintended file may be processed, or an intended file skipped, due to the file-extension filter operator precedence (endswith(".xlsx") or endswith(".xls") and "\_p" not in file), which applies the "\_p" exclusion only to .xls files; in addition, re-running the batch over a populated output tree can overwrite prior results without warning, and configured thresholds that are not consumed by the logic may create a false expectation of threshold-based filtering. Severity: Low-Medium (wrong or duplicated output). Probability: Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0003 defines the intended iteration and exclusion scope; SPEC-RVC-P26.0003 with test\_excluded\_sheets\_produce\_no\_output, and SPEC-RVC-P26.0004 with TestCleanFilename, verify sheet exclusion and safe naming. Residual risk: Low-Medium.

**\[RISK-RVC-P26.0005\]**

Linked to: **\[REQ-RVC-P26.0005\]**; **\[SPEC-RVC-P26.0005\]**

**Risk Name: Silent Visit Skip or Metadata Misattribution**

Risk: A worksheet whose structure deviates from the expected export layout may be silently discarded (fewer than three rows) or produce mis-attributed metadata; if the "Patient ID", "Visit ID" or "Visit Date" columns are absent or relocated, the first-row lookup raises a KeyError that aborts the batch, or associates measurements with the wrong visit. Because the skip is reported only on the console, an operator may not notice that a visit is missing from the consolidated output. Severity: Medium (missing or misattributed non-diagnostic data, offline module, no patient exposure). Probability: Low-Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0005 fixes the ingestion contract and skip rule; SPEC-RVC-P26.0005 with TestRunExported.test\_short\_sheet\_skipped\_without\_error and test\_metadata\_columns\_populated verify controlled skipping and correct metadata extraction. Residual risk: Low-Medium.

**\[RISK-RVC-P26.0006\]**

Linked to: **\[REQ-RVC-P26.0006\]**; **\[SPEC-RVC-P26.0006\]**

**Risk Name: Data Loss through Coercion and Sentinel Normalization**

Risk: The blanket conversion of zero, None and pd.NA to NaN, combined with to\_numeric(errors="coerce"), may silently discard legitimate readings — a true zero measurement or a value stored in an unexpected textual format is converted to missing data and excluded from both the baseline selection and the output, without any warning to the operator. Severity: Medium (loss of otherwise valid non-diagnostic data). Probability: Low. Initial risk: Medium. Mitigation: REQ-RVC-P26.0006 defines the normalization contract; SPEC-RVC-P26.0006 with test\_string\_values\_converted\_to\_numeric, test\_column\_with\_no\_positive\_values\_skipped and test\_nan\_in\_data\_propagates\_to\_output pin the coercion and NaN-propagation behaviour. Residual risk: Low.

**\[RISK-RVC-P26.0007\]**

Linked to: **\[REQ-RVC-P26.0007\]**; **\[SPEC-RVC-P26.0007\]**

**Risk Name: Output Overwrite, Schema Drift and Plaintext PII Exposure**

Risk: Re-running the component overwrites the two global CSV files in place, without versioning, so a partial or erroneous batch can silently replace a valid prior output. Concatenating visits with heterogeneous acquisition-point columns yields sparse rows that may be misread downstream. In addition, the CSV outputs store visit metadata (patient\_id, visit\_date) in plaintext, with no encryption at rest applied by this component. Severity: Low-Medium (wrong or overwritten output; PII confidentiality handled by the downstream storage layer). Probability: Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0007 fixes the output schema and Base-row policy; SPEC-RVC-P26.0007 with the seven TestRunExported schema and value cases verify the exact column layout and correctness. Encryption at rest (REQ-G-P26.0073) is provided by the downstream storage layer and is treated as out of scope for this offline computation module (see scope note below). Residual risk: Low-Medium.

*Scope note (out-of-scope assumption):* This component operates offline on already-exported visit data and produces plaintext CSV files for downstream consumption. Data-at-rest encryption and access control (REQ-G-P26.0073) are assumed to be enforced by the downstream storage and synchronization layers and are therefore out of scope for the Raw Variation Computation. The code-level traceability anchor to REQ-COMP-P26.0073 records this dependency; it does not imply that encryption is implemented within this module.

9. # **Parameters** {#parameters}

This section contains all the fixed default parameters for the Raw Variation Computation.

| Parameter | Value | Description |
| :---- | :---- | :---- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

# 

## 

# 

10. # **Document Governance** {#document-governance}

    1. ## **Revision List & Notes**  {#revision-list-&-notes}

| Revisision  | Date | Approved By \-  Name Acronymus | Notes |
| :---- | :---- | :---- | :---- |
| 00.02 |  |  |  |
| 00.01 | \#2026m08d03 | \[IR\] | Updated from implemented source code. Added SR/SPEC/RISK-0005..0007 documenting the primary run\_exported entry point (consolidated multi-sheet ingestion, numeric coercion, tidy long-format CSV export). Annotated REQ/SPEC-0003 (run()) as legacy. Definitions expanded. PII/encryption (REQ-G-P26.0073) recorded as out-of-scope assumption. Verified against tests/test\_raw\_variation.py (31 passed). |
| 00.00 | \#2026m07d31 | \[IR\] | First edition. SR, TS and Risk Analysis populated from the implemented source code (raw\_variation.py, config.xml) and verified against tests/test\_raw\_variation.py. |

    2. **Authors, Contributors & Reviewers** 

| Name & Surname  \[Name Acronymus\] | Role:  \[Authors, Contributors, Reviewers, Approver\] |
| :---- | :---- |
| Ilaria Rocco \[IR\] |  Author |
|  |  |
|  |  |

    3. **Signatures & Approvals**

for Math Biology,

City

| Date | Name & Surname   | Role | Signature |
| :---- | :---- | :---- | :---- |
| \#yyyymMMdDD  |  | s |  |
|   |  |  |  |
|   |  |  |  |

for \<XXX OTHER PARTIES\>

City

| Date | Name & Surname   | Role | Signature |
| :---- | :---- | :---- | :---- |
|   |  |  |  |
|   |  |  |  |
|   |  |  |  |

