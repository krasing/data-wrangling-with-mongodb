
### Explore the dataset to get a feeling about it

    less data.osm

    ls -lh data.osm

### Read documentation - search openstreetmap documentation
clarify basic data features like nodes, ways, relations

You can find the [OSM XML article]
(https://wiki.openstreetmap.org/wiki/OSM_XML) on the OSM wiki

### Openstreetmap data iterative parsing
Find all top level tags in the dataset (revise audit.py)

    import xml.etree.cElementTree as ET
    
    tags = {}
    for event, elem in ET.iterparse(filename):
        tag = elem.tag
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1
    return tags

### Decide on a data model

```json
{
"id": "2406124091",
"visible":"true",
"version":"2",
"changeset":"17206049",
"timestamp":"2013-08-03T16:43:42Z",
"user":"linuxUser16",
"uid":"1219059"
"pos": [41.9757030, -87.6921867],
"tags": [
         { "k" : "addr:housenumber", "v" : "5157"},
         { "k" : "addr:postcode", "v" : "60625"},
         { "k" : "addr:street", "v" : "North Lincoln Ave"},
        ]
```
OR

```json
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}
```
### 

```python
def audit():
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    pprint.pprint(dict(street_types))
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
```

