"""
Page routes (landing, app interface)
"""

from flask import Blueprint, render_template

page_bp = Blueprint('pages', __name__)


@page_bp.route('/')
def index():
    """Serve the landing page"""
    return render_template('landing.html')


@page_bp.route('/app')
def app_index():
    """Serve the chat application"""
    return render_template('index.html')
