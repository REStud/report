clear all
here
local here = r(here)

use "`here'data/git-events.dta", clear

bysort MS (numeric_date): generate t = _n
xtset MS t

generate spell = D.numeric_date
bysort MS (t): generate byte at_editor = (branch[_n-1] == branch[_n] ) | (branch[_n-1] == "author")

xtset MS t
generate byte change = L.at_editor != at_editor
bysort MS (t): generate byte spell_id = sum(change)

* count of packages in pipeline
egen last_commit = max(t), by(MS)

codebook MS
save "`here'temp/git-events-processed.dta", replace

rename accepted_year year
preserve
    collapse (sum) spell, by(MS year spell_id at_editor)
    drop if spell_id == 1
    replace spell_id = int((spell_id - 1)/2)

    reshape wide spell, i(MS spell_id year) j(at_editor)
    rename spell_id revision
    rename spell0 time_at_author
    rename spell1 time_at_editor

    egen max_revision = max(revision), by(MS)
    save "`here'temp/collapsed_year.dta", replace
restore

keep if year == 2024

collapse (sum) spell, by(MS accepted_at spell_id at_editor)
drop if spell_id == 1
replace spell_id = int((spell_id - 1)/2)

reshape wide spell, i(MS spell_id) j(at_editor)
rename spell_id revision
rename spell0 time_at_author
rename spell1 time_at_editor

egen max_revision = max(revision), by(MS)
save "`here'temp/collapsed_accepted_at.dta", replace


local opt width(7) start(0) frequency graphregion(color(white))

summarize time_at_editor if revision==0, detail
summarize time_at_editor if revision>=1, detail
summarize time_at_author, detail
twoway (histogram time_at_editor if revision==0, `opt' color(blue%30)) (histogram time_at_editor if revision>=1, `opt' color(red%30)), xtitle(Days at editor) legend(order(1 "First submission" 2 "Revision"))
graph export "`here'output/time_at_editor.png", replace width(800)

tabulate max_revision if revision == 0
histogram max_revision if revision == 0, color(blue%30) discrete start(0) frequency xtitle(Accepted revision) graphregion(color(white))
graph export "`here'output/revision.png", replace width(800)
