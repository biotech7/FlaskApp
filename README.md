# FlaskApp
Server/App Info
* My static IP address is 52.59.100.171
* The port number I configured is 2200
* Username and password: grader, grader

Configurations in Steps
### Goals

- Install Apache and configure it to serve a Python mod_wsgi application.

- Install Flask
# Steps


1.  Install Apache.
 
    After updating the package index, install Apache.
    ```
    sudo apt-get update
    sudo apt-get install apache2
    ```


2.  Install and enable mod_wsgi.

    To install:
    ```
    sudo apt-get install libapache2-mod-wsgi python-dev
    ```

    To enable mod_wsgi:
    ```
    sudo a2enmod wsgi
    ```

3.  Create a directory for the Flask application.

    Move to the `/var/www` directory and create a directory for your application.
    ```
    cd /var/www
    sudo mkdir catalog
    ```

4.  Clone your Flask application into the new directory. 

    Move inside your app directory and [clone](/how-to/install-git-clone-repository.md) in your Flask application from Github. 
    ```
    cd catalog
    sudo git clone {your repository clone URL}
    ```

    Rename the directory created by git to `catalog`.
    ```
    sudo mv /{git-repository-name} FlaskApp
    ```

5.  Install Flask and SQLAlchemy inside a virtual environment.

    If pip is not installed, add it now. 
    ```
    sudo apt-get install python-pip
    ```

    Install *virtualenv*.
    ```
    sudo pip install virtualenv
    ```

    Create a virtual environment inside your `FlaskApp` directory.
    ```
    cd catalog
    sudo virtualenv venv
    ```

    Activate the virtual environment and install Flask and SQLAlchemyinside.
    ```
    source venv/bin/activate 
    sudo pip install Flask
    sudo pip install flask-sqlalchemy
    ```

6.  Configure files as needed and test if the installation was successful.
    
    Make sure your database conneciton Url matches the username and password you set up in [installing and configuring PostgreSQL to work with SQLAlchemy](how-to/install-postgres-and-configure.md).

    If your modules reference other files, you will need to alter filepaths.  The path to your FlaskApp directory will be: `/var/www/catalog/catalog`. 

    Test if the installation is successful and the app can run:
    ```
    sudo python __init__.py
    ```
    If it says `Running on http://0.0.0.0:5000/`, your installation was successful.

7. Configure and enable a new virtual host with Apache.

    Create a configuration file for Apache:
    ```
    sudo nano /etc/apache2/sites-available/catalog.conf
    ```

    And input the configuration:
    ```
    <VirtualHost *:80>
        ServerName 52.59.100.171
        ServerAdmin grader@52.59.100.171
        WSGIScriptAlias / /var/www/catalog/flaskapp.wsgi
        <Directory /var/www/catalog/catalog/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/catalog/catalog/static
        <Directory /var/www/catalog/catalog/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    ```

    Enable the virtual host.
    ```
    sudo a2ensite catalog.conf
     ```
    Change default site to point to app
    ```
    sudo nano /etc/apache2/sites-available/000.default.conf
    change DocumentRoot /var/www/html to  /var/www/catalog/catalog/templates
    paste 'WSGIScriptAlias / /var/www/catalog/catalog.wsgi' without the quotes just below it. save and exit from nano
    ```
    
   

8. Create a .wsgi file.
    
    Apache uses a .wsgi file to serve the Flask application. Create the file:
    ```
    cd /var/www/catalog
    sudo nano catalog.wsgi
    ```

    Input the configuration:
    ```
    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/catalog/")

    from catalog import app as application
    application.secret_key = {Add your secret key}
    ```

9.  Install and configure PostgreSQL
    ```
    1. Install some necessary Python packages for working with PostgreSQL: $ sudo apt-get install libpq-dev python-dev.
    2. Install PostgreSQL: $ sudo apt-get install postgresql postgresql-contrib
    3. PostgreSQL automatically creates a new user 'postgres' during its installation. So we can connect to the database by  using postgres username with: $ sudo -u postgres psql
    4. Create a new user called 'catalog' with his password: # CREATE USER catalog WITH PASSWORD 'catalog';
    5. Give catalog user the CREATEDB permission: # ALTER USER catalog CREATEDB;
    6. Create the 'catalog' database owned by catalog user: # CREATE DATABASE catalog WITH OWNER catalog;
    7. Connect to the database: # \c catalog
    8. Revoke all the rights: # REVOKE ALL ON SCHEMA public FROM public;
    9. Lock down the permissions to only let catalog role create tables: # GRANT ALL ON SCHEMA public TO catalog;
    10.Log out from PostgreSQL: # \q. Then return to the grader user: $ exit.
    11.Edit the db_seed.py and database_setup.py file:
    12.Change engine = create_engine('sqlite:///category.db') to engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
    13.Remote connections to PostgreSQL should already be blocked. Double check by opening the config file: $ sudo nano /etc/postgresql/9.5/main/pg_hba.conf Source: DigitalOcean.
    ```
10. Restart Apache.
    
    ```
    sudo service apache2 restart
    ```
    Open your browser and navigate to the domain name or IP address you entered in the `catalog.conf` configuration file. If all is well, you will see your app.

#### References & Credits

[Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)</br>
[golgtwins/Udacity-P7-Linux-Server-Configuration](https://libraries.io/github/golgtwins/Udacity-P7-Linux-Server-Configuration)</br>
[Internal Server Error: Target WSGI script cannot be loaded as Python module AND IOError: [Errno 2] No such file or directory: 'client_secrets.json'
](https://stackoverflow.com/questions/31168606/internal-server-error-target-wsgi-script-cannot-be-loaded-as-python-module-and/33223884)


