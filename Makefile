output/report.pdf: output/report.md output/downloads.png output/downloads_histogram.png output/revision.png output/time_at_editor.png output/main_issues.png
	pandoc $< -o $@
output/main_issues.png: code/issues.do data/git-events.dta data/issues.dta
	stata -b do $<
output/downloads.png output/downloads_histogram.png&: code/zenodo.do zenodo/zenodo_data_2022.csv zenodo/zenodo_data_2021.csv
	stata -b do $<
output/revision.png output/time_at_editor.png&: code/durations.do data/git-events.dta
	stata -b do $<
zenodo/zenodo_data_2022.csv: zenodo/zenodo_pull.py
	cd zenodo; python3 zenodo_pull.py
data/git-events.dta data/issues.dta: code/github.do github-data/output/gitlog.csv github-data/output/report-labs.csv
	stata -b do $<