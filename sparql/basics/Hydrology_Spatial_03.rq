
# Finds all gravel wells (as well as use and depth) that connect to sand and gravel aquifers in Penobscot county.
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX me_mgs: <http://sawgraph.spatialai.org/v1/me-mgs#>
PREFIX fio: <http://w3id.org/fio/v1/fio#>
PREFIX naics: <http://sawgraph.spatialai.org/v1/fio/naics#>
PREFIX us_frs: <http://sawgraph.spatialai.org/v1/us-frs#>
PREFIX me_mgs_data: <http://sawgraph.spatialai.org/v1/me-mgs-data#>
PREFIX kwg-ont: <http://stko-kwg.geog.ucsb.edu/lod/ontology/>
PREFIX spatial: <http://purl.org/spatialai/spatial/spatial-full#>
PREFIX kwgr: <http://stko-kwg.geog.ucsb.edu/lod/resource/>
PREFIX qudt: <http://qudt.org/schema/qudt/>
PREFIX saw_water: <http://sawgraph.spatialai.org/v1/saw_water#>
PREFIX gwml2: <http://gwml2.org/def/gwml2#>

SELECT DISTINCT ?well ?use ?depth_val ?wellType ?aq ?aqtype WHERE {

        ?well a me_mgs:MGS-Well .
        ?well me_mgs:hasUse ?use.
        ?well me_mgs:ofWellType me_mgs_data:d.wellType.Gravel.
        ?well me_mgs:ofWellType ?wellType.
        ?well me_mgs:wellDepth ?wellDepth.
        ?wellDepth qudt:numericValue ?depth_val .
        ?well kwg-ont:sfWithin ?s2neighbor.

      SERVICE <repository:Spatial> {
      SELECT * WHERE {
    	# Restrict them to Penobscot County, Maine
   		?s2neighbor spatial:connectedTo kwgr:administrativeRegion.USA.23019.
        }
    }

        ?aq rdf:type gwml2:GW_Aquifer.
        ?aq saw_water:aquiferType ?aqtype.

    	# just sand and gravel aquifers
        FILTER(?aqtype = 'sand and gravel')
	    # Find all wells that access the aquifers
    	?sp_s2 spatial:connectedTo ?aq .
    	?aq rdf:type gwml2:GW_Aquifer .
    	?aq_s2 spatial:connectedTo ?aq .
        ?aq_s2 rdf:type kwg-ont:S2Cell_Level13 .
        ?well rdf:type me_mgs:MGS-Well .
	    ?well kwg-ont:sfWithin ?aq_s2 .


} ORDER BY ?depth_val LIMIT 100