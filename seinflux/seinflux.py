import time
import json
import click

from datetime import datetime
from subprocess import Popen, PIPE
from influxdb import InfluxDBClient


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


@click.command()
@click.option("--ihost", default="192.168.1.1", help="SolarEdge Inverter IP address")
@click.option("--iport", default="1502", help="SolarEdge Inverter ModBus TCP port")
@click.option("--dbhost", default="localhost", help="InfluxDB Host")
@click.option("--dbport", default=8086, help="InfluxDB Port")
@click.option("--dbname", default="solar", help="InfluxDB Database name")
@click.option(
    "--path",
    default="sunspec-status",
    help="sunspec-status perl script path",
)
@click.option("--sleep", default=5, help="Sleep time in seconds between polling the inverter")
def cli(ihost, iport, dbhost, dbport, dbname, path, sleep):
    """
    seinflux queries a SolarEdge inverter via Modbus over TCP and then enters data into an influxdb database. Rinse and
    repeat.
    """
    while True:  # run forever
        client = InfluxDBClient(host=dbhost, port=dbport)
        client.switch_database(dbname)

        process = Popen([path, "-m", "0", "-j", "--port", iport, ihost], stdout=PIPE)
        (output, err) = process.communicate()
        exit_code = process.wait()

        if exit_code == 0:
            data_points = create_body(json.loads(output))
            client.write_points(data_points)
        else:
            # log if there is an issue
            click.echo(f"Issue with running sunspec status: {err}")
        time.sleep(sleep)


if __name__ == "__main__":
    cli()
