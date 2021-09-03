here
local here = r(here)

import delimited using "`here'/trello_json/table31aug21.csv", clear
rename list_before from_list
rename list_after to_list

* read MS number
generate ms_number = real(ustrregexs(0)) if ustrregexm(name, "([0-9]){5}") 

* convert date string to datetime
generate double timestamp = date(date, "YMD#")
format timestamp %tdCCYY-NN-DD

* keep list moves and first action only
keep if action_id == 0 | !missing(from_list, to_list)
egen byte ever_accepted = max(to_list == "Editor accepted"), by(ms_number)

* group actions
egen action_number = rank(action_id), by(ms_number) unique
xtset ms_number action_number
* time spent in "from" list before moving it to "to" list
* FIXME: some cards are created in "Author submitted", some are moved there. The former will have . for duration
generate duration = datediff(L.timestamp, timestamp, "day")
* round #: how many times have the card moved out from "Author submitted"?
bysort ms_number (action_number): generate round_number = sum((from_list == "Author submitted"))
tabulate round_number, missing
* FIXME: move to analyze.do
tabulate round_number if to_list == "Editor accepted"

generate byte at_editor = 1 if inlist(from_list, "Author submitted", "At team", "At editor", "WIP", "Revised")
replace at_editor = 0 if inlist(from_list, "At author")
tabulate at_editor, missing

* merge different lists at editor
drop if round_number == 0 | missing(at_editor)
replace round_number = 3 if round_number > 3
collapse (sum) duration, by(ms_number ever_accepted round_number at_editor)
reshape wide duration, i(ms_number round_number) j(at_editor)
reshape long
mvencode duration, mv(0) override

table round_number at_editor if ever_accepted
table round_number at_editor if ever_accepted, statistic(mean duration)
save "`here'/data/durations.dta", replace

collapse (sum) duration, by(ms_number ever_accepted at_editor)
table at_editor if ever_accepted, statistic(mean duration)
