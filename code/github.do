clear all
here
local here = r(here)

use "`here'git_data/output/gitlog.dta", clear
replace MS = "27827" if MS == "27827-1"
destring MS, force replace

* keep only packages with new branch naming
keep if inlist(branch_imputed, "author", "version1", "version2", "version3", "version4")
egen byte ever_accepted = max(tag=="accepted"), by(MS)

* keep backages accepted in 2021 fiscal year
egen submitted_at = min(numeric_date), by(MS)
egen accepted_at = max(cond(tag=="accepted", numeric_date, .)), by(MS)
scalar dbegin = 1630495609 - 13.4*3600
scalar dend = dbegin + 2 * 365 * 24 * 3600 // 2 is the year factor here

keep if ever_accepted & (accepted_at > dbegin) * (accepted_at <= dend)
save "`here'data/git-events.dta", replace

use "`here'git_data/output/report_labs.dta", clear
replace MS = "27827" if MS == "27827-1"
destring MS, force replace

local vars cite_data DAS confidential_data save_output relative_path include_data stata_packages matlab_toolboxes requirements
foreach X in `vars' {
    generate byte `X' = 0
    forvalues j=1/7 {
        replace `X' = 1 if lab`j' == "`X'"
    }
}
drop lab?
save "`here'data/issues.dta", replace
