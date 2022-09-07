here
local here = r(here)

clear 
tempfile zenodo
import delimited using "`here'/zenodo/zenodo_data_2021.csv", clear
rename id zenodoid
keep zenodoid unique_views unique_downloads
rename unique_* *
rename downloads downloads2021
rename views views2021
save `zenodo', replace

import delimited using "`here'/zenodo/zenodo_data_2022.csv", clear
rename id zenodoid
generate created_at = date(created,"YMD##")
keep zenodoid unique_views unique_downloads created_at
rename unique_* *
rename downloads downloads2022
rename views views2022
merge 1:1 zenodoid using `zenodo', nogenerate

reshape long views downloads, i(zenodoid) j(year)
generate stats_at = date("2021-09-14","YMD##") if year == 2021
replace stats_at = date("2022-09-07","YMD##") if year == 2022

format created_at %tdCCYY-NN-DD
format stats_at %tdCCYY-NN-DD

generate since = round((stats_at - created_at)/30)
drop if missing(downloads) & year == 2021
generate downloads_per_month = downloads / since

keep zenodo year since downloads downloads_per_month
reshape wide since downloads downloads_per_month, i(zenodoid) j(year)

generate str lbl = ""
replace lbl = "Geography and Agricultural Productivity" if zenodoid == 5259883
replace lbl = "Quasi-Experimental Shift-Share Research Designs" if zenodoid == 4619197
replace lbl = "Identifying Shocks via Time-Varying Volatility" if zenodoid == 4448256
replace lbl = "Skill-Biased Structural Change" if zenodoid == 4773516
replace lbl = "Trade and Domestic Production Networks" if zenodoid == 3997900
replace lbl = "Measuring the Incentive to Collude" if zenodoid == 5104830

scatter downloads_per_month2022 downloads_per_month2021, mcolor(blue%30) legend(off) graphregion(color(white)) mlabel(lbl) mlabposition(6) xtitle(Last year) ytitle(This year)
graph export "`here'/downloads.png", replace width(800)

histogram downloads_per_month2022, color(blue%30) legend(off) graphregion(color(white)) frequency xtitle(Downloads per month)
graph export "`here'/downloads_histogram.png", replace width(800)

reshape long
summarize downloads_per_month if year==2022, detail

