# dowhen

A conditional execution system and scheduler.  Pretty much a self-hosted IFTTT.

## Quickstart

### Install

    python setup.py install

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
