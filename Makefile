report.pdf: report.md downloads.png data/durations.dta
	pandoc $< -o $@
downloads.png: code/zenodo.do zenodo/zenodo_data.csv
	stata -b do $<
data/durations.dta: code/durations.do trello_json/table31aug21.csv
	stata -b do $<