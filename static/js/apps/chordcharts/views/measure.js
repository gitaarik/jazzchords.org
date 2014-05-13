define(
    ['models/measure', 'views/chord', 'init/measure_edit'],
    function(Measure, ChordView, measureEdit) {

        return Backbone.View.extend({

            tagName: 'td',
            className: 'measure',
            model: Measure,

            initialize: function() {

                if(!this.$el.find('.chords').length) {
                    this.$el.html('<div class="chords"></div>');
                }
                this.chords = this.$el.find('.chords');

                this.listenTo(this.model, 'change', this.render);
                this.listenTo(this.model, 'destroy', this.remove);

            },

            events: {
                'click': 'openMeasureEdit'
            },

            openMeasureEdit: function(event) {

                if($(event.target).closest('.chord-name').length) {
                    // If the click was on a chord name, the chord edit widget
                    // should open and not the measure edit widget.
                    return;
                }

                // If the measure edit widget is already open for this measure
                // then close it, otherwise open it.
                if(
                    measureEdit.get('visible') &&
                    measureEdit.get('measure') == this.model
                ) {
                    measureEdit.set('visible', false);
                }
                else {

                    // Don't allow to remove the measure if it's the
                    // last measure in the last line.
                    if (
                        this.model.get('line').get('measures').length == 1 &&
                        this.model.get('line').get('subsection').get('lines').length == 1
                    ) {
                        remove_possible = false;
                    } else {
                        remove_possible = true;
                    }

                    measureEdit.set({
                        'visible': true,
                        'measure': this.model,
                        'measure_el': this.$el,
                        'beat_schema': this.model.get('beat_schema'),
                        'remove_possible': remove_possible
                    });

                }

            },

            render: function() {
                this.chords.html('');
                this.drawChords();
                this.drawSeperationLines();
                return this;
            },

            drawChords: function() {

                this.$el.removeClass('measure-beatschema-' +
                    this.model.previousAttributes().beat_schema
                );
                this.$el.addClass('measure-beatschema-' + 
                    this.model.get('beat_schema')
                );

                var that = this;
                var beats = this.model.get('beat_schema').split('-');

                _.each(beats, function(chord, i) {

                    that.chords.append(
                        new ChordView({
                            model: that.model.get('chords').at(i)
                        }).render().el
                    );

                });

            },

            drawSeperationLines: function() {
                // Draws the lines that seperate the different measure parts
                // inside the measure

                var box_width = GLOBALS.settings.box_width;
                var box_height = GLOBALS.settings.box_height;
                var border_width = GLOBALS.settings.border_width;
                var canvas;
                var context;

                switch(this.model.get('beat_schema')) {

                    case '2-2':

                        canvas = document.createElement('canvas');
                        context = canvas.getContext('2d');

                        canvas.style.position = 'absolute';
                        canvas.width = box_width;
                        canvas.height = box_height;

                        context.lineWidth = border_width;

                        context.beginPath();
                        context.moveTo(box_width, 0);
                        context.lineTo(0, box_height);
                        context.stroke();

                        this.chords.prepend(canvas);

                        break;

                    case '2-1-1':

                        canvas = document.createElement('canvas');
                        context = canvas.getContext('2d');

                        canvas.style.position = 'absolute';
                        canvas.width = box_width;
                        canvas.height = box_height;

                        context.lineWidth = border_width;

                        context.beginPath();
                        context.moveTo(box_width, 0);
                        context.lineTo(0, box_height);
                        context.stroke();

                        context.beginPath();
                        context.moveTo(box_width / 2, box_height / 2);
                        context.lineTo(box_width, box_height);
                        context.stroke();

                        this.chords.prepend(canvas);

                        break;

                    case '1-1-2':

                        canvas = document.createElement('canvas');
                        context = canvas.getContext('2d');

                        canvas.style.position = 'absolute';
                        canvas.width = box_width;
                        canvas.height = box_height;

                        context.lineWidth = border_width;

                        context.beginPath();
                        context.moveTo(box_width, 0);
                        context.lineTo(0, box_height);
                        context.stroke();

                        context.beginPath();
                        context.moveTo(0, 0);
                        context.lineTo(box_width / 2, box_height / 2);
                        context.stroke();

                        this.chords.prepend(canvas);

                        break;

                    case '1-1-1-1':

                        canvas = document.createElement('canvas');
                        context = canvas.getContext('2d');

                        canvas.style.position = 'absolute';
                        canvas.width = box_width;
                        canvas.height = box_height;

                        context.lineWidth = border_width;

                        context.beginPath();
                        context.moveTo(box_width, 0);
                        context.lineTo(0, box_height);
                        context.stroke();

                        context.beginPath();
                        context.moveTo(0, 0);
                        context.lineTo(box_width, box_height);
                        context.stroke();

                        this.chords.prepend(canvas);

                        break;

                }

            }

        });

    }
);
