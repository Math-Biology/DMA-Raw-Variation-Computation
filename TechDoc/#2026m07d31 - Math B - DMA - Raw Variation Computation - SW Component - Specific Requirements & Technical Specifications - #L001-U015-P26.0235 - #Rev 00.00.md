 

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
| Effective Date | 31 July 2026 |
| Current Revision | 00.00 |
| Short Doc Code | \[RVC\] |

# 

2. # **Definitions & Acronyms**  {#definitions-&-acronyms}

| Def. / Acron. | Description |
| :---- | :---- |
|  Math B | Math Biology |
| DMA  | Deep Metabolic-process Assessment |
| RVC | Raw Variations Computation |
|  |  |
|  |  |

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

**Batch Orchestration and Per-Sheet Excel Export**

Requirement: The component shall process, in batch, every visit folder under the configured input path and every worksheet of each contained Excel workbook, excluding non-measurement sheets. For each processed worksheet it shall export two Excel files, the unmodified original data and the computed percentage variations, into a dedicated, filesystem-safe output folder, keeping data separated per source sheet/protocol.

**\[REQ-RVC-P26.0001\]** 

Linked to: **\[REQ-G-P26.xxxx\]**

**Requirement Name**

Requirement: 

**\[REQ-RVC-P26.0001\]** 

Linked to: **\[REQ-G-P26.xxxx\]**

**Requirement Name**

Requirement: 

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

**Batch Iteration and Dual-Workbook Export**

Specification: The run(config\_path) function iterates each sub-folder (visit) of input\_path, and for each Excel file reads all sheets via pandas.read\_excel(sheet\_name=None), discarding the sheets Screening Protocol and Notes. For every retained sheet it creates an output folder named \<visit\>\_\<filename\>\_\<sheet\> under output\_path and writes two workbooks: \<filename\>\_\<sheet\>\_\<original\>.xlsx (raw data, all rows) and \<filename\>\_\<sheet\>\_\<percentage\_variation\>.xlsx (computed variations, baseline row excluded), where the suffixes are taken from it\_config.

Verification Method: Automated integration test, pytest class TestRun (test\_both\_output\_files\_created, test\_percentage\_variation\_values\_correct, test\_original\_file\_contains\_all\_rows, test\_variation\_file\_excludes\_baseline\_row, test\_excluded\_sheets\_produce\_no\_output). Acceptance: both files present for a valid sheet, correct variation values, original retains all rows, variation excludes the baseline row, and excluded sheets produce no output folder.

**\[SPEC-RVC-P26.0004\]**

Linked to: **\[REQ-RVC-P26.0003\]**

**Filename Sanitization**

Specification: The clean\_filename(filename, replacement="\_") function replaces every character in the forbidden set \< \> : " / \\ | ? \* and . with the replacement character (default underscore), guaranteeing that sheet names are converted into filesystem-safe folder and file names before any workbook is written.

Verification Method: Automated unit test, pytest class TestCleanFilename (test\_forbidden\_chars\_replaced, test\_clean\_string\_unchanged, test\_custom\_replacement\_char, test\_empty\_string). Acceptance: all forbidden characters replaced, already-clean strings unchanged, custom replacement honoured, empty string handled.

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
| 00.01 |  |  |  |
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

