define(
    [],
    function() {

        /*
         * Model specially for the API sync that updates the section's
         * key without changing the chords.
         */
        return Backbone.Model.extend({

            url: function() {

                return (
                    GLOBALS.api_root_url +
                    'section-key/' +
                    this.get('section').get('id') + '/'
                );

            },

            isNew: function() {
                return true;
            },

            toJSON: function() {

                var section = this.get('section');

                return {
                    tonic: section.get('tonic'),
                    tonality: section.get('tonality')
                };

            }

        });

    }
);
