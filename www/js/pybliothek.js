(function($) {

    var Book = Backbone.Model.extend({
        defaults : {
            db_id : null,
            isbn : null,
            author : null,
            title : null,
            inserted : null
        }
    });

    var BookList = Backbone.Collection.extend({
        model : Book
    });

    // line in the table
    var BookView = Backbone.View.extend({
        tagName : 'tr',
        template : $('#template .tmpl_book table tr').template(),
        render : function() {

            $(this.el).html($.tmpl(this.template, this.model.toJSON()));
            return this;
        }
    });

    var BookAddView = Backbone.View.extend({
        el : $('#modal_book_add'), // .template(),

        events : {
            'click button#submit' : 'submit',
            'click button#cancel' : 'cancel'
        },

        initialize : function() {
            _.bindAll(this, 'openNew', 'submit', 'cancel');

            // var el = $.tmpl(this.template);
            this.el = $(this.el).modal({
                'show' : false
            });
            // this.el = el;
        },

        openNew : function() {
            console.log($('#float_placeholder'));

            // $('#float_placeholder').append (el);
            this.el.modal('show');
        },
        submit : function() {
            this.el.modal('hide');
        },
        cancel : function() {
            this.el.modal('hide');
        }
    });

    var PybliothekView = Backbone.View.extend({
        el : $('#tbl_placeholder'),
        template : $('#template .tmpl_book_list').template(),
        initialize : function() {

            _.bindAll(this, 'load', 'updateContent', 'render');

            this.collection = new BookList();
            this.collection.bind('reset', this.render);

            // we hold one modal only
            this.bookAddView = new BookAddView();
        },

        events : {
            'click button#refresh' : 'load',
            'click button#add' : 'addBook'
        },

        addBook : function() {
            this.bookAddView.openNew();
        },

        buildBookFromJSON : function(d) {
            var b = new Book();

            b.set({
                isbn : d.isbn,
                author : d.author,
                title : d.title,
                id : d.id
            });
            return b;
        },
        updateContent : function(data) {
            console.log('update');
            this.collection.reset(_.map(JSON.parse(data),
                    this.buildBookFromJSON));
        },

        render : function() {

            $(this.el).html($.tmpl(this.template));
            _(this.collection.models).each(function(i) {
                var bv = new BookView({
                    model : i
                });
                $('.list', this.el).append(bv.render().el);
            });

            console.log('render');
        },

        load : function() {
            $.ajax({
                type : 'GET',
                url : '/book',
                success : this.updateContent
            });
        }
    });

    var pybliothek = new PybliothekView();
    pybliothek.load();

})(jQuery);
