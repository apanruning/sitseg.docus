/** This module hide state of system in client and hide the implementatios of certain funcions to manipulate this state **/

/**  State Object

structure: 
        base_layers: point to list of OpenLayers layer
        layers: hold the current Maap.Layers in the map
        map: point to map
        map_options: Base options for map
**/

// Initialization function
Maap.State = function() {
    // create map whith map options     
    mep = new OpenLayers.Map('map');

    // update the state variable
    this.map = mep
};

Maap.State.prototype = {
    map: null,
    base_layers: [],
    layers: [],    
};





