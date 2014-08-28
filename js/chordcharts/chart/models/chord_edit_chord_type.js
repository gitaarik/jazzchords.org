var ChordType = require('./chord_type.js');


module.exports = Backbone.Model.extend({
    initialize: function() {
        this.set('chord_type', new ChordType(this.get('chord_type')));
    }
});
