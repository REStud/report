# Created by: Gergely Attila Kiss
# email: kiss.gergely.attila17@gmail.com
# Date: 23 Aug 2023
# 

gh repo list restud-replication-packages -L 1000 --json 'name,sshUrl,createdAt' > temp/tempfile
cat temp/tempfile |jq '.[]| [.name, .sshUrl, .createdAt]| @csv'|tr -d \\\\ | tr -d '\"' > temp/gh_list.csv
rm temp/tempfile