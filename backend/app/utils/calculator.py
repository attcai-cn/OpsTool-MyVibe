import ipaddress
from datetime import datetime, timezone


# Bandwidth conversion
# Units in bits per second
BANDWIDTH_UNITS = {
    "bps": 1,
    "Bps": 8,
    "Kbps": 1_000,
    "KBps": 8 * 1_000,
    "Mbps": 1_000_000,
    "MBps": 8 * 1_000_000,
    "Gbps": 1_000_000_000,
    "GBps": 8 * 1_000_000_000,
}


def convert_bandwidth(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit not in BANDWIDTH_UNITS or to_unit not in BANDWIDTH_UNITS:
        raise ValueError("Invalid bandwidth unit")
    bits = value * BANDWIDTH_UNITS[from_unit]
    result = bits / BANDWIDTH_UNITS[to_unit]
    return result


def convert_timestamp(timestamp: int | None = None, dt_str: str | None = None) -> dict:
    if timestamp is not None:
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return {
            "timestamp": timestamp,
            "datetime_utc": dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "datetime_local": datetime.fromtimestamp(timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "iso": dt.isoformat(),
        }
    elif dt_str is not None:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S", "%Y/%m/%d"):
            try:
                dt = datetime.strptime(dt_str, fmt)
                ts = int(dt.timestamp())
                return {
                    "timestamp": ts,
                    "datetime_utc": dt.replace(tzinfo=timezone.utc).strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    ),
                    "datetime_local": dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "iso": dt.replace(tzinfo=timezone.utc).isoformat(),
                }
            except ValueError:
                continue
        raise ValueError("Unsupported datetime format")
    else:
        # Return current time
        now = datetime.now(timezone.utc)
        ts = int(now.timestamp())
        return {
            "timestamp": ts,
            "datetime_utc": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "datetime_local": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
            "iso": now.isoformat(),
        }


def calculate_subnet(cidr: str) -> dict:
    try:
        network = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        raise ValueError(f"Invalid CIDR: {e}")

    hosts = list(network.hosts())
    return {
        "network": str(network.network_address),
        "netmask": str(network.netmask),
        "broadcast": str(network.broadcast_address),
        "prefixlen": network.prefixlen,
        "total_hosts": network.num_addresses - 2
        if network.num_addresses > 2
        else network.num_addresses,
        "first_host": str(hosts[0]) if hosts else None,
        "last_host": str(hosts[-1]) if hosts else None,
        "cidr": str(network),
        "version": network.version,
    }
