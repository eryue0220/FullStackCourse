# Log Analysis - Udacity FSND Projects

## 0. Require

First of all, please make sure you have installed:

* [vagrant](https://www.vagrantup.com/downloads.html)
* [python 3.x](https://www.python.org/downloads/)
* [git](https://git-scm.com/downloads) 

Then clone this project in your computer via git.

## 1. How to Run

Change the directory into your project, assume it is like that:

```bash
$PATH/TO/fullstackcourse/vagrant
```

then download the data from the follow link:

* [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

And unzip the file. After that, executing the code as follow in your terminal:

```bash
vagrant up
```

when finish, you can run the code:

```bash
vagrant ssh
```

If no error, now you enter the develop environment, then execute the code:

```bash
psql -d news -f newsdata.sql
```

Finall, running the python code:

```python
python query.py
```

Waiting a moment, you will see the `result.txt` file which is the query result.

## 2. What does it do?

So doing a lot of work, but what is the requirements we need to do, or what does we really doing in the python code? We just do three things in the python code.

* 1. `Query the most top 3 articles from the database.`
* 2. `Query the most popular article author from the database.`
* 3. `Query the percentage of error request.`
