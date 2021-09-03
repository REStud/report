here
local here = r(here)

import delimited using "`here'/trello_json/table31aug21.csv", clear

* read MS number

* convert date string to datetime

* group actions
egen card_id = group(card)
egen action_number = rank(-timestamp), by(card)
xtset card action_number
* time spent in "from" list before moving it to "to" list
* FIXME: some cards are created in "Author submitted", some are moved there. The former will have . for duration
generate duration = timestamp - L.timestamp
* round #: how many times have the card moved out from "Author submitted"?
bysort card (action_number): generate round_number = sum((from_list == "Author submitted"))
tabulate round_number, missing
* FIXME: move to analyze.do
tabulate round_number if to_list == "Editor accepted"

generate byte at_editor = 1 if inlist(from_list, "Author submitted", "At team", "At editor")
replace at_editor = 0 if inlist(from_list, "At author")
tabulate at_editor, missing

* merge different lists at editor
collapse (sum) duration, by(card round_number at_editor)

table round_number at_editor, statistic(mean duration)
save "`here'/data/durations.dta", replace