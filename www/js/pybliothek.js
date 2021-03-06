(function($) {

    var Book = Backbone.Model.extend({
        defaults : {
            db_id : null,
            isbn : null,
            author : null,
            title : null,
            inserted : null,
            publisher : null
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
            'click a#lookup' : 'lookup',
            'click a#add' : 'add',
            'click a#cancel' : 'cancel'
        },

        initialize : function() {
            _.bindAll(this, 'openNew', 'lookup', 'fillLookupData', 'add',
                    'cancel');

            this.el = $(this.el).modal({
                'show' : false
            });

            // book to be filled on lookup
            // this.model = new Book();
            // this.model.bind('reset', this.render);
        },

        openNew : function() {
            // console.log($('#float_placeholder'));
            this.el.modal('show');
        },
        lookup : function() {
            console.log($('#fld_isbn').val());
            $.ajax({
                type : 'GET',
                url : '/lookup',
                data : {
                    'isbn' : $('#fld_isbn').val()
                },
                success : this.fillLookupData
            });
        },
        fillLookupData : function(data) {
            var d = JSON.parse(data);

            $('#modal_book_add #title').val (d.title);
            $('#modal_book_add #author').val (d.author);
            $('#modal_book_add #publisher').val (d.publisher);

        },
        add : function() {
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
            'click a#refresh' : 'load',
            'click a#add' : 'addBook'
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
                id : d.id,
                publisher : d.publisher
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
                url : '/catalog',
                success : this.updateContent
            });
        }
    });

    var pybliothek = new PybliothekView();
    pybliothek.load();

})(jQuery);
