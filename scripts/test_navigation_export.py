import unittest, tempfile, json
from pathlib import Path
from xml.etree import ElementTree as ET
import navigation_export as n

class NavigationExportTest(unittest.TestCase):
 def sample(self):
  return {'revision':'r1','route_geometry':[{'name':'D1 coastal road','geometry_kind':'schematic_waypoint_connection','crs':'WGS84','coordinates':[[121,31],[121.1,31.1],[121.2,31]],'source_urls':['https://example.org/observed-points']} ]}
 def test_no_silent_coordinate_system_conversion(self):
  p=self.sample();p['route_geometry'][0]['crs']='GCJ02'
  with self.assertRaises(ValueError):n.build_kml(p)
 def test_requires_sources_and_valid_coordinates(self):
  for field,value in [('source_urls',[]),('coordinates',[[300,31],[121,31]])]:
   p=self.sample();p['route_geometry'][0][field]=value
   with self.assertRaises(ValueError):n.build_kml(p)
 def test_order_and_geometry_semantics_survive(self):
  root=ET.fromstring(n.build_kml(self.sample()));ns={'k':'http://www.opengis.net/kml/2.2'}
  coords=root.find('.//k:LineString/k:coordinates',ns).text.split()
  self.assertEqual(coords,['121,31','121.1,31.1','121.2,31'])
  self.assertIn('schematic_waypoint_connection',''.join(root.itertext()))
  self.assertNotIn('<time>',ET.tostring(root,encoding='unicode'))
 def test_missing_geometry_does_not_invent_track(self):
  with self.assertRaises(ValueError):n.build_kml({'days':[{'route':'A to B'}]})
 def test_boolean_coordinates_rejected(self):
  p=self.sample();p['route_geometry'][0]['coordinates'][0][0]=True
  with self.assertRaises(ValueError):n.build_kml(p)
 def test_road_geometry_requires_provider_evidence(self):
  p=self.sample();p['route_geometry'][0]['geometry_kind']='provider_road_geometry'
  with self.assertRaises(ValueError):n.build_kml(p)

if __name__=='__main__':unittest.main()
