### INITILIALIZATION

1. Build config file via `my_conf` 

2. Initialize migration with the following commands:

   ```sh
   :: Ensure the database is created
   flask db init
   flask db migrate
   flask db upgrade
   ```

   

### DEPLOYING ON APACHE XAMPP

1. Download the `mod_wsgi` from https://www.lfd.uci.edu/~gohlke/pythonlibs/

   After that type the following command line:

   ```sh
   pip install <*.whl>
   ```

2. Extract `wsgi_module` with the command line below

   ```sh
   mod_wsgi-express module-config
   ```

   Paste the output to `httpd.conf` file in the last line

3. Paste the following script after the previous step

   ```sh
   <IfModule wsgi_module>
       Listen 5000
       <VirtualHost *:5000>
           ServerName 127.0.0.1
           WSGIScriptAlias / "/path/to/portfolio/run.wsgi"
           <Directory /path/to/portfolio>            
               Allow from all            
               Require all granted
           </Directory>
           WSGIApplicationGroup %{GLOBAL}
           
           ErrorLog "/path/to/portfolio/logs/error.log"
           CustomLog "/path/to/portfolio/access.log" common
       </VirtualHost>
   </IfModule>  
   ```

4. Restart the Apache service in the following steps

   **windows+R** --> type `services.msc` --> search `Apache24` --> restart

5. Go to Browser http://localhost:5000
