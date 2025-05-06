# SAWGraph Water Ontology

This directory includes the current RDF/OWL version of the SAWGraph water ontology and a corresponding schema diagram.

The ontology represents both surface water (e.g., lakes and rivers) and groundwater (e.g., wells and aquifers) features. For surface water features it primarily reuses concepts from HY_Features (OGC WaterML 2: Part 3), which aligns with the Internet of Water (Geoconnex). A distinction is made between features (`hyfo:WaterFeature` and `hyf:HY_HydroFeature`) and their representations (`hyfo:WaterFeatureRepresenation`). For groundwater features it primarily reuses concepts from GroundWaterML2 (GWML2; OGC WaterML 2: Part 4) as well as concepts from the Hydro Foundational Ontology (HyFO), which builds on GWML2. Additional HyFO concepts are used to unify the surface water and groundwater features in a single ontology.

Some basic development notes are available on Google Drive: [SAWGraph Water Ontology Notes](https://docs.google.com/document/d/1Xt1DwA0yqQO5XrGjjg91M8qv9p_hAw7kgP76TqD0964/edit?usp=sharing).
