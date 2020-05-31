# dowhen

A conditional execution system and scheduler.  Pretty much a self-hosted IFTTT.
There is (currently) no UI.

## Quickstart

### Install

#### Generic

    pip3 install --user git+https://github.com/mikeshultz/dowhen.git

#### Production

    useradd dowhen
    sudo -u dowhen bash
    pip3 install --user git+https://github.com/mikeshultz/dowhen.git

You may also want to configure a daemon.  You can use the service file in this
repo as a template.

    # Service file location may be different depending on distro
    curl -s https://raw.githubusercontent.com/mikeshultz/dowhen/master/ops/systemd/dowhen.service | sudo tee /usr/lib/systemd/system/dowhen-test.service

### Configure

Create a configuration file at `$HOME/.config/dowhen/dowhen.yaml` with your
triggers.  An example config file is
[`dowhen.yaml.example`](dowhen.yaml.example).  Each trigger describes when to
fire and what to do when it fires.

For instance, to turn on a WeMo switch on sunrise:

    ---
    triggers:
      - when: 
          name: openweathermap.sunrise
          args:
            zip: 59801
        do:
          # Turn on plant lights
          - name: wemo.on
            args:
              mac: "30:23:DE:AD:BE:EF"

### Run

Then you can run the daemon:

    dowhen daemon

### Modules

#### When

"When" modules act as triggers.  They will signal when a condition is met. For
instance, it will indicate the current time, or certain weather conditions have
occurred.

##### datetime

The `datetime` When module will trigger on times and dates.

 - daily
 - hourly
 - minutely
 - time(time_string)

##### openweathermap

The `openweathermap` When module triggers on weather-based data.

- sunrise(zip)
- sunset(zip)

#### Do

"Do" modules perform actions.  For example, the Wemo Do module would do things
like turn on and off Wemo switches.

##### wemo

The `wemo` Do module performs actions on Belkin Wemo devices.

 - on(mac)
 - off(mac)
 - toggle(mac)
