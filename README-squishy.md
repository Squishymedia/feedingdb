FEED: a database of mammalian feeding behaviors
====

Getting started with Vagrant
----

Ensure you have VirtualBox, `vagrant` and `vagrant-triggers` installed.

0. Download and install VirtualBox: https://www.virtualbox.org/wiki/Downloads
1. Download and install `vagrant`: https://www.vagrantup.com/downloads.html
2. Run: `vagrant plugin install vagrant-triggers`

Now you can bring up the vagrant box for FEED: Anywhere in this repository, run: `vagrant up`.

Starting with a prod DB dump (for dev use)
----

To begin working with a DB dump from prod, there a few things you have to do to bring it into the new world.

First, load the DB dump. Use `vagrant ssh` to log into the box. Then, assuming the database `feeddb` is set up with a user named `feeddb`, restore the database from a file called `feed`:

```
pg_restore -h localhost -d feeddb -O -U feeddb feed
```

Enter `feeddb` when prompted for a password. You will see errors like this; it is OK:

```
GRANT ALL ON TABLE feed_trial T...
pg_restore: [archiver (db)] Error from TOC entry 2667; 0 0 ACL feed_trial_id_seq feeding_app
pg_restore: [archiver (db)] could not execute query: ERROR:  role "feeding_app" does not exist
    Command was: REVOKE ALL ON SEQUENCE feed_trial_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE feed_trial_id_seq FROM feeding_app;
GRANT ALL O...
WARNING: errors ignored on restore: 75
```

If instead you see several hundred errors, something else has gone wrong.

Next, run all the migrations and load OWL terms from fixtures:

```
./manage.py migrate feed
```

Now you can load correspondence CSVs:

```
./manage.py loadcorrespondence b ../data/behavior_correspondence.csv
./manage.py loadcorrespondence m ../data/al_muscles_correspondence.csv
```

See `data/README.md` for more information about the OWL terms and correspondences.

Next, load approval options.

```
./manage.py loaddata feeddb/feed/fixtures/approval_type.yaml
```

Then, load the schema and data into Solr:

`sudo feeddb-refresh-solr`

Finally, create a super user with access to edit everything.

`./manage.py createsuperuser`


Loading data from ontology
----

See `data/README.md` for information about loading ontology data into Django.

Servers
----

 * Dev: (in office)
   * http://dev-feed.sqm.private/
   * Superuser: `admin` / `admin`
   * Shell: `ssh -p 22421 dev-feed.sqm.private` and `./manage.py ...`
 * Vagrant: 1.2+
 * Vagrantfile: From `webdev-vagrant` as of June 2014

Notable URLs:

 * http://dev-feed.sqm.private/search/?q=pig -- sample search

Setting up a dev server or vagrant box
====

The puppet manifests applied by `vagrant provision` will do a lot of the work, but refreshing the solr schema is not yet automated.

You may also refer to the Deployment section below for manual instructions on setting up a server.

Refresh solr schema & index
====

This is now automated via puppet configuration. See `vagrant/manifests/default.pp` for details.

If you make changes to the schema or want to rebuild the index, run:

```
# while inside vagrant or on the dev server:
sudo feeddb-refresh-solr
# while outside vagrant:
vagrant ssh -c sudo feeddb-refresh-solr
```

If you know you haven't changed the index schema, you can do a simple index rebuild like this:

```
./manage.py rebuild_index --noinput
```

Deployment
====

The deployment process should be very similar to the setup for a dev environment. These are the major steps:

1. Ensure your server has an appropriate Python environment and is able to serve Django applications. These requirements are mostly similar to FEED1's requirements. See below for details.
2. Install and configure `solr`. See below for details.
3. Copy `settings.py.example` to `settings.py` and modify it to match your preferences and environment. Follow the instructions within those files. You may also want to read & revise `settings_common.py`. The former is specific to your deployment and is not tracked in git; the latter is tracked and contains configuration that should be common to all instances of FEED.
4. Load a FEED1 database into the location specified by `settings.py`. See above.
5. Run the migrations to update the database schema: `./manage.py migrate feed`
6. Load approval options. See above for details.
7. Load correspondences for behavior and muscles. See above for details.
8. Populate the `solr` search index. See below for details.
9. Configure a `cron` job to keep the search index up to date. See below for details.
9. Configure permissions on the upload directory to allow the Django app to write to the directory. On CentOS, this looks like: `chown -R apache <dir>` or `chgrp -R apache <dir> && find <dir> -type d | xargs chmod g+ws`
9. Check that all features are working as expected. Test thoroughly before opening up access to general users.

*Note*: It is assumed you are in the `src` directory for all commands described in this file.

Prerequisite packages
----

On CentOS 6 or RHEL 6, the following command will install the requisite packages for the deployment on Apache 2 using python virtualenv:

```
yum install -y postgresql-devel python-virtualenv python-pip python python-devel httpd
```

This document was prepared using python 2.6, Apache 2, and Postgres 8.4.20. Other versions may or may not work, but we do recommend using the versions maintained by your chosen distribution.

Python environment
----

It is generally recommended to use Python's `virtualenv` feature to isolate the environment of this application. The `virtualenv` utility creates an isolated python environment specific to FEED. If you are not using more than one python application on the server, you may safely omit use of `virtualenv`; packages will then be installed globally and the installation process will likely require superuser privileges.

The following commands will install the Python prerequisites for `feeddb`. If you don't use `virtualenv`, you can omit the first two lines of this recipe:

```
cd .../path/to/this/repo/src
virtualenv ~/feed-virtualenv
source ~/feed-virtualenv/bin/activate
pip install -r feeddb/requirements.txt
```

If you are using `virtualenv`, you will need to "activate" the environment before Django's `manage.py` will work. This only needs to be done once per terminal session:

```
source .../path/to/virtualenv/bin/activate
```

Web server (WSGI on Apache2)
----

Configure your web server to serve the FEED app. At Squishymedia, we use Apache2 with `mod_wsgi`. This is the VirtualHost configuration used for our development boxes: (the repo is checked out at `/server`; your checkout directory will likely differ)

```
<VirtualHost *:80>
  ServerName feeddb

  ## Vhost docroot
  DocumentRoot "/server/src/feeddb"

  ## Directories, there should at least be a declaration for /server/src/feeddb

  <Directory "/server/src/feeddb">
    Options Indexes FollowSymLinks MultiViews
    AllowOverride None
    Order allow,deny
    Allow from all
  </Directory>

  ## Logging
  ErrorLog "/var/log/httpd/feeddb_error.log"
  ServerSignature Off
  CustomLog "/var/log/httpd/feeddb_access.log" combined

  WSGIDaemonProcess wsgi display-name=%{GROUP} processes=2 threads=15
  WSGIProcessGroup wsgi
  WSGIScriptAlias / "/server/src/feeddb/wsgi.py"
</VirtualHost>
```

If you are using `virtualenv`, you must also specify the appropriate WSGIPythonHome configuration. At Squishymedia, we use the following snippet to configure `mod_wsgi`:

```
<IfModule mod_wsgi.c>
  # This is the path to the UNIX-domain socket for the WSGI server. This
  # differs between distributions; on CentOS the path is `/var/run/wsgi`.
  WSGISocketPrefix /var/run/wsgi
  
  # This path should match the argument given to `virtualenv` when creating the
  # virtual environment.
  WSGIPythonHome "/path/to/your/feeddb/virtualenv/"
</IfModule>
```

Note that this is merely an example; there are many other ways to deploy Django applications. See these links for starters:

https://docs.djangoproject.com/en/dev/howto/deployment/

https://docs.djangoproject.com/en/dev/howto/deployment/fastcgi/

http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html

Solr (installation)
----

Apache Solr is the search platform used in FEED2. We employ the "example" configuration that comes with `solr-3.6.2` and modify the indexing configuration using Haystack.  Due to compatibility issues, we use Solr 3 rather than the newer Solr 4.

First, ensure you have Java. On CentOS or RHEL, this will do it:

```
yum install -y java-1.7.0-openjdk
```

Next, download and install `solr` to the `/opt` directory with index configuration in `/etc/solr`. (some commands will need to be run as `root`)

```
mkdir -p /opt/solr
mkdir -p /etc/solr
mkdir -p /var/lib/solr
wget --output-document=/tmp/solr-3.6.2.tgz https://archive.apache.org/dist/lucene/solr/3.6.2/apache-solr-3.6.2.tgz
tar -xf /tmp/solr-3.6.2.tgz -C /opt/solr
ln -s /opt/solr/apache-solr-3.6.2 /opt/solr/current
cp -rf /opt/solr/current/example/solr/* /etc/solr/
```

Install an appropriate init script with the appropriate variable values. If you want to use the init script bundled in this repository, just run the following commands:

```
cp ../vagrant/modules/solr/files/solr /etc/init.d/solr
chown root /etc/init.d/solr
chmod 0755 /etc/init.d/solr

cat > /etc/default/solr-jetty <<EOT
JAVA_HOME=/usr/java/default # Path to Java
NO_START=0 # Start on boot
JETTY_HOST=0.0.0.0 # Listen to all hosts
JETTY_USER=solr # Run as this user
JETTY_HOME=/opt/solr/current/example
SOLR_HOME=/etc/solr
EOT
```

Start the `solr` service:

```
service solr start
```

Finally, make sure this init script is configured to run on boot:

```
chkconfig solr on
```

Solr (configuration)
----

The vagrant environment defined in this repo includes a script called `feeddb-refresh-solr` that will generate a solr schema based on the index model defined in `feeddb/feed/search_indexes.py` and rebuild the index. The script is simply a convenience wrapper around these three commands: (the first two must be run as root)

```
./manage.py build_solr_schema > /etc/solr/conf/schema.xml
service solr restart
./manage.py rebuild_index --noinput
```

As with all `./manage.py` commands, be sure you are using an appropriate Python environment (i.e. activate your virtualenv if you are using virtualenv).

Cron
----

The index needs a cron job to stay current. The command to run is:

```
./manage.py update_index --remove --age=X
```

where `X` is a number of hours. Content which has been modified in the last X hours will be re-indexed. Content which has been removed will be removed from the index.

The cronjob must specify all paths absolutely. If you are using a virtualenv, be sure to use the python binary in that virtualenv. For example, this job will update the index every half hour by re-indexing changes from the last hour:

```
0,30 * * * * /virtualenv/feeddb/bin/python /server/feed-django/src/manage.py update_index --remove --age 1
```


Hosting & Maintenance Notes
====

The app is mostly self-sufficient once it's set up. That said, all apps require some maintenance. Here are some things to keep track of during the app's lifetime:

 * Security updates for all packages listed in `feeddb/requirements.txt`.
 * Security updates for Solr 3.
 * Security updates for all system packages

For security information, we recommend that you subscribe to the security mailing lists for the projects in question.

It is also worthwhile to keep an eye on system performance through the following metrics:

 * Disk, memory, and CPU usage
 * Uptime & responsiveness, error rates
 * Real-life usage data -- a change in usage patterns across all users may indicate some change in the system which you might not detect otherwise.

Monitoring tools such as `monit` or services such as New Relic can help with these needs.
