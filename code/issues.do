clear all
here
local here = r(here)

tempfile git
use "`here'data/git-events.dta", clear
keep MS
duplicates drop
save `git', replace

use "`here'data/issues.dta", clear
merge 1:1 MS using `git', keep(match using) nogenerate

drop MS
unab vars: _all
collapse (mean) `vars'

rename * V*
generate i = 1
reshape long V, i(i) j(issue) string
replace V = 100*V

generate issue_num = 3 if issue=="cite_data"
replace issue_num = 2 if issue=="DAS"
replace issue_num = 1 if issue=="save_output"

label define IV 1 "Save output" 2 "Data Availability Statement" 3 "Cite data"
label values issue_num IV

local opt graphregion(color(white)) horizontal ylab(#3, value) xtitle(Percent) ytitle("")
twoway dropline V issue_num, `opt' color(blue)
graph export "`here'main_issues.png", replace width(800)