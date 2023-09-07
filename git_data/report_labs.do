import delimited "output/report_labs.csv", varn(nonames) clear
rename (v1-v8) (MS lab1 lab2 lab3 lab4 lab5 lab6 lab7)
replace lab1 = "DAS" if lab1 == "DAS,"
save "output/report_labs.dta", replace
