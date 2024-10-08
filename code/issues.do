clear all
here
local here = r(here)

tempfile git
use "`here'data/git-events.dta", clear
keep MS
duplicates drop
save `git', replace

use "`here'data/issues.dta", clear
duplicates drop MS, force
merge 1:1 MS using `git', keep(match using) nogenerate
save "`here'temp/issues.dta", replace

drop MS branch commit
unab vars: _all
collapse (mean) `vars'

rename * V*
generate i = 1
reshape long V, i(i) j(issue) string
replace V = 100*V

generate issue_num = 4 if issue=="cite_data"
replace issue_num = 3 if issue=="DAS"
replace issue_num = 2 if issue=="save_output"
replace issue_num = 1 if issue=="stata_packages"

label define IV 1 "Stata packages" 2 "Save output" 3 "DAS" 4 "Cite data"
label values issue_num IV

local opt graphregion(color(white)) horizontal ylab(#4, value) xtitle(Percent) ytitle("")
twoway dropline V issue_num, `opt' color(blue)
graph export "`here'output/main_issues.png", replace width(800)
