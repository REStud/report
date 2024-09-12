here
local here = r(here)

clear 
tempfile zenodo
import delimited using "`here'zenodo/zenodo_data_2021.csv", clear
rename id zenodoid
keep zenodoid unique_views unique_downloads
rename unique_* *
rename downloads downloads2021
rename views views2021
save `zenodo', replace

tempfile zenodo22
import delimited using "`here'zenodo/zenodo_data_2022.csv", clear
rename id zenodoid
generate created_at = date(created,"YMD##")
keep zenodoid unique_views unique_downloads created_at
rename unique_* *
rename downloads downloads2022
rename views views2022
merge 1:1 zenodoid using `zenodo', nogenerate
save `zenodo22', replace

tempfile zenodo23
import delimited using "`here'zenodo/zenodo_data.csv", clear
rename id zenodoid
generate created_at = date(created,"YMD##")
keep zenodoid unique_views unique_downloads created_at
keep if created_at < 23260 // fy2023
rename unique_* *
rename downloads downloads2023
rename views views2023
duplicates drop zenodoid, force
merge 1:1 zenodoid using `zenodo22', nogenerate
save `zenodo23', replace

import delimited using "`here'zenodo/zenodo_data.csv", clear
rename id zenodoid
generate created_at = date(created,"YMD##")
generate updated_at = date(update_time,"YMD##")

format created_at %tdCCYY-NN-DD
format updated_at %tdCCYY-NN-DD

keep zenodoid unique_views unique_downloads created_at updated_at
rename unique_* *

sort zenodoid updated_at
by zenodoid (updated_at): generate update = _n
xtset zenodoid update
generate spell_length = updated_at - L.updated_at
generate new_downloads = downloads - L.downloads
generate new_views = views - L.views
generate days_since_upload = updated_at - created_at
generate months_since_upload = int(days_since_upload/30)

drop if spell_length < 20 | missing(spell_length)
generate downloads_per_month = new_downloads / (spell_length/30)

keep if days_since_upload > 180
summarize downloads_per_month, detail

collapse (mean) downloads_per_month, by(zenodoid)

save "`here'temp/zenodo.dta", replace

