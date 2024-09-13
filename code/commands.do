import delimited "github-data/output/analysis-table.csv", clear varnames(1) case(preserve) encoding(UTF-8)

rename repo MS
destring MS, replace force
drop if missing(MS)

egen file_tag = tag(MS dofile)

collapse (count) n_lines = file_tag (sum) n_files = file_tag, by(MS)
save "temp/commands.dta", replace