use "temp/collapsed_year.dta", clear

label variable time_at_author "Days at author"
label variable time_at_editor "Days at editor"

histogram time_at_editor if revision==0, freq by(year) xtitle(Days at editor on first submission) ytitle(Number of packages)

* Export the graph
graph export "output/editor_time0.png", replace width(1000)

histogram time_at_editor if revision>0, freq by(year) xtitle(Days at editor on resubmission) ytitle(Number of packages)

* Export the graph
graph export "output/editor_time1.png", replace width(1000)

* report median time at editor over years
replace revision = 1 if revision > 1
collapse (mean) time_at_editor, by(year revision)

xtset revision year
xtline time_at_editor, title("Average time at editor over years") ytitle("Days") xtitle("Year") ylab(0(20)100) overlay legend(order(1 "First submission" 2 "Resubmission"))

* Export the graph
graph export "output/editor_time.png", replace width(1000)