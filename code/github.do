clear all
here
local here = r(here)

use "`here'/git_data/output/gitlog.dta", clear
replace MS = "27827" if MS == "27827-1"
destring MS, force replace

* Python datetime is in second, use days
replace numeric_date = int(numeric_date / 3600 / 24)
scalar fy2021 = int(1630447200 / 3600 / 24) - 365
scalar fy2022 = fy2021 + 365
scalar fy2023 = fy2022 + 365

* keep only packages with new branch naming
keep if inlist(branch_imputed, "author", "version1", "version2", "version3", "version4")
egen byte ever_accepted = max(tag=="accepted"), by(MS)

* keep backages accepted in 2021 fiscal year
egen submitted_at = min(numeric_date), by(MS)
egen accepted_at = max(cond(tag=="accepted", numeric_date, .)), by(MS)
scalar dbegin = fy2021
scalar dend = fy2023 + 365

generate submitted_year = .
generate accepted_year = .
forvalues fy = 2021/2023 {
    replace submitted_year = `fy' if inrange(submitted_at, fy`fy', fy`fy'+365) & submitted_year == .
    replace accepted_year = `fy' if inrange(accepted_at, fy`fy', fy`fy'+365) & accepted_year == .
}

egen ms_tag = tag(MS)
tabulate submitted_year if ms_tag == 1
tabulate accepted_year if ms_tag == 1

keep if ever_accepted & (accepted_at > dbegin) * (accepted_at <= dend)
save "`here'/data/git-events.dta", replace

use "`here'/git_data/output/report_labs.dta", clear
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
save "`here'/data/issues.dta", replace
