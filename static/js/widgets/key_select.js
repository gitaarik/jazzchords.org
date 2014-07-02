define(['init/all_keys'], function(allKeys) {

    function KeySelect(key_select_el, delegate) {

        this.tonic = 'C';
        this.tonality = 1;

        this.key_select_el = key_select_el;
        this.tonic_el = this.key_select_el.find('.tonic');
        this.tonic_currently_selected_el = this.tonic_el.find('.currently-selected');
        this.tonic_choices_el = this.tonic_el.find('.tonic-choices');
        this.tonality_el = this.key_select_el.find('.tonality');
        this.tonality_text_el = this.tonality_el.find('span');

        this.delegate = delegate;

        this.initKeyTonic();
        this.initKeyTonality();

        return this;

    }

    KeySelect.prototype.initKeyTonic = function() {

        var that = this;

        this.tonic_currently_selected_el.click(function() {
            that.tonic_choices_el.toggle();
        });

        this.tonic_el.find('.tonic-choices ul li').click(function(el) {
            var tonic = $(el.target).data('tonic');
            that.updateTonic(tonic);
            that.updateKey();
        });

        $('html').click(function(el) {

            if (
                !$(el.target).closest('.tonic').length &&
                !$(el.target).closest('.tonic-choices').length
            ) {
                that.tonic_choices_el.hide();
            }

        });

    };

    KeySelect.prototype.initKeyTonality = function() {

        var that = this;

        this.tonality_el.click(function() {

            var tonality;

            if (that.tonality_text_el.html() == 'Major') {
                tonality = 2;
            } else {
                tonality = 1;
            }

            that.updateTonality(tonality);
            that.updateKey();

        });

    };

    KeySelect.prototype.updateTonic = function(tonic) {

        this.tonic = tonic;
        this.tonic_currently_selected_el.html(this.tonic);

        this.tonic_choices_el.find('li.selected').removeClass('selected');
        this.tonic_choices_el.find(
            'li[data-tonic=' + this.tonic + ']'
        ).addClass('selected');
        this.tonic_choices_el.hide();

    };

    KeySelect.prototype.updateTonality = function(tonality) {

        this.tonality = tonality;

        if (this.tonality == 1) {
            tonality_text = 'Major';
        } else {
            tonality_text = 'Minor';
        }

        this.tonality_text_el.html(tonality_text);

    };

    KeySelect.prototype.updateKey = function() {

        this.delegate.key_changed(
            allKeys.findWhere({
                tonic: this.tonic,
                tonality: this.tonality
            })
        );

    };

    return KeySelect;

});
