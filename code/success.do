use "temp/zenodo.dta", clear
merge 1:1 MS using "temp/commands.dta", keep(match master) nogenerate
merge 1:1 MS using "temp/issues.dta", keep(match) nogenerate

generate byte stata = !missing(n_lines)
generate ln_n_lines = ln(n_lines)
generate ln_n_files = ln(n_files)

poisson downloads_per_month stata DAS cite_data, robust

poisson downloads_per_month ln_n_files ln_n_lines DAS cite_data if stata, robust