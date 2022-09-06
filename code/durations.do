clear all
here
local here = r(here)

use "`here'output/gitlog.dta", clear
replace MS = "27827" if MS == "27827-1"
destring MS, force replace

* keep only packages with new branch naming
keep if inlist(branch_imputed, "author", "version1", "version2", "version3", "version4")
egen byte ever_accepted = max(tag=="accepted"), by(MS)

bysort MS (numeric_date): generate t = _n
xtset MS t

generate spell = D.numeric_date/3600/24
bysort MS (t): generate byte at_editor = (branch_imputed[_n-1] == branch_imputed[_n] ) | (branch_imputed[_n-1] == "author")

xtset MS t
generate byte change = L.at_editor != at_editor
bysort MS (t): generate byte spell_id = sum(change)

collapse (sum) spell, by(MS ever_accepted spell_id at_editor)
drop if spell_id == 1
replace spell_id = int((spell_id - 1)/2)

reshape wide spell, i(MS spell_id) j(at_editor)
rename spell_id revision
rename spell0 time_at_author
rename spell1 time_at_editor

egen max_revision = max(revision), by(MS)

local opt width(7) start(0) frequency
twoway (histogram time_at_editor if ever_accepted & revision==0, `opt' color(blue%30)) (histogram time_at_editor if ever_accepted & revision>=1, `opt' color(red%30)), xtitle(Days at editor) legend(order(1 "First submission" 2 "Revision"))
graph export "`here'output/time_at_editor.png", replace width(800)

histogram max_revision if revision == 0 & ever_accepted, color(blue%30) discrete start(0) frequency xtitle(Accepted revision)
graph export "`here'output/revision.png", replace width(800)
