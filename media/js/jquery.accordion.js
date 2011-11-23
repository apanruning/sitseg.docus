/*
* Menu accordion plugin for jQuery, by David Rojas (c) 2010
* http://www.davidrojas.net
*/
(function($){
	
	$.fn.accordion = function(custom) {
		var defaults = {
			keepOpen: false,
			startingOpen: false
		} 
		var settings = $.extend({}, defaults, custom);
		if(settings.startingOpen){
			$(settings.startingOpen).show();
		}
	
		return this.each(function(){
			var obj = $(this);
			$('li a', obj).click(function(event){
					var elem = $(this).next();
					if(elem.is('ul')){
						event.preventDefault();
						if(!settings.keepOpen){
							obj.find('ul:visible').not(elem).not(elem.parents('ul:visible')).slideUp();
						}
						elem.slideToggle();
					}
			});
		});
	};
})(jQuery);