report.pdf: report.md downloads.png downloads_histogram.png revision.png time_at_editor.png main_issues.png
	pandoc $< -o $@
main_issues.png: code/issues.do data/git-events.dta data/issues.dta
	stata -b do $<
downloads.png downloads_histogram.png&: code/zenodo.do zenodo/zenodo_data_2022.csv zenodo/zenodo_data_2021.csv
	stata -b do $<
revision.png time_at_editor.png&: code/durations.do data/git-events.dta
	stata -b do $<
zenodo/zenodo_data_2022.csv: zenodo/zenodo_pull.py
	cd zenodo; python3 zenodo_pull.py
data/git-events.dta data/issues.dta: code/github.do git_data/output/gitlog.dta git_data/output/report_labs.dta
	stata -b do $<