define(
    ['collections/subsections'],
    function(Subsections) {

        return Backbone.Model.extend({

            initialize: function() {
                this.initData();
                this.initListeners();
            },

            initData: function() {

                // Only set subsections if it hasn't been set yet. Prevents errors
                // when cloning.
                if(!(this.get('subsections') instanceof Backbone.Collection)) {

                    var that = this;
                    var subsections = new Subsections();
                    subsections.url = this.subsectionsUrl();

                    _.each(this.get('subsections'), function(subsection_data) {
                        subsection_data.section = that;
                        subsections.add(subsection_data);
                    });

                    this.set('subsections', subsections);

                }

            },

            subsectionsUrl: function() {
                return this.url() + '/subsections';
            },

            initListeners: function() {
                this.stopListening();
                this.listenTo(this, 'change:alt_name', this.parseSectionNames);
            },

            /**
             * Returns the on-screen height of this section.
             */
            height: function() {

                var height = 0;

                this.get('subsections').each(function(subsection) {
                    height += subsection.height();
                });

                return height;

            },

            /**
             * Returns the name of the section.
             *
             * If `alt_name` is set, this will be used, otherwise,
             * `getSequenceLetter()` will be used.
             */
            getName: function() {

                if (this.get('alt_name')) {
                    return this.get('alt_name');
                } else {
                    return this.getSequenceLetter() + ' Section';
                }

            },

            /**
             * Returns the sequence letter this section would have in
             * case he wouldn't have an `alt_name`.
             */
            getSequenceLetter: function() {

                var this_number = this.get('number');

                var sections = this.collection.filter(function(section) {
                    return (
                        !section.get('alt_name') &&
                        section.get('number') < this_number
                    );
                });

                return 'ABCDEFG'[sections.length];

            },

            /**
             * Parses the names for the sections following this one.
             *
             * The section names will be based on this section name. For
             * example, if this is the first section and it has a an
             * `alt_name`, and the next section doesn't have an
             * `alt_name`, then this section can take the sequence name
             * `A`. If this section wouldn't have an `alt_name`, this
             * section's sequence letter would be `A` so the next sectin
             * would know it should have sequence letter `B`.
             */
            parseSectionNames: function() {

                if (!this.collection) {
                    // If we're not in a collection yet, this is not
                    // possible/necessary.
                    return;
                }

                var this_number = this.get('number');

                this.collection.each(function(section) {
                    if (
                        !section.get('alt_name') &&
                        section.get('number') > this_number
                    ) {
                        section.trigger('change');
                    }
                });

            },

            copy: function(attributes) {

                var copy = this.clone();
                copy.set({
                    id: null,
                    subsections: this.get('subsections').copy({ section: copy })
                });

                if(attributes) {
                    copy.set(attributes);
                }

                copy.initListeners();

                return copy;

            },

            /**
             * Recursively saves this section and it's children (lines,
             * measures and chords).
             */
            saveRecursive: function() {

                var that = this;

                this.save(null, { success: function() {
                    that.get('subsections').url = that.subsectionsUrl();
                    that.get('subsections').each(function(subsection) {
                        subsection.saveRecursive();
                    });
                }});

            },

            toJSON: function() {
                return {
                    number: this.get('number'),
                    alt_name: this.get('alt_name'),
                    key_distance_from_chart: this.get('key_distance_from_chart'),
                    time_signature: this.get('time_signature'),
                    use_subsections: this.get('use_subsections')
                };
            }

        });

    }
);
