
### explore the dataset to get a feeling about it

    less data.osm

    ls -lh data.osm

### read documentation - search openstreetmap documentation
clarify basic data features like nodes, ways, relations

You can find the [OSM XML article]
(https://wiki.openstreetmap.org/wiki/OSM_XML) on the OSM wiki

### explore example
Find all top level tags in the dataset (revise [audit.py](audit.py))

    tags = {}
    for event, elem in ET.iterparse(filename):
        tag = elem.tag
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1
    return tags
