report.pdf: report.md downloads.png downloads_histogram.png revision.png time_at_editor.png
	pandoc $< -o $@
downloads.png downloads_histogram.png &: code/zenodo.do zenodo/zenodo_data_2022.csv zenodo/zenodo_data_2021.csv
	stata -b do $<
revision.png time_at_editor.png &: code/durations.do git_data/output/gitlog.dta
	stata -b do $<
zenodo/zenodo_data_2022.csv: zenodo/zenodo_pull.py
	cd zenodo; python3 zenodo_pull.py