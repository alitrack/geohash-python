"""
Pure Python implementation of Geohash compatible with python-geohash
"""
from math import log10

__version__ = "0.8.5"
__all__ = ['encode', 'decode', 'decode_exactly', 'bbox', 'neighbors', 'expand',
           'decode_uint64', 'encode_uint64', 'expand_uint64']

_base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
_base32_map = {c: i for i, c in enumerate(_base32)}

def _encode_i2c(lat, lon, lat_length, lon_length):
    """Interleave bits of latitude and longitude to create geohash"""
    precision = int((lat_length + lon_length) / 5)
    if lat_length < lon_length:
        a = lon
        b = lat
    else:
        a = lat
        b = lon
    
    boost = (0, 1, 4, 5, 16, 17, 20, 21)
    ret = ''
    for i in range(precision):
        ret += _base32[(boost[a & 7] + (boost[b & 3] << 1)) & 0x1F]
        t = a >> 3
        a = b >> 2
        b = t
    
    return ret[::-1]

def encode(latitude, longitude, precision=12):
    """
    Encode a position given in float arguments latitude, longitude to
    a geohash which will have the character count precision.
    """
    if latitude >= 90.0 or latitude < -90.0:
        raise ValueError("invalid latitude")
    while longitude < -180.0:
        longitude += 360.0
    while longitude >= 180.0:
        longitude -= 360.0

    lat_interval = (-90.0, 90.0)
    lon_interval = (-180.0, 180.0)
    
    geohash = []
    bits = [16, 8, 4, 2, 1]
    bit = 0
    ch = 0
    even = True
    
    while len(geohash) < precision:
        if even:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                ch |= bits[bit]
                lon_interval = (mid, lon_interval[1])
            else:
                lon_interval = (lon_interval[0], mid)
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                ch |= bits[bit]
                lat_interval = (mid, lat_interval[1])
            else:
                lat_interval = (lat_interval[0], mid)
        
        even = not even
        if bit < 4:
            bit += 1
        else:
            geohash.append(_base32[ch])
            bit = 0
            ch = 0
    
    return ''.join(geohash)

def decode(hashcode, delta=False):
    """
    Decode a geohash to a (latitude, longitude) pair.
    If delta is True, return the bounding box deltas too.
    """
    lat_interval = (-90.0, 90.0)
    lon_interval = (-180.0, 180.0)
    
    lat_err = 90.0
    lon_err = 180.0
    even = True
    
    for c in hashcode:
        cd = _base32_map[c]
        for mask in [16, 8, 4, 2, 1]:
            if even:
                lon_err /= 2
                if cd & mask:
                    lon_interval = ((lon_interval[0] + lon_interval[1])/2, lon_interval[1])
                else:
                    lon_interval = (lon_interval[0], (lon_interval[0] + lon_interval[1])/2)
            else:
                lat_err /= 2
                if cd & mask:
                    lat_interval = ((lat_interval[0] + lat_interval[1])/2, lat_interval[1])
                else:
                    lat_interval = (lat_interval[0], (lat_interval[0] + lat_interval[1])/2)
            even = not even
    
    lat = (lat_interval[0] + lat_interval[1]) / 2
    lon = (lon_interval[0] + lon_interval[1]) / 2
    
    if delta:
        return lat, lon, lat_err, lon_err
    return lat, lon

def decode_exactly(hashcode):
    """
    Decode a geohash to a (latitude, longitude) pair and the bounding
    box it was encoded from.
    """
    lat, lon, lat_err, lon_err = decode(hashcode, True)
    return lat, lon, lat_err, lon_err

def bbox(hashcode):
    """
    Decode a geohash to a bounding box that contains the original
    rectangle that was encoded.
    """
    lat, lon, lat_err, lon_err = decode(hashcode, True)
    return {
        'n': lat + lat_err,
        's': lat - lat_err,
        'e': lon + lon_err,
        'w': lon - lon_err
    }

def _neighbor_strings():
    """Return list of neighbor direction strings"""
    return {
        'n': ['p0r21436x8zb9dcf5h7kjnmqesgutwvy', 'bc01fg45238967deuvhjyznpkmstqrwx'],
        's': ['14365h7k9dcfesgujnmqp0r2twvyx8zb', '238967debc01fg45kmstqrwxuvhjyznp'],
        'e': ['bc01fg45238967deuvhjyznpkmstqrwx', 'p0r21436x8zb9dcf5h7kjnmqesgutwvy'],
        'w': ['238967debc01fg45kmstqrwxuvhjyznp', '14365h7k9dcfesgujnmqp0r2twvyx8zb']
    }

def _border_strings():
    """Return list of border strings"""
    return {
        'n': ['prxz', 'bcfguvyz'],
        's': ['028b', '0145hjnp'],
        'e': ['bcfguvyz', 'prxz'],
        'w': ['0145hjnp', '028b']
    }

def neighbors(hashcode):
    """
    Return a dictionary with keys of n, ne, e, se, s, sw, w, nw
    and values of the neighboring geohash in that direction.
    """
    neighbor_strings = _neighbor_strings()
    borders = _border_strings()
    
    def _get_neighbor(hashcode, direction):
        if not hashcode:
            return ''
        
        neighbor = list(hashcode)
        last_chr = neighbor[-1]
        type_ = len(hashcode) % 2
        
        if last_chr in borders[direction][type_]:
            neighbor_prefix = _get_neighbor(''.join(neighbor[:-1]), direction)
            if not neighbor_prefix:
                return ''
            idx = neighbor_strings[direction][type_].find(last_chr)
            if idx != -1:
                return neighbor_prefix + _base32[idx]
            return ''
        else:
            idx = neighbor_strings[direction][type_].find(last_chr)
            if idx != -1:
                neighbor[-1] = _base32[idx]
                return ''.join(neighbor)
            return ''
    
    return {
        'n':  _get_neighbor(hashcode, 'n'),
        's':  _get_neighbor(hashcode, 's'),
        'e':  _get_neighbor(hashcode, 'e'),
        'w':  _get_neighbor(hashcode, 'w'),
        'ne': _get_neighbor(_get_neighbor(hashcode, 'n'), 'e'),
        'nw': _get_neighbor(_get_neighbor(hashcode, 'n'), 'w'),
        'se': _get_neighbor(_get_neighbor(hashcode, 's'), 'e'),
        'sw': _get_neighbor(_get_neighbor(hashcode, 's'), 'w')
    }

def expand(hashcode):
    """
    Expand a geohash to the nine geohashes that form a 3x3 grid
    containing the original geohash in the center.
    """
    return neighbors(hashcode)

def decode_uint64(geohash_uint64):
    """
    Decode a uint64 geohash to a (latitude, longitude) pair.
    
    Args:
        geohash_uint64: 64-bit unsigned integer representing a geohash
        
    Returns:
        tuple: (latitude, longitude)
    """
    bits = [(geohash_uint64 >> i) & 1 for i in range(63, -1, -1)]
    lat_bits = bits[1::2]
    lon_bits = bits[0::2]
    
    lat_interval = (-90.0, 90.0)
    lon_interval = (-180.0, 180.0)
    
    for lat_bit in lat_bits:
        lat_mid = (lat_interval[0] + lat_interval[1]) / 2
        if lat_bit:
            lat_interval = (lat_mid, lat_interval[1])
        else:
            lat_interval = (lat_interval[0], lat_mid)
    
    for lon_bit in lon_bits:
        lon_mid = (lon_interval[0] + lon_interval[1]) / 2
        if lon_bit:
            lon_interval = (lon_mid, lon_interval[1])
        else:
            lon_interval = (lon_interval[0], lon_mid)
    
    return ((lat_interval[0] + lat_interval[1]) / 2,
            (lon_interval[0] + lon_interval[1]) / 2)

def encode_uint64(latitude, longitude):
    """
    Encode a position given in float arguments latitude, longitude to
    a uint64 geohash.
    
    Args:
        latitude: float latitude (-90.0 to 90.0)
        longitude: float longitude (-180.0 to 180.0)
        
    Returns:
        int: 64-bit unsigned integer representing the geohash
    """
    if latitude >= 90.0 or latitude < -90.0:
        raise ValueError("invalid latitude")
    while longitude < -180.0:
        longitude += 360.0
    while longitude >= 180.0:
        longitude -= 360.0

    lat_interval = (-90.0, 90.0)
    lon_interval = (-180.0, 180.0)
    
    geohash_uint64 = 0
    bit_length = 0
    
    while bit_length < 64:
        if bit_length % 2 == 0:
            mid = (lon_interval[0] + lon_interval[1]) / 2
            if longitude > mid:
                geohash_uint64 = (geohash_uint64 << 1) | 1
                lon_interval = (mid, lon_interval[1])
            else:
                geohash_uint64 = (geohash_uint64 << 1) | 0
                lon_interval = (lon_interval[0], mid)
        else:
            mid = (lat_interval[0] + lat_interval[1]) / 2
            if latitude > mid:
                geohash_uint64 = (geohash_uint64 << 1) | 1
                lat_interval = (mid, lat_interval[1])
            else:
                geohash_uint64 = (geohash_uint64 << 1) | 0
                lat_interval = (lat_interval[0], mid)
        
        bit_length += 1
    
    return geohash_uint64

def expand_uint64(geohash_uint64):
    """
    Return a list of uint64 geohash ranges that surround the given uint64 geohash.
    Each range is represented as a tuple of (min_hash, max_hash).
    
    Args:
        geohash_uint64: 64-bit unsigned integer representing a geohash
        
    Returns:
        list: List of tuples [(min_hash1, max_hash1), (min_hash2, max_hash2), ...]
              representing ranges of neighboring geohashes
    """
    lat, lon = decode_uint64(geohash_uint64)
    lat_err = 90.0 / (1 << 32)  # Error for 32 bits of latitude precision
    lon_err = 180.0 / (1 << 32)  # Error for 32 bits of longitude precision
    
    ranges = []
    # North range
    ranges.append((
        encode_uint64(lat + lat_err/2, lon - lon_err),
        encode_uint64(lat + lat_err/2, lon + lon_err)
    ))
    # East range
    ranges.append((
        encode_uint64(lat - lat_err, lon + lon_err/2),
        encode_uint64(lat + lat_err, lon + lon_err/2)
    ))
    # South range
    ranges.append((
        encode_uint64(lat - lat_err/2, lon - lon_err),
        encode_uint64(lat - lat_err/2, lon + lon_err)
    ))
    # West range
    ranges.append((
        encode_uint64(lat - lat_err, lon - lon_err/2),
        encode_uint64(lat + lat_err, lon - lon_err/2)
    ))
    
    return ranges
