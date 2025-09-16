clear all
here
local here = r(here)

import delimited "`here'github-data/data/raw/gitlog.csv", clear varn(1) case(preserve)
replace MS = "27827" if MS == "27827-1"
destring MS, force replace

* Julia datetime is in timestamps with seconds (2019-12-10T17:28:33Z)
replace date = substr(date, 1, 10)
gen numeric_date = date(date, "YMD")
scalar fy2021 = date("2020-09-01", "YMD")
scalar fy2022 = fy2021 + 365
scalar fy2023 = fy2022 + 365
scalar fy2024 = fy2023 + 365
* 2024 is a leap year	
scalar fy2025 = fy2024 + 366
scalar fy2026 = fy2025 + 365

* keep only packages with new branch naming
keep if inlist(branch, "author", "version1", "version2", "version3", "version4")
egen byte ever_accepted = max(tag=="accepted" | tag == "accept"), by(MS)

* keep backages accepted in 2021 fiscal year
egen submitted_at = min(numeric_date), by(MS)
egen accepted_at = max(cond(tag=="accepted" | tag == "accept", numeric_date, .)), by(MS)
scalar dbegin = fy2021
* 2024 is a leap year
scalar dend = fy2025

generate submitted_year = .
generate accepted_year = .

forvalues fy = 2021/2025 {
	local begindate = fy`fy'
	local enddate = fy`=`fy'+1' -1
    replace submitted_year = `fy' if inrange(submitted_at, `begindate', `enddate') & submitted_year == .
    replace accepted_year = `fy' if inrange(accepted_at, `begindate', `enddate') & accepted_year == .
}

egen ms_tag = tag(MS)
tabulate submitted_year if ms_tag == 1
tabulate accepted_year if ms_tag == 1

keep if ever_accepted & (accepted_at > dbegin) * (accepted_at <= dend)
save "`here'data/git-events.dta", replace

import delimited "`here'github-data/data/temp/issues.csv", clear varn(1) case(preserve)
*replace MS = "27827" if MS == "27827-1"
*destring MS, force replace
foreach var of varlist DAS cite_data confidential_data forward_slash requirements include_data macosx matlab_toolboxes readme relative_path save_output stata_packages {
	generate `var'b = 0 if `var' == "false"
	replace `var'b = 1 if `var' == "true"
	drop `var'
	ren `var'b `var'
}

save "`here'data/issues.dta", replace
