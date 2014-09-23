var ChordEditNotes = require('../collections/chord_edit_notes.js');
var ChordEditChordTypes = require('../collections/chord_edit_chord_types.js');
var ChordEdit = require('../models/chord_edit.js');
var ChordEditNote = require('../models/chord_edit_note.js');
var chordTypes = require('../init/chord_types.js');
var allKeys = require('../../../core/widgets/all_keys.js');
var ChordEditNoteView = require('./chord_edit_note.js');
var ChordEditChordTypeView = require('./chord_edit_chord_type.js');


module.exports = Backbone.View.extend({

    model: ChordEdit,

    events: {
        'click header .close': 'close',
        'click .tabs li': 'switchTab',
        'click .chord-settings .setting.note .rest': 'useAsRest',
        'click .chord-settings .setting.type .toggle': 'toggleChordTypes',
        'click .chord-settings .setting.alt-bass-note .none': 'noAltBass'
    },

    initialize: function() {
        this.chord_type_el = this.$el.find('.chord-settings .setting.type');
        this.initChordTypes();
        this.listenTo(this.model, 'change', this.render);
    },

    render: function() {

        // Only show the edit widget when 'visible' is true,
        // otherwise, hide the edit widget.

        if (this.model.get('visible')) {

            var previousAttributes = this.model.previousAttributes();

            // If the edit widget was already open for this chord,
            // then apparently something else than the visibility
            // changed, so we apply the changes.
            if (
                previousAttributes.visible &&
                this.model.get('chord') == previousAttributes.chord
            ) {
                this.applyChanges();
            }

            this.show();

        } else {
            this.$el.hide();
        }

        return this;

    },

    initChordTypes: function() {
        // Creates the views for the chord type choices and binds them to
        // the existing HTML

        var that = this;
        this.chordEditChordTypes = new ChordEditChordTypes();

        chordTypes.each(function(chord_type) {
            that.chordEditChordTypes.add({
                chord_type: chord_type
            });
        });

        var number = 0;
        var chordEditChordType;

        this.chord_type_el.find('li').each(function() {

            chordEditChordType = that.chordEditChordTypes.models[number];
            chordEditChordType.set('editWidget', that.model);

            new ChordEditChordTypeView({
                el: this,
                model: chordEditChordType
            });

            number++;

        });

    },

    applyChanges: function() {
        // Applies the changes made in the edit widget to the chord

        var note = Boolean(this.model.get('note'));
        var alt_bass = Boolean(this.model.get('alt_bass_note'));

        var chord_data = {
            chord_type_id: this.model.get('chord_type').get('id'),
            alt_bass: alt_bass,
            rest: !note
        };

        if (note) {
            chord_data.chord_pitch = this.model.get('note').get(
                'distance_from_root'
            );
        }

        if (alt_bass) {
            chord_data.alt_bass_note = this.model.get('alt_bass_note');
            chord_data.alt_bass_pitch = (
                this.model.get('alt_bass_note').get('distance_from_root')
            );
        } else {
            chord_data.alt_bass_note = false;
        }

        this.model.get('chord').set(chord_data);
        this.model.get('chord').save();

    },

    close: function() {
        this.model.set('visible', false);
    },

    switchTab: function(obj) {
        // Switches to a tab in the edit widget
        // like 'note', 'type' and 'alt_bass_bass'

        var tab = $(obj.currentTarget);
        this.openTab(tab.data('key'));

    },

    openTab: function(key) {
        // Opens tab matching provided key

        this.$el.find('.tabs li').removeClass('active')
            .parent().find('li[data-key=' + key + ']')
            .addClass('active');

        this.$el.find('.chord-settings .setting').hide().parent().find(
            '.setting[data-key=' + key + ']'
        ).show();

    },

    /**
     * Sets this chord to be used as a rest.
     */
    useAsRest: function() {
        this.model.set('note', false);
    },

    /**
     * Toggles between the two pages of chord type options
     */
    toggleChordTypes: function(obj) {

        if (this.chord_type_el.find('.type-part-1').is(':visible')) {
            this.showChordTypePart(2);
        } else {
            this.showChordTypePart(1);
        }

    },

    noAltBass: function() {
        this.model.set('alt_bass_note', false);
    },

    showChordTypePart: function(number) {
        // Shows the chord type part of the provided number
        // The chord type choices are in these parts
        this.chord_type_el.find('.type-part').hide();
        this.chord_type_el.find('.type-part-' + number).show();
    },

    /**
     * Parses the settings on the model and render the html
     * accordingly.
     */
    show: function() {

        // If the edit widget opens on a different chord than the
        // last one, then reset the editWidget.
        if (
            this.model.previousAttributes().chord !=
            this.model.get('chord')
        ) {
            this.reset();
        }

        var offset = this.offset();

        this.$el.css({
            'top': this.model.get('offset').top + offset.top,
            'left': this.model.get('offset').left + offset.left
        });

        this.parseNotes();
        this.parseChordTypes();

        this.$el.show();

    },

    offset: function() {
        // Get the offset for the edit widget based on the chord it was
        // opened for.

        var beat_schema = this.model.get('chord')
            .get('measure').get('beat_schema');

        var off_top;
        var off_left;

        switch(beat_schema) {

            case '4':
                off_top = 85;
                off_left = -10;
                break;

            case '2-2':
                off_top = 60;
                off_left = -29;
                break;

            case '2-1-1':

                switch(this.model.get('chord').get('number')) {

                    case 1:
                        off_top = 60;
                        off_left = -29;
                        break;

                    case 2:
                        off_top = 47;
                        off_left = -9;
                        break;

                    case 3:
                        off_top = 77;
                        off_left = -39;
                        break;

                }

                break;

            case '1-1-2':

                switch(this.model.get('chord').get('number')) {

                    case 1:
                        off_top = 77;
                        off_left = -39;
                        break;

                    case 2:
                        off_top = 47;
                        off_left = -9;
                        break;

                    case 3:
                        off_top = 60;
                        off_left = -29;
                        break;

                }

                break;

            case '1-1-1-1':

                switch(this.model.get('chord').get('number')) {

                    case 1:
                        off_top = 77;
                        off_left = -39;
                        break;

                    case 2:
                        off_top = 47;
                        off_left = -9;
                        break;

                    case 3:
                        off_top = 47;
                        off_left = -9;
                        break;

                    case 4:
                        off_top = 77;
                        off_left = -39;
                        break;

                }

                break;

        }

        return {
            top: off_top,
            left: off_left
        };

    },

    /**
     * Parses the note and the alt bass note choices.
     */
    parseNotes: function() {

        var that = this;
        var note_types = ['note', 'alt_bass_note'];

        // If the notes are different from the last time, regenerate
        // the models/views.
        if (
            this.model.get('note_choices') !=
            this.model.previousAttributes().note_choices
        ) {

            that.editWidgetNotes = [];

            _.each(note_types, function(note_type) {

                that.editWidgetNotes[note_type] = new ChordEditNotes();
                var editWidgetNote;
                var note_choices = that.$el.find(
                    '.chord-settings ' +
                    '.setting[data-key=' + note_type + '] ul'
                );
                note_choices.html('');

                that.model.get('note_choices').each(function(note) {

                    editWidgetNote = new ChordEditNote({
                        note_id: note.get('id'), // used for `findWhere` later on
                        note: note,
                        note_type: note_type,
                        editWidget: that.model
                    });

                    that.editWidgetNotes[note_type].add(editWidgetNote);

                    note_choices.append(
                        new ChordEditNoteView({
                            model: editWidgetNote
                        }).render().el
                    );

                });

            });

        }

        // Select the correct note
        _.each(note_types, function(note_type) {

            // Deselect last selected if it exists
            var current_selected = (
                that.editWidgetNotes[note_type]
                .findWhere({ selected: true })
            );

            if (current_selected) {
                current_selected.set('selected', false);
            }

            // Select note if it is set (bass note doesn't have to be
            // set)

            var deselect_button = that.$el.find(
                '.chord-settings ' +
                '.setting[data-key=' + note_type + '] .deselect'
            );

            if (that.model.get(note_type)) {

                if (deselect_button) {
                    deselect_button.removeClass('selected');
                }

                that.editWidgetNotes[note_type].findWhere({
                    note_id: that.model.get(note_type).id
                }).set('selected', true);

            } else if (deselect_button) {
                deselect_button.addClass('selected');
            }

        });

    },

    parseChordTypes: function() {
        // Select the correct chord type

        var that = this;
        var current_selected = this.chordEditChordTypes.findWhere({
            selected: true
        });

        if (current_selected) {
            current_selected.set('selected', false);
        }

        this.chordEditChordTypes.find(function(chordEditChordType) {
            return (
                chordEditChordType.get('chord_type').get('id') ==
                that.model.get('chord_type').get('id')
            );
        }).set('selected', true);

    },

    /**
     * Resets the edit widget to the "start state".
     *
     * For example, the chosen chord is the chord the edit is on and
     * the selected tab is the note tab.
     */
    reset: function() {

        var chord = this.model.get('chord');
        var rest = chord.get('rest');
        var note;

        if (rest) {
            note = false;
        } else {
            note = chord.get('note');
        }

        this.model.set({
            note: note,
            chord_type: chord.get('chord_type'),
            alt_bass: chord.get('alt_bass'),
            alt_bass_note: chord.get('alt_bass_note'),
            rest: rest,
            note_choices: (
                allKeys.findWhere({
                    id: chord.get('key_id')
                }).get('notes')
            )
        });

        // Show the chord type part that has the curent selected chord
        // type.
        var current_chord_type = this.chordEditChordTypes.findWhere({
            chord_type: this.model.get('chord_type')
        });

        if (this.chordEditChordTypes.indexOf(current_chord_type) > 11) {
            this.showChordTypePart(2);
        } else {
            this.showChordTypePart(1);
        }

        this.openTab('note');

    }

});