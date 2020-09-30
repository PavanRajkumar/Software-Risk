## Commands to extract commit info 

*From a github repository and convert it to a rudimentary CSV format*

 - echo "commit id,author,date,comment,changed files,lines added,lines deleted" > data.csv    		
    **[ initialising a csv file ]**
   
 - git log --since='last year'  --date=local --all --pretty="%x40%h%x2C%an%x2C%ad%x2C%x22%s%x22%x2C" --shortstat | tr "\n" " " | tr "@" "\n" >> data.csv     
 **[*extracts commit id, commit message, author, data, comment, files changedn, lines added, lines deleted* ]**

## To find buggy commits

 - git log -i --all --grep BUG --grep FIX --pretty=format:%h"
 - git --no-pager diff {commit}^ {commit} -U0 -- {fname}
 - git --no-pager blame -L{start},+{n} {commit}^ -- {fname}

## To get the latest commit

 - git log -1  --pretty="%x40%h%x2C%an%x2C%ad%x2C%x22%s%x22%x2C" --shortstat

## Formatting data cmd line
  
sed -i 's/ files changed//g' data1.csv  ...

## Commits per author
 - git shortlog -s -n 



