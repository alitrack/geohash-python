# Python Geohash

A Python implementation of the Geohash algorithm compatible with  [python-geohash](https://pypi.org/project/python-geohash/). This package provides functionality to encode and decode geohashes, as well as find neighboring geohashes. It supports both string-based and uint64-based geohash representations.

## Installation

```bash
pip install geohash-python
```

## Features

- Encode latitude/longitude to geohash
- Decode geohash to latitude/longitude
- Get neighboring geohashes
- Get bounding box for geohash
- Pure Python implementation
- uint64 geohash support for efficient storage and computation

## API Reference

### String-based Geohash Operations

#### encode(latitude, longitude, precision=12)
Encode a position to geohash string
- Parameters:
  - latitude: float (-90.0 to 90.0)
  - longitude: float (-180.0 to 180.0)
  - precision: int, length of resulting geohash string (default: 12)
- Returns: str, geohash string

#### decode(hashcode)
Decode a geohash string to latitude/longitude
- Parameters:
  - hashcode: str, geohash string
- Returns: tuple (latitude, longitude)

#### decode_exactly(hashcode)
Decode a geohash string to latitude/longitude with error margins
- Parameters:
  - hashcode: str, geohash string
- Returns: tuple (latitude, longitude, latitude_error, longitude_error)

#### neighbors(hashcode)
Get all 8 adjacent geohashes
- Parameters:
  - hashcode: str, geohash string
- Returns: dict with keys n,ne,e,se,s,sw,w,nw containing neighboring geohashes

#### expand(hashcode)
Alias for neighbors() - returns all 8 adjacent geohashes
- Parameters:
  - hashcode: str, geohash string
- Returns: dict with keys n,ne,e,se,s,sw,w,nw containing neighboring geohashes

#### bbox(hashcode)
Get the bounding box of a geohash
- Parameters:
  - hashcode: str, geohash string
- Returns: dict with keys n,s,e,w containing the bounds

### uint64-based Geohash Operations

#### encode_uint64(latitude, longitude)
Encode a position to 64-bit integer geohash
- Parameters:
  - latitude: float (-90.0 to 90.0)
  - longitude: float (-180.0 to 180.0)
- Returns: int, 64-bit unsigned integer geohash

#### decode_uint64(geohash_uint64)
Decode a 64-bit integer geohash to latitude/longitude
- Parameters:
  - geohash_uint64: int, 64-bit unsigned integer geohash
- Returns: tuple (latitude, longitude)

#### expand_uint64(geohash_uint64)
Get ranges of adjacent geohashes as uint64 values
- Parameters:
  - geohash_uint64: int, 64-bit unsigned integer geohash
- Returns: list of tuples [(min_hash1, max_hash1), (min_hash2, max_hash2), ...] representing ranges of neighboring geohashes

## Usage Examples

### String-based Geohash Operations

```python
import geohash

# Encode a location
lat, lon = 37.8324, -122.2715
hash = geohash.encode(lat, lon)  # returns 12 character string
hash = geohash.encode(lat, lon, precision=6)  # returns 6 character string

# Decode a geohash
lat, lon = geohash.decode(hash)

# Get exact decoding with error margins
lat, lon, lat_err, lon_err = geohash.decode_exactly(hash)

# Get bounding box
bbox = geohash.bbox(hash)
print(f"North: {bbox['n']}, South: {bbox['s']}, East: {bbox['e']}, West: {bbox['w']}")

# Get neighbors
neighbors = geohash.neighbors(hash)
print(f"North: {neighbors['n']}, Northeast: {neighbors['ne']}")
```

### uint64-based Geohash Operations

```python
import geohash

# Encode latitude/longitude to uint64 geohash
lat, lon = 37.8324, -122.2715
uint64_hash = geohash.encode_uint64(lat, lon)

# Decode uint64 geohash to latitude/longitude
lat, lon = geohash.decode_uint64(uint64_hash)

# Get neighbor ranges as uint64 values
neighbor_ranges = geohash.expand_uint64(uint64_hash)
for min_hash, max_hash in neighbor_ranges:
    print(f"Range: {min_hash} to {max_hash}")
```

## uint64 Geohash Format

The uint64 geohash format uses a 64-bit unsigned integer to represent a geohash:
- 32 bits for longitude precision
- 32 bits for latitude precision
- Bits are interleaved: even bits for longitude, odd bits for latitude
- Provides approximately 0.5cm precision at the equator

Benefits of uint64 geohash:
- More efficient storage in databases
- Faster comparison operations
- Memory-efficient geospatial calculations
- Consistent precision across all locations

## License

MIT License
