-----------------------------------------------------------------------------------------------------------
For deplotment:

uvicorn main:app --reload
is only intended for development. Here's the full breakdown:

🛠️ --reload (Development Mode)
Automatically reloads the server when you change the code.
Slower performance.
Not secure: it exposes more internals and is not hardened.
Good for local testing, debugging, and development.

🚀 Production Mode (No --reload)
In production, you should:
Disable --reload.
Run Uvicorn behind a production-ready web server like Gunicorn or Uvicorn with workers.

✅ Recommended production command:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Or, with Gunicorn:
gunicorn -k uvicorn.workers.UvicornWorker main:app --workers 4

🔒 Why?
Production mode is faster and more stable.
It doesn’t reload on every change.
It’s meant to handle multiple requests with worker processes.
You can also add:
HTTPS
Reverse proxy (Nginx)
Logging
Error monitoring

✅ Summary:
| Mode                | Command                                                          | Use Case                |
| ------------------- | ---------------------------------------------------------------- | ----------------------- |
| Development         | `uvicorn main:app --reload`                                      | Local coding/testing    |
| Production          | `uvicorn main:app --workers 4`                                   | Deploy to internet      |
| Production (robust) | `gunicorn -k uvicorn.workers.UvicornWorker main:app --workers 4` | For serious deployments |

------------------------------------------------------------------------------------------------------------------------------------

Influxdb
    User: bernardoantonio
    Password: influxdb1#
    API token: 4Up32I3Xg5xU3X3X5c_T5ksBBolkOxtcn-6VC4d0XpX0kG1Hq90pprEfRShSGOJ_pA70to9jzb8baZp_ISC8yA==
    organization: test
    bucket: test

    In myproject:
        pip install influxdb-client
        Create influxdb_conn.py

Grafna
    User: admin
    Password: admin

What I did today:
    Sensor -> Python script -> InfluxDB -> Grafana -> Live Dashboard

    Step 1:
        Run images of Influxdb and Grafana:
            docker run -d --name influxdb -p 8086:8086 -v influxdb-data:/var/lib/influxdb2 influxdb:2.7
            docker run -d --name=grafana -p 3000:3000 grafana/grafana

    Step 2:
        Configure InfluxDB:
            Set user and password, Organization and Bucket. Organization and Bucket will be used on python script.
            InfluxDB will give us an API token.
        To enter to Grafana:
            User and password are: admin.

    Step 3:
        Connect Grafana to InfluxDB:
            Go to Data Sources -> Add data source -> InfluxDB
            Fill in:
                Url: http://host.docker.internal:8'86 (Windows/Mac).
                http://localhost:8086 (Linux).
                Organization, Bucket and Token.
                Save&Test

    Step 4: 
        Send data from a Python Script.
            pip install influxdb-client
            (See influxdb_conn.py).
    
    Step 5:
        Build the Dashboard in Grafana:
            Go to Grafana -> Dashboards -> New Dashboard
            Customize the chart.
            Make the query.
            

