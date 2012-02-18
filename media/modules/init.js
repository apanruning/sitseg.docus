/*** 
    This module extends the state layer to set specific initialization 
    functions to state 
***/

// This funcion hide what layers must be available in the switcher-layers 
// control map when the map is shown
Maap.State.prototype.initializeBaseLayers = function() {
    layerMapnik = new OpenLayers.Layer.OSM.Mapnik(
            "OpenStreetMap (Mapnik)",
            {layers: 'basic'}
    );
    this.map.addLayer(layerMapnik); 
    this.base_layers = this.base_layers.concat(layerMapnik);

    return 0;
}

// This funcion set the initial bounds for map
Maap.State.prototype.initializeBounds = function() {
    //change this values for change de level zoom
    this.map.zoomToExtent(
        new OpenLayers.Bounds(
            -7160964.775099885,
            -3693704.7356770867,
            -7130772.148932681,
            -3678417.3300227895
        ),
        true
    );
    return 0;
}

// This function initialize the control objects of state 
Maap.State.prototype.initializeControls = function () {
    //add and/or remove controls to map
    this.map.addControl(new OpenLayers.Control.Navigation()); 
    this.map.addControl(new OpenLayers.Control.PanZoomBar());
    this.map.addControl(new OpenLayers.Control.OverviewMap());
    this.map.addControl(new OpenLayers.Control.LayerSwitcher({'ascending':false}))
    this.map.addControl(new OpenLayers.Control.ScaleLine());
    this.map.addControl(new OpenLayers.Control.Permalink('permalink'));
    this.map.addControl(new OpenLayers.Control.KeyboardDefaults());
    this.map.addControl(new OpenLayers.Control.Attribution());
    this.map.addControl(new OpenLayers.Control.MousePosition());

    return 0;
}


// This function initialize all settings of state. 
Maap.State.prototype.init = function() {

    //add initial layers to map
    this.initializeBaseLayers();

    var ol_wms = new OpenLayers.Layer.WMS(
                "OpenLayers WMS",
                "http://vmap0.tiles.osgeo.org/wms/vmap0",
                {layers: 'basic'} 
            );

    var gwc = new OpenLayers.Layer.WMS(
                "Global Imagery",
                "http://maps.opengeo.org/geowebcache/service/wms",
                {layers: "bluemarble"},
                {tileOrigin: new OpenLayers.LonLat(-180, -90)}
            );
    var dm_wms = new OpenLayers.Layer.WMS(
                "DM Solutions Demo",
                "http://www2.dmsolutions.ca/cgi-bin/mswms_gmap",
                {layers: "bathymetry,land_fn,park,drain_fn,drainage," +
                     "prov_bound,fedlimit,rail,road,popplace",
                 transparent: "true", format: "image/png"},
                {visibility: false}
            );

    this.map.addLayers([ol_wms, gwc, dm_wms]);

    var layOsmarender = new OpenLayers.Layer.OSM.Osmarender("Osmarender");
    this.map.addLayer(layOsmarender);

    var layCycleMap = new OpenLayers.Layer.OSM.CycleMap("CycleMap");
    this.map.addLayer(layCycleMap);

    //load controls to map
    this.initializeControls();

    //set the level to the user can see the map. (zoom)        
    this.initializeBounds(); 

    return 0;

}
        

