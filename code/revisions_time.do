use "temp/collapsed_year.dta", clear

keep if revision == max_revision
collapse (count) n = MS, by(year max_revision)
rename max_revision revision
reshape wide n, i(year) j(revision)

egen n2plus = rowtotal(n2 n3 n4)

tsset year
tsline n0 n1 n2plus, title("Distribution of Package Revisions Over Time") ytitle("Number of packages") xtitle("Year") legend(order(1 "0 revisions" 2 "1 revision" 3 "2 or more revisions")) ylab(0(20)100)

* Export the graph
graph export "output/revisions_time.png", replace width(1000)