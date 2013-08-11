define(
    ['models/edit_widget_chord_type'],
    function(EditWidgetChordType) {

        return Backbone.View.extend({

            model: EditWidgetChordType,

            initialize: function() {
                this.listenTo(this.model, 'change', this.render)
            },

            events: {
                'click': 'chooseSymbol'
            },

            chooseSymbol: function() {
                this.model.get('editWidget').set('chord_type',
                    this.model.get('chord_type'))
            },

            render: function() {

                this.$el.html(this.model.get('symbol'))

                if(this.model.get('selected')) {
                    this.$el.addClass('selected')
                }
                else {
                    this.$el.removeClass('selected')
                }

            }

        })

    }
)
