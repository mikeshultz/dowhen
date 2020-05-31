from dowhen.common import normalize_mac_address
from dowhen.do.wemo.comm import discover_wemo


def main():
    devices = discover_wemo()

    for dev in devices:
        print("[Wemo {}] {}: {}".format(
            dev.device_type,
            dev.name,
            normalize_mac_address(dev.mac)
        ))


if __name__ == "__main__":
    main()
