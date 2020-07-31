import time
import click

from datetime import datetime
from subprocess import Popen, PIPE
import psycopg2


def get_timestamp():
    """Get timestamp now in ISO format"""
    return datetime.utcfromtimestamp(time.time()).isoformat()


def create_body(sunspec_dict):
    """
    Translate the sunspec-status output JSON into a format which can be used to insert into influxdb
    """
    time = get_timestamp()
    output = []
    for k, v in sunspec_dict.items():
        if k == "timestamp":
            pass
        else:
            point = {"measurement": "solaredge", "time": time, "fields": {k: v}}
            output.append(point)
    return output


def create_insert(csv_data):
    data_list = csv_data.split(",")
    sql = f"INSERT INTO solaredge (ts, status, ac_power, dc_power, total_production, ac_voltage, ac_current, dc_voltage, dc_current, temperature, exported_energy_m1, imporoted_energy_m1, exported_energy_m2, imported_energy_m2) VALUES ('{data_list[0]}','{data_list[1]}',{data_list[2]},{data_list[3]},{data_list[4]},{data_list[5]},{data_list[6]},{data_list[7]},{data_list[8]},{data_list[9]},{data_list[10]},{data_list[11]},{data_list[12]},{data_list[13]})"
    return sql


@click.command()
@click.option("--ihost", default="192.168.1.1", help="SolarEdge Inverter IP address")
@click.option("--iport", default="1502", help="SolarEdge Inverter ModBus TCP port")
@click.option("--dbhost", default="localhost", help="Postgres Host")
@click.option("--dbport", default=5432, help="Postgres Port")
@click.option("--dbname", default="solar", help="Postgres Database name")
@click.option("--dbuser", default="postgres", help="Postgres username")
@click.option(
    "--dbpass", default="postgres", help="Postgres password (change your password :D)"
)
@click.option(
    "--path", default="sunspec-status", help="sunspec-status perl script path",
)
@click.option(
    "--sleep", default=5, help="Sleep time in seconds between polling the inverter"
)
def cli(ihost, iport, dbhost, dbport, dbname, dbuser, dbpass, path, sleep):
    """
    seinflux queries a SolarEdge inverter via Modbus over TCP and then enters data into an postgres database. Rinse and
    repeat.
    """
    conn = psycopg2.connect(
            host=dbhost, port=dbport, dbname=dbname, user=dbuser, password=dbpass
        )
    while True:  # run forever
        cur = conn.cursor()
        process = Popen(
            [path, "-m", "0", "--port", iport, ihost], stdout=PIPE, encoding="utf-8"
        )
        (output, err) = process.communicate()
        exit_code = process.wait()

        if exit_code == 0:
            insert_str = create_insert(output[:-1])
            cur.execute(insert_str)
            conn.commit()
        else:
            # log if there is an issue
            click.echo(f"Issue with running sunspec status: {err}")
        time.sleep(sleep)


if __name__ == "__main__":
    cli()
