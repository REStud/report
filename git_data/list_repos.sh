#!/bin/bash
# Author: Sarav AK
# Email: hello@gritfy.com
# Created Date: 19 Aug 2021
# 
# Modified by: Gergely Attila Kiss
# email: kiss.gergely.attila17@gmail.com
# Date: 29 Aug 2022
# 

# For this you need to generate an API key token on github under settings/developer/Personal access tokens
USERNAME=`head -n1 temp/secrets`
TOKEN=`tail -n1 temp/secrets`


# No of reposoitories per page - Maximum Limit is 100
PERPAGE=200

# Org base URL
BASEURL="https://api.github.com/orgs/restud-replication-packages/repos"


# Calculating the Total Pages after enabling Pagination
TOTALPAGES=`curl -I -i -u ${USERNAME}:${TOKEN} -H "Accept: application/vnd.github.v3+json" -s ${BASEURL}\?per_page\=${PERPAGE} | grep -i link: 2>/dev/null|sed 's/link: //g'|awk -F',' -v  ORS='\n' '{ for (i = 1; i <= NF; i++) print $i }'|grep -i last|awk '{print $1}' | tr -d '\<\>' | tr '\?\&' ' '|awk '{print $3}'| tr -d '=;page'`
i=1

until [ $i -gt $TOTALPAGES ]
do
  result=`curl -s -u $USERNAME:$TOKEN -H 'Accept: application/vnd.github.v3+json' ${BASEURL}?per_page=${PERPAGE}\&page=${i} 2>&1`
  echo $result > temp/tempfile
  cat temp/tempfile|jq '.[]| [.name, .ssh_url, .clone_url]| @csv'|tr -d '\\"'
  ((i=$i+1))
done