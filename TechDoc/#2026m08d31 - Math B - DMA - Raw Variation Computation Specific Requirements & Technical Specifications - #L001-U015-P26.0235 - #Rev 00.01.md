 

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

[**7\. Technical Specification	7**](#technical-specification)

[**8\. Risk Analysis	10**](#risk-analysis)

[**9\. Parameters	12**](#parameters)

[**10\. Document Governance	13**](#document-governance)

[10.1. Revision List & Notes	13](#revision-list-&-notes)

# 

1. # **Document Information**

| Doc. Title. | DMA \- Raw Variation Computation Specific Requirements & Technical Specifications |
| :---- | :---- |
| Doc ID | \#L001-U015-P26.0235 |
| Doc Type | requirements & technical specification |
| Department  &/or Processes Area | R\&D |
| Effective Date | 3 August 2026 |
| Current Revision | 00.01 |
| Short Doc Code | \[RVC\] |

# 

2. # **Definitions & Acronyms** 

| Def. / Acron. | Description |
| :---- | :---- |
|  Math B | Math Biology |
| DMA  | Deep Metabolic-process Assessment |
| RVC | Raw Variations Computation |
|  |  |
|  |  |

3. # **Referencies**

Unless otherwise specified, definitions and acronyms are defined in DOC-QMS-001 – Definitions, Acronyms & Ontology.

| Ref. | Doc ID | Description or Link |
| :---- | :---- | :---- |
| ref.1 | \#L001-U001-P26.0007 | Math B \- Definitions, Acronyms & Ontology |
| ref.2 | \#L001-U015-P26.0020 | Math B \- DMA \- Hardware & Software Components Tree & Accessory \- Registry |
| ref.3 | \#L001-U015-P26.0018 | Math B \- Procedure \- Protocols & IDs \- Revisions and Versioning and Status |
| ref.4 | \#L001-U015-P26.0039 | Math B \- Procedure Requirements, Technical Specification & Design Traceability Matrix \- Principles |
| ref.5 | \#L001-U015-P26.0035 | Math B \- DMA Screening \- General Hardware & Software Requirements |
| ref.6 | \#L001-U015-P26.0033 | Math B \- DMA Screening \- Design Traceability Matrix (DTM) \- MDR Class I |

4. # **Introduction (Purpose & Scope)**

This document defines the Raw Variation Computation Specific Requirements (SR) and Technical Specifications (TS) for the DMA Screening system, a Class I medical device developed by Math Biology S.r.l. for the non-invasive acquisition of quasi-static bioelectrical surface currents. 

The document is produced in accordance with the Quality Management System requirements of ISO 13485:2016 and the applicable provisions of EU Regulation 2017/745 (MDR). It constitutes a formal design output record within the DMA Screening History File and provides the foundational input for the Design Traceability Matrix (DTM, ref.6). Requirements derivation, identifier coding, and traceability rules applied throughout this document follow the procedures defined in ref. 3 and ref. 4\.

Each specific requirement (SR) in this document is formally linked to a higher-level General Requirement (GR), establishing a clear vertical chain of compliance as required by ISO 13485:2016 Clause 7.3. Moreover, in this documentation structure, each SR is defined with enough granularity to concurrently serve as the detailed Technical Specification (TS) for the implementation of the Raw Variation Computation, ensuring direct traceability for subsequent verification and validation activities (MDR Annex II, Section 3).

## 

5. # **Involved Components**

This document relates to the software components listed in the following table. For additional details about Components see **ref. 2\.**

| Component\_ID | Versioning | Name |
| :---- | :---- | :---- |
| \#L001-U015-P26.0234 | 00.00 | Raw Variation Computation |
|  |  |  |
|  |  |  |

6. # **Specific Requirements**

This section lists all Specific Requirements for the Raw Variation Computation. Each SR is derived from one or more General Requirements (GR) defined in **ref.5**. 

**\[REQ-RVC-P26.0001\]** 

Linked to: **\[REQ-G-P26.0072\]**

**External Configuration Loading**

Requirement: The component loads all execution parameters at runtime from an external XML configuration file, with no processing parameter hardcoded in the source. The configuration provides, as a minimum, the input and output folder paths and the output-file label suffixes used to name generated workbooks. A missing or malformed configuration file results in a controlled failure of the run.

**\[REQ-RVC-P26.0002\]** 

Linked to: **\[REQ-G-P26.0018\]**

**Baseline Percentage-Variation Computation**

Requirement: For each numerical measurement series in an input sheet, the component computes the percentage variation of every observation relative to a per-series baseline, where the baseline is the minimum strictly-positive value of the series. Non-numerical descriptor columns are preserved unchanged; null, zero and missing values are handled as missing data (NaN) and don’t corrupt the computation of other series.

**\[REQ-RVC-P26.0003\]** 

Linked to: **\[REQ-G-P26.0031\]**

**Batch Orchestration and Per-Sheet Excel Export (Legacy Entry Point)**

Requirement: As a legacy, backward-compatibility capability, the component process, in batch, every visit folder under the configured input path and every worksheet of each contained Excel workbook, excluding non-measurement sheets. For each processed worksheet it exports two Excel files, the unmodified original data and the computed percentage variations, into a dedicated, filesystem-safe output folder, keeping data separated per source sheet/protocol. This entry point is retained for backward compatibility only and is not the path invoked on program execution; the primary execution path is defined in REQ-RVC-P26.0004.

**\[REQ-RVC-P26.0004\]** 

Linked to: **\[REQ-G-P26.0031\], \[REQ-G-P26.0011\]**

**Consolidated Multi-Sheet Visit Ingestion and Batch Orchestration**

Requirement: The component provides a primary entry point, invoked automatically on program execution, that ingests a single consolidated multi-sheet Excel workbook (one worksheet per visit) as its principal input. For each visit it extracts the identifying metadata (patient identifier, visit identifier, visit date) and reconstructs the measurement table of markers versus acquisition points, discarding structural padding and any worksheet that does not contain measurement data. The orchestration process all visits in a single batch and emit progress information suitable for operator monitoring of long-running executions.

**\[REQ-RVC-P26.0005\]** 

Linked to: **\[REQ-G-P26.0018\]**

**Measurement Value Normalization**

Requirement: Prior to any computation, all measurement values must be coerced to a numeric representation, and non-informative sentinels (zero, null and missing values) must be normalized to a single missing-value marker, so that they neither participate in baseline determination nor corrupt the computation of other series.

**\[REQ-RVC-P26.0006\]**

Linked to: **\[REQ-G-P26.0031\]**

**Consolidated Tidy (Long-Format) Output Generation**

Requirement: The component consolidates all processed visits into two global outputs in long (tidy) format — one carrying the original measurements and one carrying the computed percentage variations — where every record is uniquely identified by visit, marker and acquisition point together with the visit metadata. The original output retains the baseline row; the variation output excludes it.

**\[REQ-RVC-P26.0007\]**

Linked to: **\[REQ-G-P26.0018\]**

**Per-Visit Oscillation (δ) Computation**

Requirement: For each anatomical point within a single visit, the component computes an oscillation index δ measuring the spread of the raw percentage variations across markers, defined as the maximum value minus the minimum strictly-positive value of the series, expressed in percentage points. A point that does not present at least two strictly-positive values yields δ \= 0\. No corrective rule is applied to the input; the raw percentage variations are consumed as-is.

**\[REQ-RVC-P26.0008\]**

Linked to: **\[REQ-G-P26.0018\], \[REQ-G-P26.0089\]**

**Oscillation Batch Orchestration & Consolidated Export**

Requirement: The component provides a pipeline entry point that ingests the consolidated long-format percentage-variation dataset produced upstream, groups records by (visit\_id, patient\_id, visit\_date, point), applies the δ computation per group, and exports a consolidated oscillation dataset (one record per visit/point) with a fixed column schema to the configured output location. Absence or multiplicity of the expected input results in a controlled error.

**\[REQ-RVC-P26.0009\]**

Linked to: **\[REQ-G-P26.0087\]**

**Median Oscillation Aggregation per Anatomical Point**

Requirement: The component aggregates the per-visit oscillation dataset into a population-level summary, computing the median δ for each anatomical point across all visits, ordered by descending median, and exports it as a dedicated sidecar dataset (one record per point).

**\[REQ-RVC-P26.0010\]**

Linked to: **\[REQ-G-P26.0086\], \[REQ-G-P26.0029\]**

**Oscillation Analysis Report Generation**

Requirement: The component generates a summary report of the oscillation analysis, comprising a ranked visualization of median δ per anatomical point and a compiled PDF document assembled via a programmatic templating/formatting engine. All textual output of the report shall use exclusively non-diagnostic language consistent with the device's Intended Purpose, and shall not use terms implying a clinical diagnosis, specific pathology or treatment recommendation (ref.5, REQ-G-P26.0022 / REQ-G-P26.0028).

7. # **Technical Specification**

This section provides the Technical Specification for each Specific Requirement defined in Section 6\. 

**\[SPEC-RVC-P26.0001\]**

Linked to: **\[REQ-RVC-P26.0001\]**

**XML Configuration Parsing**

Specification: The load\_config(xml\_file) function parses the XML configuration with xml.etree.ElementTree and returns three dictionaries: (1) file\_config from \<file\_config\> with string values including input\_path and output\_path; (2) visit\_config from \<visit\_config\> with every child converted to float (eight thresholds threshold\_1..threshold\_8 in the delivered config.xml); (3) it\_config from \<it\_config\> with string output-label suffixes including original and percentage\_variation. If the file cannot be located the underlying parser raises FileNotFoundError, aborting the run. Note: the threshold values are loaded and reserved but are not yet consumed by the current processing logic.

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

Specification: The clean\_filename(filename, replacement=“\_”) function replaces every character in the forbidden set \< \> : " / \\ | ? \* and . with the replacement character (default underscore), guaranteeing that sheet names are converted into filesystem-safe folder and file names before any workbook is written.

Verification Method: Automated unit test, pytest class TestCleanFilename (test\_forbidden\_chars\_replaced, test\_clean\_string\_unchanged, test\_custom\_replacement\_char, test\_empty\_string). Acceptance: all forbidden characters replaced, already-clean strings unchanged, custom replacement honoured, empty string handled.

**\[SPEC-RVC-P26.0005\]**

Linked to: **\[REQ-RVC-P26.0004\]**

**Multi-Sheet Excel Parsing, Metadata Extraction & Table Reconstruction**

Specification: The run\_exported(config\_path) function opens Input/\<exported\_visits\_file\> via pandas.ExcelFile and iterates every sheet in sheet\_names. Sheets with fewer than three rows (df.shape\[0\] \< 3\) are skipped with a console notice. For each retained sheet, visit metadata is read from the first data row df.iloc\[0\]: patient\_id from “Patient ID”, visit\_id from int(“Visit ID”) when present else the sheet name, and visit\_date from “Visit Date”. Row df.iloc\[1\] is promoted to column headers, rows df.iloc\[2:\] become the measurement data with a reset index, and every column whose header is NaN (metadata overflow / padding) is dropped; the first surviving column is treated as the marker/descriptor column. The module \_\_main\_\_ guard invokes run\_exported() as the primary execution path, and a progress message is printed every 500 processed sheets.

Verification Method: Automated integration test, pytest class TestRunExported (test\_metadata\_columns\_populated, test\_short\_sheet\_skipped\_without\_error, test\_original\_csv\_has\_required\_columns). Acceptance: metadata columns populated from the first data row, sheets with fewer than three rows excluded from the output, and the marker column preserved as the descriptor.

**\[SPEC-RVC-P26.0006\]**

Linked to: **\[REQ-RVC-P26.0005\]**

**Numeric Coercion & Missing-Value Normalization**

Specification: In run\_exported, every measurement column (all columns after the marker column) is converted with pandas.to\_numeric(errors=“coerce”), so non-parseable strings become NaN. The reconstructed table is then processed with df.replace({0: np.nan, None: np.nan, pd.NA: np.nan}), mapping zero, None and pd.NA to np.nan. This guarantees that compute\_percentage\_variations receives numeric input and that zero and missing entries are excluded from the “minimum strictly-positive” baseline selection and propagate as NaN without affecting other series.

Verification Method: Automated tests, pytest TestRunExported.test\_string\_values\_converted\_to\_numeric (output value column has numeric dtype) together with TestComputePercentageVariations.test\_column\_with\_no\_positive\_values\_skipped and test\_nan\_in\_data\_propagates\_to\_output. Acceptance: values stored as numeric, all-missing series skipped, NaN preserved through the computation.

**\[SPEC-RVC-P26.0007\]**

Linked to: **\[REQ-RVC-P26.0006\]**

**Wide-to-Long Melt & Dual Global CSV Export**

Specification: For each visit, run\_exported melts the reconstructed original table with df.melt(id\_vars=\[marker\_col\], var\_name=“point”, value\_name=“value”) and the computed-variation table with value\_name=“percentage\_variation”, inserting the visit\_id, patient\_id and visit\_date columns and renaming the marker column to “marker”. Per-visit frames are accumulated and concatenated with pandas.concat(ignore\_index=True). Two CSV files are written under the configured output\_path (created if absent): all\_visits\_\<original\>.csv with columns visit\_id, patient\_id, visit\_date, marker, point, value (Base row retained) and all\_visits\_\<percentage\_variation\>.csv with columns visit\_id, patient\_id, visit\_date, marker, point, percentage\_variation (Base row excluded). The filename suffixes are taken from it\_config. Each written path is echoed to stdout.

Verification Method: Automated integration test, pytest class TestRunExported (test\_original\_csv\_created, test\_variation\_csv\_created, test\_original\_csv\_has\_required\_columns, test\_variation\_csv\_has\_required\_columns, test\_original\_csv\_includes\_base\_row, test\_variation\_csv\_excludes\_base\_row, test\_percentage\_variation\_values\_correct). Acceptance: both CSVs created with the exact column schema, Base row present in the original output and absent in the variation output, and correct percentage values.

**\[SPEC-RVC-P26.0008\]**

Linked to: **\[REQ-RVC-P26.0007\]**

**δ Column-Oscillation Algorithm**

Specification: The compute\_column\_oscillation(column) function drops NaN, keeps strictly-positive values (\> 0\) and returns float(max \- min) of those; it returns 0.0 when fewer than two strictly-positive values remain (zeros, negatives and NaN excluded). The compute\_oscillations(df) function applies compute\_column\_oscillation to every numeric column (df.select\_dtypes(include=\[np.number\])) and returns a pandas.Series named "oscillation\_%" indexed by column name. Defined in oscillations/src/oscillation.py.

Verification Method: Automated unit test, pytest classes TestComputeColumnOscillation (test\_normal\_range, test\_zeros\_excluded\_from\_min, test\_negatives\_excluded, test\_single\_positive\_returns\_zero, test\_all\_zeros\_returns\_zero, test\_empty\_series\_returns\_zero, test\_all\_negatives\_returns\_zero, test\_nan\_values\_ignored, test\_identical\_positive\_values, test\_returns\_float) and TestComputeOscillations (test\_output\_name, test\_index\_contains\_numeric\_columns\_only, test\_values), in oscillations/tests/test\_oscillation.py. Acceptance: δ equals the expected value (pytest.approx), zeros/negatives/NaN excluded from the range, sub-two-positive series return 0.0, non-numeric columns excluded, and the Series is named "oscillation\_%".

**\[SPEC-RVC-P26.0009\]**

Linked to: **\[REQ-RVC-P26.0008\]**

**Grouped Oscillation Computation & CSV Export**

Specification: The run(input\_path, output\_path) function in oscillations/run\_oscillation.py reads the input CSV, groups by GROUP\_KEYS \= \[visit\_id, patient\_id, visit\_date, point\], applies compute\_column\_oscillation to each group's percentage\_variation series, resets the index and renames the result column to oscillation\_%; it creates OUTPUT\_DIR if absent and writes a CSV with columns \[visit\_id, patient\_id, visit\_date, point, oscillation\_%\]. The find\_input\_file() helper auto-discovers the single \*.csv present in data/input, raising FileNotFoundError when none is present and ValueError when more than one is present. Note: input and output locations are module-level constants (data/input, data/output) and are not read from config.xml — see RISK-RVC-P26.0008.

Verification Method: Automated integration test, pytest classes TestFindInputFile (test\_single\_csv\_returned, test\_no\_csv\_raises\_file\_not\_found, test\_multiple\_csvs\_raises\_value\_error) and TestRun (test\_output\_file\_created, test\_output\_schema, test\_one\_row\_per\_visit\_point, test\_oscillation\_values, test\_output\_dir\_created\_if\_missing), in oscillations/tests/test\_run\_oscillation.py. Acceptance: exact output schema, one record per (visit, point), correct δ values, output directory created if missing, and controlled errors on zero or multiple candidate inputs.

**\[SPEC-RVC-P26.0010\]**

Linked to: **\[REQ-RVC-P26.0009\]**

**Median-by-Point Aggregation & Sidecar Export**

Specification: The compute\_median\_by\_point(output\_path) function reads the oscillation CSV, groups by point, computes the pandas median of oscillation\_%, renames it to median\_oscillation\_%, sorts the result in descending order, and writes a sidecar CSV named \<stem\>\_median\_by\_point.csv with columns \[point, median\_oscillation\_%\]. Defined in oscillations/run\_oscillation.py.

Verification Method: Automated integration test, pytest class TestComputeMedianByPoint (test\_output\_file\_created, test\_output\_schema, test\_one\_row\_per\_point, test\_median\_values, test\_sorted\_descending), in oscillations/tests/test\_run\_oscillation.py. Acceptance: exact sidecar schema, one record per anatomical point, correct median values, and descending order.

**\[SPEC-RVC-P26.0011\]**

Linked to: **\[REQ-RVC-P26.0010\]**

**Median-δ Chart Generation**

Specification: The plot\_median\_by\_point(df\_median, out\_dir) function in oscillations/src/plot\_oscillations.py renders a horizontal matplotlib bar chart of median\_oscillation\_% per anatomical point, creates the figures/ subdirectory under out\_dir and writes the image to out\_dir/figures/median\_by\_point.png at 150 DPI. It requires df\_median to carry the columns point and median\_oscillation\_%.

Verification Method: Automated unit test, pytest class TestPlotMedianByPoint (test\_output\_file\_created, test\_output\_is\_png \[PNG magic-byte header\], test\_figures\_subdirectory\_created), in oscillations/tests/test\_plot\_oscillations.py. Acceptance: a valid PNG file is produced and the figures/ subdirectory is created.

**\[SPEC-RVC-P26.0012\]**

Linked to: **\[REQ-RVC-P26.0010\]**

**Oscillation PDF Report Compilation**

Specification: The generate\_report(output\_csv, median\_csv) function in oscillations/src/generate\_report.py computes dataset statistics (\_compute\_stats: n\_rows, n\_visits, n\_points, mean, median, zero\_pct), escapes LaTeX special characters character-by-character (\_tex\_escape), builds ranked table rows (\_build\_table\_rows), renders an article-class LaTeX template and runs pdflatex twice in nonstopmode to resolve the table of contents, returning the PDF path. run\_oscillation.py orchestrates the sequence run \-\> compute\_median\_by\_point \-\> generate\_report, tolerating report-generation failure with a printed warning rather than aborting the pipeline.

Verification Method: Automated unit test, pytest classes TestTexEscape (test\_underscore\_escaped, test\_backslash\_becomes\_textbackslash, test\_no\_double\_escape, test\_plain\_text\_unchanged), TestComputeStats (test\_n\_rows, test\_n\_visits, test\_mean, test\_zero\_pct) and TestBuildTableRows (test\_rank\_starts\_at\_one, test\_value\_formatted\_two\_decimals, test\_row\_ends\_with\_latex\_newline), in oscillations/tests/test\_generate\_report.py. Acceptance: correct LaTeX escaping without double-escaping, correct summary statistics, and correctly formatted table rows. Verification gap (flagged): end-to-end PDF compilation via pdflatex depends on an external toolchain and is not exercised by the unit tests; a compilation failure surfaces only as a runtime warning.

8. # **Risk Analysis**

This section provides the Risk Analysis entries for each Specific Requirement, in compliance with ISO 14971 and ref.4. For each risk, severity × probability establishes the initial risk level; the mitigation link identifies the SR/TS providing the control; residual risk is stated after mitigation.

**\[RISK-RVC-P26.0001\]**

Linked to: **\[REQ-RVC-P26.0001\]**

**Silent or Uncontrolled Configuration Failure**

Risk: A missing, malformed or partially-populated configuration file may cause the run to abort with a raw, unhandled exception (FileNotFoundError / ParseError) and no user-facing message, or to proceed with default/empty values, leading the operator to run the component with unknown parameters. Severity: Medium (invalid or absent output, no patient exposure, offline module). Probability: Low-Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0001 mandates controlled failure on a missing/malformed configuration; SPEC-RVC-P26.0001 and test\_missing\_file\_raises verify the failure is raised rather than silently ignored. Residual risk: Low.

**\[RISK-RVC-P26.0002\]**

Linked to: **\[REQ-RVC-P26.0002\]**

**Incorrect Baseline / Missing-Value Misinterpretation**

Risk: Because the baseline is defined as the minimum strictly-positive value of a series rather than the first acquired value, an atypical or artefactual low reading can shift the baseline and distort all reported percentage variations; likewise, unintended NaN propagation could hide values in the output and be misread as valid data. Severity: Medium (misleading non-diagnostic indicators). Probability: Low. Initial risk: Medium. Mitigation: REQ-RVC-P26.0002 fixes the baseline definition and missing-value handling; SPEC-RVC-P26.0002 and the seven TestComputePercentageVariations cases pin the algorithm behaviour, including baseline selection, row dropping and NaN propagation. Residual risk: Low.

**\[RISK-RVC-P26.0003\]**

Linked to: **\[REQ-RVC-P26.0003\]**

**Risk Name: Incorrect Input Selection or Output Overwrite**

Risk: An unintended file may be processed, or an intended file skipped, due to the file-extension filter operator precedence (endswith(".xlsx") or endswith(".xls") and "\_p" not in file), which applies the "\_p" exclusion only to .xls files; in addition, re-running the batch over a populated output tree can overwrite prior results without warning, and configured thresholds that are not consumed by the logic may create a false expectation of threshold-based filtering. Severity: Low-Medium (wrong or duplicated output). Probability: Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0003 defines the intended iteration and exclusion scope; SPEC-RVC-P26.0003 with test\_excluded\_sheets\_produce\_no\_output, and SPEC-RVC-P26.0004 with TestCleanFilename, verify sheet exclusion and safe naming. Residual risk: Low-Medium.

**\[RISK-RVC-P26.0004\]**

Linked to: **\[REQ-RVC-P26.0004\]**

**Silent Visit Skip or Metadata Misattribution**

Risk: A worksheet whose structure deviates from the expected export layout may be silently discarded (fewer than three rows) or produce mis-attributed metadata; if the “Patient ID”, “Visit ID” or “Visit Date” columns are absent or relocated, the first-row lookup raises a KeyError that aborts the batch, or associates measurements with the wrong visit. Because the skip is reported only on the console, an operator may not notice that a visit is missing from the consolidated output. Severity: Medium (missing or misattributed non-diagnostic data, offline module, no patient exposure). Probability: Low-Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0005 fixes the ingestion contract and skip rule; SPEC-RVC-P26.0005 with TestRunExported.test\_short\_sheet\_skipped\_without\_error and test\_metadata\_columns\_populated verify controlled skipping and correct metadata extraction. Residual risk: Low-Medium.

**\[RISK-RVC-P26.0005\]**

Linked to: **\[REQ-RVC-P26.0005\]**

**Data Loss through Coercion and Sentinel Normalization**

Risk: The blanket conversion of zero, None and pd.NA to NaN, combined with to\_numeric(errors=“coerce”), may silently discard legitimate readings — a true zero measurement or a value stored in an unexpected textual format is converted to missing data and excluded from both the baseline selection and the output, without any warning to the operator. Severity: Medium (loss of otherwise valid non-diagnostic data). Probability: Low. Initial risk: Medium. Mitigation: REQ-RVC-P26.0005 defines the normalization contract; SPEC-RVC-P26.0006 with test\_string\_values\_converted\_to\_numeric, test\_column\_with\_no\_positive\_values\_skipped and test\_nan\_in\_data\_propagates\_to\_output pin the coercion and NaN-propagation behaviour. Residual risk: Low.

**\[RISK-RVC-P26.0006\]**

Linked to: **\[REQ-RVC-P26.0006\]**

**Output Overwrite, Schema Drift and Plaintext PII Exposure**

Risk: Re-running the component overwrites the two global CSV files in place, without versioning, so a partial or erroneous batch can silently replace a valid prior output. Concatenating visits with heterogeneous acquisition-point columns yields sparse rows that may be misread downstream. In addition, the CSV outputs store visit metadata (patient\_id, visit\_date) in plaintext, with no encryption at rest applied by this component. Severity: Low-Medium (wrong or overwritten output; PII confidentiality handled by the downstream storage layer). Probability: Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0006 fixes the output schema and Base-row policy; SPEC-RVC-P26.0007 with the seven TestRunExported schema and value cases verify the exact column layout and correctness. Encryption at rest (REQ-G-P26.0073) is provided by the downstream storage layer and is treated as out of scope for this offline computation module. Residual risk: Low-Medium.

**\[RISK-RVC-P26.0007\]**

Linked to: **\[REQ-RVC-P26.0007\]**

**δ Misinterpretation / Zero-Ambiguity**

Description: δ uses the minimum strictly-positive value (not the first reading), so an artefactual low value can inflate δ; and δ \= 0 is emitted both for genuinely stable points and for points with insufficient signal (fewer than two strictly-positive values), which a reader may conflate. Severity: Medium (misleading non-diagnostic indicator). Probability: Low. Initial risk: Medium. Mitigation: REQ-RVC-P26.0007 and SPEC-RVC-P26.0008 fix the δ definition and the zero-return contract; the ten TestComputeColumnOscillation cases pin the edge behaviour (zeros, negatives, NaN, single/empty/identical series). Residual risk: Low.

**\[RISK-RVC-P26.0008\]**

Linked to: **\[REQ-RVC-P26.0008\]**

**Uncontrolled Input Selection & Hardcoded Paths**

Description: The oscillation pipeline auto-selects the single CSV in a hardcoded data/input path and writes to a hardcoded data/output path; it does not read config.xml, contradicting the RVC configuration principle (REQ-RVC-P26.0001, no hardcoded processing paths). A wrong file may be processed, or a valid output silently overwritten on re-run. Severity: Low-Medium (wrong or duplicated output; offline module, no patient exposure). Probability: Medium. Initial risk: Medium. Mitigation: find\_input\_file() raises FileNotFoundError / ValueError on zero or multiple inputs (TestFindInputFile). Open finding: externalise the input/output locations to config.xml for consistency with REQ-RVC-P26.0001. Residual risk: Medium (until paths are externalised).

**\[RISK-RVC-P26.0009\]**

Linked to: **\[REQ-RVC-P26.0009\]**

**Aggregation Masking**

Description: Median-by-point aggregation over a right-skewed, zero-inflated δ distribution can mask sub-population variation; a zero median may hide relevant spread present at individual visits and be misread as a stable point. Severity: Low-Medium (potential misreading of a non-diagnostic population indicator). Probability: Low. Initial risk: Low-Medium. Mitigation: the median is chosen deliberately over the mean to resist right-skew and zero inflation; SPEC-RVC-P26.0010 and TestComputeMedianByPoint pin the aggregation and ordering. Residual risk: Low.

**\[RISK-RVC-P26.0010\]**

Linked to: **\[REQ-RVC-P26.0010\]**

**Non-Diagnostic-Language Violation & Report Toolchain Dependency**

Description: The current LaTeX report text uses clinical/diagnostic phrasing (e.g. "a meaningful clinical signal", "clinically stable") which conflicts with the non-diagnostic-language control for this Class I device (ref.5, REQ-G-P26.0022 / REQ-G-P26.0028); separately, PDF output depends on an external pdflatex toolchain that is not covered by the unit tests, so a compilation failure is surfaced only as a runtime warning. Severity: Medium (regulatory — Intended-Purpose compliance). Probability: Medium. Initial risk: Medium. Mitigation: REQ-RVC-P26.0010 mandates exclusively non-diagnostic language in the report output. Open findings: (1) revise the report wording in generate\_report.py to remove clinical/diagnostic terms; (2) add an end-to-end report smoke test covering pdflatex compilation. Residual risk: Medium (until the report wording is corrected).

9. # **Parameters**

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

10. # **Document Governance**

    1. ## **Revision List & Notes** 

| Revisision  | Date | Approved By \-  Name Acronymus | Notes |
| :---- | :---- | :---- | :---- |
| 00.02 |  |  |  |
| 00.01 | \#2026m08d31 | \[IR\] | This revision extends the document to cover the downstream oscillation-analysis pipeline implemented in the 'oscillations' sub-module of the component, which consumes the consolidated percentage-variation output produced by the core Raw Variation Computation and derives per-visit and population-level oscillation indicators together with an automated summary report. Added the oscillation-analysis pipeline (oscillations sub-module): SR REQ-RVC-P26.0007-0010, TS SPEC-RVC-P26.0008-0012, and RISK-RVC-P26.0007-0010. |
| 00.00 | \#2026m08d03 | \[IR\] | First edition. SR, TS and Risk Analysis populated from the implemented source code (raw\_variation.py, config.xml) and verified against tests/test\_raw\_variation.py. |

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

