Tired with manage vhosts for your apache2? This script will do this automatically. You have to locale www dir in the home of your user.
Go to module directory, then:

If you want add a vhost:
```bash
python new-domain.py my-domain.test
```
Your site is under: ~/www/vhosts/my-domain.test
Restart your browser, put http://my-domain.test and voilà.


If you want to remove a vhost:
```bash
python del-domain.py my-domain.test
```
Your site is zipped in ~/www/vhosts/my-domain.test.zip


**installation**
git clone https://github.com/codecats/apache2-hosts

**additional information**
Testing enviroment Ubuntu 14.04 with apache 2.4
