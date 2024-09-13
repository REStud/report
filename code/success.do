use "temp/zenodo.dta", clear
merge 1:1 MS using "temp/commands.dta", keep(match master) nogenerate
merge 1:1 MS using "temp/issues.dta", keep(match) nogenerate

generate byte stata = !missing(n_lines)
poisson downloads_per_month stata DAS cite_data, robust