here
local here = r(here)

import delimited using "`here'/zenodo/zenodo_data.csv", clear

label variable unique_downloads "Downloads"
label variable unique_views "Views"

generate str lbl = ""
replace lbl = "Identifying Shocks via Time-Varying Volatility" if zenodoid == 4448256
replace lbl = "Property Rights, Land Misallocation and Agricultural Efficiency in China" if zenodoid == 4029206
replace lbl = "Trade and Domestic Production Networks" if zenodoid == 3997900
replace lbl = "The Macroeconomics of Microfinance" if zenodoid == 3959907
replace lbl = "Measuring the Incentive to Collude: The Vitamin Cartels, 1990–1999" if zenodoid == 5104830
replace lbl = "Stochastic Revealed Preferences with Measurement Error" if zenodoid == 4007866

foreach X of varlist unique_views unique_downloads {
    summarize `X', detail
}

scatter unique_downloads unique_views, mcolor(blue%30) legend(off) graphregion(color(white)) mlabel(lbl) mlabposition(6) xscale(range(0 600))
graph export "`here'/downloads.png", replace width(800)