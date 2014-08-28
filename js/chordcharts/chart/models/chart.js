var Sections = require('../collections/sections.js');


module.exports = Backbone.Model.extend({

    initialize: function() {

        // Only set sections if it hasn't been set yet. Prevents errors
        // when cloning.
        if (!(this.get('sections') instanceof Backbone.Collection)) {

            var that = this;
            var sections = new Sections();

            sections.url = (
                GLOBALS.api_root_url + 'charts/' +
                this.get('id') + '/sections'
            );

            _.each(this.get('sections'), function(section_data) {
                section_data.chart = that;
                sections.add(section_data);
            });

            this.set('sections', sections);

        }

    }

});
