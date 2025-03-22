"""Web interface for the paperscraper application."""
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired
import os
from datetime import datetime
import pandas as pd

from .api import OpenAlexClient
from .export import export_papers_to_csv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

class SearchForm(FlaskForm):
    """Form for paper search."""
    search_terms = TextAreaField('Search Terms (one per line)', validators=[DataRequired()])
    recent_only = BooleanField('Only show papers from the last 10 years')
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page with search form."""
    form = SearchForm()
    if form.validate_on_submit():
        # Split search terms and remove empty lines
        search_terms = [term.strip() for term in form.search_terms.data.split('\n') if term.strip()]
        if not search_terms:
            flash('Please enter at least one search term', 'error')
            return redirect(url_for('index'))
            
        # Calculate minimum year if recent_only is checked
        min_year = None
        if form.recent_only.data:
            min_year = datetime.now().year - 10
            print(f"Setting minimum year to: {min_year}")
            
        return redirect(url_for('search', terms=','.join(search_terms), min_year=min_year))
    return render_template('index.html', form=form)

@app.route('/search')
def search():
    """Search results page."""
    terms = request.args.get('terms', '').split(',')
    min_year = request.args.get('min_year', type=int)
    
    if not terms or not terms[0]:
        flash('Please enter at least one search term', 'error')
        return redirect(url_for('index'))

    try:
        client = OpenAlexClient()
        all_papers = []
        
        for term in terms:
            print(f"\nProcessing search term: {term}")
            papers = client.get_top_cited_papers(term, min_year=min_year)
            all_papers.extend(papers)
            
        if not all_papers:
            flash('No papers found matching your search criteria', 'warning')
            return redirect(url_for('index'))
            
        # Export all papers to CSV
        output_file = export_papers_to_csv(all_papers, "batch_search")
        
        return render_template('results.html', 
                             papers=all_papers, 
                             query=", ".join(terms),
                             output_file=output_file,
                             min_year=min_year)
    except Exception as e:
        print(f"Error during search: {str(e)}")
        flash(f'Error performing search: {str(e)}', 'error')
        return redirect(url_for('index'))

def run_app(debug=True):
    """Run the Flask application."""
    app.run(debug=debug) 