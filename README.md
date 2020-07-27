# solaredge-influx

Just me hacking around with my SolarEdge inverter and trying to graph some of the data using a bunch of different 
components.

# Base requirements

- https://github.com/tjko/sunspec-monitor (Perl SunSpec scraper)
    - There are some dependencies. I found using [cpan](https://www.cpan.org/modules/INSTALL.html) helpful to install
      them. The script is included in the `sunspec-monitor` folder as zip file.

- [influxdb](https://docs.influxdata.com/influxdb/v1.8/introduction/install/)
    - You will need to create an empty database. By default the package uses `solar`
    
- [grafana](https://grafana.com/docs/grafana/latest/)
    - You should be able to use any visualization tool, but I've used grafana since it integrated nicely
      with influxdb



# sunspec-monitor

Originally I wanted to use `pySunSpec` but I ran into issues with it. `sunspec-monitor` worked out of the box for me
and also provided output into a JSON format which I could easily ingest into Python and influxdb. I might circle back
and try to get it working with `pySunSpec` but for now the perl script is a dependency. :(

This is a perl script and has its own dependency on the `Device::Modbus::TCP` module. [cpan](https://www.cpan.org/modules/INSTALL.html)
seems to be the spot to get everything properly setup. If you are on Linux you should be covered with most modern distros.

Check to see if you have cpan installed via `cpan -v`:

```bash
# cpan -v
Loading internal logger. Log::Log4perl recommended for better logging
>(info): /usr/bin/cpan script version 1.67, CPAN.pm version 2.20
```

Then you can install `cpanminus`:

```bash
# cpan App::cpanminus
```

Once you have that done install the `Modbus:TCP` dependency:

```bash
# cpanm Device::Modbus::TCP
--> Working on Device::Modbus::TCP
Fetching http://www.cpan.org/authors/id/J/JF/JFRAIRE/Device-Modbus-TCP-0.026.tar.gz ... OK
Configuring Device-Modbus-TCP-0.026 ... OK
==> Found dependencies: Device::Modbus, Role::Tiny, Try::Tiny, Net::Server
--> Working on Device::Modbus
Fetching http://www.cpan.org/authors/id/J/JF/JFRAIRE/Device-Modbus-0.021.tar.gz ... OK
Configuring Device-Modbus-0.021 ... OK
==> Found dependencies: Try::Tiny
--> Working on Try::Tiny
Fetching http://www.cpan.org/authors/id/E/ET/ETHER/Try-Tiny-0.30.tar.gz ... OK
Configuring Try-Tiny-0.30 ... OK
Building and testing Try-Tiny-0.30 ... OK
Successfully installed Try-Tiny-0.30
Building and testing Device-Modbus-0.021 ... OK
Successfully installed Device-Modbus-0.021
--> Working on Role::Tiny
Fetching http://www.cpan.org/authors/id/H/HA/HAARG/Role-Tiny-2.001004.tar.gz ... OK
Configuring Role-Tiny-2.001004 ... OK
Building and testing Role-Tiny-2.001004 ... OK
Successfully installed Role-Tiny-2.001004
--> Working on Net::Server
Fetching http://www.cpan.org/authors/id/R/RH/RHANDOM/Net-Server-2.009.tar.gz ... OK
Configuring Net-Server-2.009 ... OK
Building and testing Net-Server-2.009 ... OK
Successfully installed Net-Server-2.009
Building and testing Device-Modbus-TCP-0.026 ... OK
Successfully installed Device-Modbus-TCP-0.026
5 distributions installed
```

You can now try the script in the zip against your inverter:

```bash
# ./sunspec-status -j --port 1502 -m 0 <Inverter IP>
{
	"timestamp": "2020-07-26 22:55:22",
	"status": "SLEEPING",
	"ac_power": 0,
	"dc_power": 0,
	"total_production": 96579,
	"ac_voltage": 244.90,
	"ac_current": 0.00,
	"dc_voltage": 0.00,
	"dc_current": 0.00,
	"temperature": 25.18,
	"exported_energy": 0,
	"imported_energy": 0,
	"exported_energy_m2": 0,
	"imported_energy_m2": 0
}
```

The hard part is now done!


# Installation

Assuming you have a conda env already setup for this package, and you have the base requirements from above.

```bash
git clone https://github.com/fdosani/solaredge-influx.git
cd solaredge-influx
pip install .
```