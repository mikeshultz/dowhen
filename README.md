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
