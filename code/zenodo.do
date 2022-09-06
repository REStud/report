here
local here = r(here)

clear 
tempfile zenodo
save `zenodo', emptyok replace
forvalues year = 2021/2022 {
    import delimited using "`here'/zenodo/zenodo_data_`year'.csv", clear
    rename id zenodoid
    generate year = `year'
    append using `zenodo'
    save `zenodo', replace
}

keep zenodoid year unique_views unique_downloads
rename unique_* *
reshape wide views downloads, i(zenodoid) j(year)

* uncumulate cumulated stats
foreach X in views downloads {
    replace `X'2022 = `X'2022 - `X'2021 if !missing(`X'2021)
}

generate str lbl = ""
replace lbl = "Identifying Shocks via Time-Varying Volatility" if zenodoid == 4448256
replace lbl = "Property Rights, Land Misallocation and Agricultural Efficiency in China" if zenodoid == 4029206
replace lbl = "Trade and Domestic Production Networks" if zenodoid == 3997900
replace lbl = "The Macroeconomics of Microfinance" if zenodoid == 3959907
replace lbl = "Measuring the Incentive to Collude: The Vitamin Cartels, 1990–1999" if zenodoid == 5104830
replace lbl = "Stochastic Revealed Preferences with Measurement Error" if zenodoid == 4007866

scatter downloads2022 downloads2021, mcolor(blue%30) legend(off) graphregion(color(white)) mlabel(lbl) mlabposition(6) xtitle(Downloads last year) ytitle(Downloads in current year)
graph export "`here'/downloads.png", replace width(800)

histogram downloads2022, color(blue%30) legend(off) graphregion(color(white)) frequency xtitle(Cumulated downloads)
graph export "`here'/downloads_histogram.png", replace width(800)

reshape long
summarize downloads, detail

