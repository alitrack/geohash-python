import unittest
import geohash

class TestGeohash(unittest.TestCase):
    def test_encode(self):
        """Test the encode functionality"""
        lat, lon = 39.9042, 116.4074
        precision = 12
        test_hash = geohash.encode(lat, lon, precision)
        assert test_hash == 'wx4g0bm6c408'
        self.assertEqual(len(test_hash), precision)

    def test_decode(self):
        """Test the decode functionality"""
        test_hash = 'wx4g0bm6c408'
        lat, lon = geohash.decode(test_hash)
        
        self.assertIsInstance(lat, float)
        self.assertIsInstance(lon, float)
        self.assertGreater(lat, -90.0)
        self.assertLess(lat, 90.0)
        self.assertGreater(lon, -180.0)
        self.assertLess(lon, 180.0)

    def test_decode_exactly(self):
        """Test the decode_exactly functionality"""
        test_hash = 'wx4g0bm6c408'
        lat, lon, lat_err, lon_err = geohash.decode_exactly(test_hash)
        
        self.assertIsInstance(lat, float)
        self.assertIsInstance(lon, float)
        self.assertIsInstance(lat_err, float)
        self.assertIsInstance(lon_err, float)
        
        # Test that errors are positive
        self.assertGreater(lat_err, 0)
        self.assertGreater(lon_err, 0)

    def test_neighbors(self):
        """Test the neighbors functionality"""
        test_hash = 'u0nd9hdfue8h'
        neighbors = geohash.neighbors(test_hash)
        
        # Check if all directions are present
        expected_directions = {'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'}
        self.assertEqual(set(neighbors.keys()), expected_directions)
        
        # Check if all neighbor hashes have the same length as input
        for direction, neighbor in neighbors.items():
            self.assertEqual(len(neighbor), len(test_hash))

    def test_uint64_encoding(self):
        """Test uint64 encoding and decoding"""
        # Test coordinates (Beijing)
        lat, lon = 39.9042, 116.4074
        
        # Test encode_uint64
        uint64_hash = geohash.encode_uint64(lat, lon)
        self.assertIsInstance(uint64_hash, int)
        
        # Test decode_uint64
        decoded_lat, decoded_lon = geohash.decode_uint64(uint64_hash)
        
        # Check if decoded coordinates are close to original
        self.assertAlmostEqual(lat, decoded_lat, places=4)
        self.assertAlmostEqual(lon, decoded_lon, places=4)

    def test_expand_uint64(self):
        """Test uint64 expansion"""
        lat, lon = 39.9042, 116.4074
        uint64_hash = geohash.encode_uint64(lat, lon)
        
        neighbor_ranges = geohash.expand_uint64(uint64_hash)
        self.assertTrue(len(neighbor_ranges) > 0)
        
        for min_hash, max_hash in neighbor_ranges:
            self.assertIsInstance(min_hash, int)
            self.assertIsInstance(max_hash, int)
            self.assertGreaterEqual(max_hash, min_hash)

if __name__ == '__main__':
    unittest.main()
