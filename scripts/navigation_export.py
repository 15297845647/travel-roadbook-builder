#!/usr/bin/env python3
"""Export evidenced WGS84 route geometry as KML; never computes roads or imports accounts."""
import argparse,json,math
from pathlib import Path
from xml.etree import ElementTree as ET

NS='http://www.opengis.net/kml/2.2'
ET.register_namespace('',NS)
def el(parent,name,text=None):
 node=ET.SubElement(parent,'{'+NS+'}'+name)
 if text is not None:node.text=str(text)
 return node

def build_kml(plan):
 geometries=plan.get('route_geometry',[])
 if not geometries:raise ValueError('No evidenced geometry; do not invent a track from names.')
 root=ET.Element('{'+NS+'}kml');doc=el(root,'Document');el(doc,'name',plan.get('trip',{}).get('title','Travel route'))
 el(doc,'description','Planning geometry, not a recorded journey. Read geometry_kind for each segment. Schematic connections are not roads or navigable tracks. Revision: '+str(plan.get('revision','')))
 for g in geometries:
  if g.get('crs')!='WGS84':raise ValueError('KML requires WGS84; convert only with a documented transformation, outside this exporter.')
  if g.get('geometry_kind') not in ['schematic_waypoint_connection','provider_road_geometry']:raise ValueError('Unknown geometry semantics')
  if g['geometry_kind']=='provider_road_geometry':
   if not all(g.get(k) for k in ['provider','checked_at','request_stops','response_reference']):raise ValueError('Provider road geometry requires provider, checked_at, request_stops and preserved response reference')
  if not g.get('source_urls') or any(not u.startswith('https://') for u in g['source_urls']):raise ValueError('Geometry sources required')
  coords=g.get('coordinates',[])
  if len(coords)<2:raise ValueError('Two or more coordinates required')
  for c in coords:
   if len(c)!=2 or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in c) or not -180<=c[0]<=180 or not -90<=c[1]<=90:raise ValueError('Invalid longitude/latitude')
  mark=el(doc,'Placemark');el(mark,'name',g['name']+(' [示意/非导航]' if g['geometry_kind']=='schematic_waypoint_connection' else ''));el(mark,'description',g['geometry_kind']+'; '+g.get('description','')+'; Sources: '+' '.join(g['source_urls']))
  style=el(mark,'Style');line=el(style,'LineStyle');el(line,'color',g.get('kml_color','ff376fca'));el(line,'width','4')
  data=el(mark,'ExtendedData')
  for key,val in [('geometry_kind',g['geometry_kind']),('crs','WGS84'),('revision',plan.get('revision',''))]:
   item=el(data,'Data');item.set('name',key);el(item,'value',val)
  ls=el(mark,'LineString');el(ls,'tessellate','1');el(ls,'coordinates',' '.join(','.join(str(v) for v in c) for c in coords))
 return ET.tostring(root,encoding='unicode',xml_declaration=True)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 args.output.write_text(build_kml(json.loads(args.plan.read_text())),encoding='utf-8')
if __name__=='__main__':main()
