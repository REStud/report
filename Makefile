report.pdf: report.md downloads.png data/durations.dta
	pandoc $< -o $@
downloads.png: code/zenodo.do zenodo/zenodo_data.csv
	stata -b do $<
revision.png time_at_editor.png&: code/durations.do git_data/output/gitlog.dta
	stata -b do $<