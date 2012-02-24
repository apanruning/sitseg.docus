/*** 
    This module extends the state layer to set specific initialization 
    functions to state 
***/

// This funcion hide what layers must be available in the switcher-layers 
// control map when the map is shown
Maap.State.prototype.initializeBaseLayers = function() {
var gphy = new OpenLayers.Layer.Google(
        "Google Physical",
        {type: google.maps.MapTypeId.TERRAIN}
    );
    var gmap = new OpenLayers.Layer.Google(
        "Google Streets", // the default
        {numZoomLevels: 20}
    );
    var ghyb = new OpenLayers.Layer.Google(
        "Google Hybrid",
        {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 20}
    );
    var gsat = new OpenLayers.Layer.Google(
        "Google Satellite",
        {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22}
    );

    this.map.addLayers([gphy, gmap, ghyb, gsat]);

    this.base_layers = this.base_layers.concat([gphy]);

    return 0;
}

// This funcion set the initial bounds for map
Maap.State.prototype.initializeBounds = function() {
    this.map.setCenter(new OpenLayers.LonLat(-68, -34).transform(
        new OpenLayers.Projection("EPSG:4326"),
        this.map.getProjectionObject()
    ), 5);
    return 0;
}

// This function initialize the control objects of state 
Maap.State.prototype.initializeControls = function () {
    //add and/or remove controls to map
    this.map.addControl(new OpenLayers.Control.Navigation()); 
    this.map.addControl(new OpenLayers.Control.PanZoomBar());
    this.map.addControl(new OpenLayers.Control.LayerSwitcher())
    this.map.addControl(new OpenLayers.Control.Attribution());
    this.map.addControl(new OpenLayers.Control.MousePosition());

    return 0;
}


// This function initialize all settings of state. 
Maap.State.prototype.init = function() {

    //add initial layers to map
    this.initializeBaseLayers();

    
    //load controls to map
    this.initializeControls();

    //set the level to the user can see the map. (zoom)        
    this.initializeBounds(); 

    return 0;

}
        

