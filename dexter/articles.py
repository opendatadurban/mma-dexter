import logging
log = logging.getLogger(__name__)

from flask import request, url_for, flash, redirect
from flask.ext.mako import render_template

from .app import app
from .models import db, Document, Issue
from .models.document import DocumentForm, DocumentAnalysisForm
from .models.source import DocumentSourceForm
from .models.author import AuthorForm

from .processing import DocumentProcessor, ProcessingError

@app.route('/articles/<id>')
def show_article(id):
    document = Document.query.get_or_404(id)
    return render_template('articles/show.haml',
            document=document)
 

@app.route('/articles/new', methods=['GET', 'POST'])
def new_article():
    form = DocumentForm()
    author_form = AuthorForm(prefix='author', csrf_enabled=False)

    form.url.data = form.url.data or request.args.get('url')
    url = form.url.data

    if request.method == 'POST':
        doc = None
        proc = DocumentProcessor()

        if url and not 'manual' in request.form:
            # new document from url
            if not proc.valid_url(url):
                flash("The URL isn't valid or we don't know how to process it.", 'error')
            else:
                url = proc.canonicalise_url(url)
                doc = Document.query.filter(Document.url == url).first()

                if doc:
                    # already exists
                    flash("We already have that article.")
                    return redirect(url_for('show_article', id=doc.id))
                else:
                    try:
                        doc = proc.process_url(url)
                    except ProcessingError as e:
                        log.error("Error processing %s: %s" % (url, e), exc_info=e)
                        flash("Something went wrong processing the document: %s" % (e,), 'error')
        else:
            # new document from article text
            if author_form.validate():
                # link author
                form.author_id.data = author_form.get_or_create_author().id

                if form.validate():
                    doc = Document()
                    form.populate_obj(doc)

                    try:
                        proc.process_document(doc)
                    except ProcessingError as e:
                        log.error("Error processing raw document: %s" % (e, ), exc_info=e)
                        flash("Something went wrong processing the document: %s" % (e,), 'error')
                        doc = None

        if doc:
            db.session.add(doc)
            db.session.flush()
            id = doc.id
            db.session.commit()
            flash('Article added.')
            return redirect(url_for('edit_article_analysis', id=id))
        
    return render_template('articles/new.haml',
            url=url,
            form=form,
            author_form=author_form)


@app.route('/articles/<id>/edit', methods=['GET', 'POST'])
def edit_article(id):
    doc = Document.query.get_or_404(id)
    form = DocumentForm(obj=doc)

    author_form = AuthorForm(prefix='author', csrf_enabled=False, obj=doc.author)

    if request.method == 'POST':
        if author_form.validate():
            # link author
            form.author_id.data = author_form.get_or_create_author().id
            if form.validate():
                form.populate_obj(doc)
                db.session.commit()
                flash('Article updated.')
                return redirect(url_for('show_article', id=id))
    else:
        author_form.person_race_id.data = doc.author.person.race.id if doc.author.person and doc.author.person.race else None
        author_form.person_gender_id.data = doc.author.person.gender.id if doc.author.person and doc.author.person.gender else None

    return render_template('articles/edit.haml',
            doc=doc,
            form=form,
            author_form=author_form)

@app.route('/articles/<id>/analysis', methods=['GET', 'POST'])
def edit_article_analysis(id):
    document = Document.query.get_or_404(id)
    form = DocumentAnalysisForm(obj=document)
    new_sources = []

    # in the page, the fields for all new sources will be transformed into
    # 'source-new[0]-name'. This form is used as a template for these
    # new source forms.
    new_source_form = DocumentSourceForm(prefix='source-new', csrf_enabled=False)

    if request.method == 'POST':
        # find new sources and build forms for them.
        # the field names are like: source-new[2]-person_name
        for key in sorted(set('-'.join(key.split('-', 3)[0:2]) for key in request.form.keys() if key.startswith('source-new['))):
            src_form = DocumentSourceForm(prefix=key)
            # skip new sources that have an empty name
            if src_form.person_name.data != '':
                new_sources.append(src_form)

        forms = [form] + new_sources
        if all(f.validate() for f in forms):
            # convert issue id's to Issue objects
            form.issues.data = [Issue.query.get_or_404(i) for i in form.issues.data]

            # update document
            form.populate_obj(document)

            # convert from empty values back into None
            if not document.topic_id:
                document.topic_id = None
            if not document.origin_location_id:
                document.origin_location_id = None

            # save new sources
            for f in new_sources:
                src = DocumentSource()
                src.document = document
                f.populate_obj(src)
                # TODO: entity id

            db.session.commit()
            flash('Analysis updated.')
            return redirect(url_for('show_article', id=id))
        else:
            flash('Please correct the problems below and try again.')
    else:
        # TODO: wtforms turns None values into None, which sucks
        if form.topic_id.data == 'None':
            form.topic_id.data = ''
        if form.origin_location_id.data == 'None':
            form.origin_location_id.data = ''
        # ensure that checkboxes can be pre-populated
        form.issues.data = [str(i.id) for i in document.issues]

    return render_template('articles/edit_analysis.haml',
            form=form,
            new_source_form=new_source_form,
            new_sources=new_sources,
            document=document)
