# Catalog for newsdata

### Pre-install

1. virtual machine based on the udacity course

2. vagrant environment 

3. newsdata.sql downloaded and  news successfully created

To create user and table use command
```
psql -d news -f newsdata.sql
```

4. python 2.7 installed correct in vm


### How to use

1. unzip the newsdata.zip under /vagrant directory



2. access the newsdata directory

```
vagrant@vagrant:/vagrant$ cd newsdata/
```

3. run newsdata.py

use command
```
vagrant@vagrant:/vagrant/catalog$ python newsdata.py
```

or if you chmod 775 to newsdata.py

```
vagrant@vagrant:/vagrant/newsdata$ ./newsdata.py
```

4. open outputfile out.txt  

Then you can find the answer to question


### Created Views

+ popular_article : title, count number of the reviews, author

+ error_date: date, sum of error num in this date 

+ total_date: date, sum of log num in this date


### More

All code have been formated by pep8 and added comment.

