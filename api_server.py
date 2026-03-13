#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iran Cities API Server
A simple Flask API server for Iranian provinces and cities data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load data
DATA_FILE = 'iran_cities.json'

def load_data():
    """Load Iran cities data from JSON file"""
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load data on startup
iran_data = load_data()

@app.route('/')
def home():
    """API home page"""
    return jsonify({
        'message': 'Iran Cities API',
        'version': '2.0.0',
        'endpoints': {
            'provinces': '/api/provinces',
            'province_by_id': '/api/provinces/<id>',
            'cities': '/api/cities',
            'city_by_id': '/api/cities/<id>',
            'search': '/api/search?q=<query>'
        }
    })

@app.route('/api/provinces', methods=['GET'])
def get_provinces():
    """Get all provinces"""
    provinces = [{
        'id': p['id'],
        'province': p['province'],
        'english_name': p['english_name'],
        'phone_code': p['phone_code'],
        'cities_count': p['cities_count']
    } for p in iran_data]
    
    return jsonify({
        'success': True,
        'count': len(provinces),
        'data': provinces
    })

@app.route('/api/provinces/<int:province_id>', methods=['GET'])
def get_province(province_id):
    """Get a specific province by ID"""
    province = next((p for p in iran_data if p['id'] == province_id), None)
    
    if province:
        return jsonify({
            'success': True,
            'data': province
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Province not found'
        }), 404


@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Get all cities"""
    all_cities = []
    for province in iran_data:
        for city in province['cities']:
            city_data = city.copy()
            city_data['province_id'] = province['id']
            city_data['province_name'] = province['province']
            all_cities.append(city_data)
    
    return jsonify({
        'success': True,
        'count': len(all_cities),
        'data': all_cities
    })

@app.route('/api/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    """Get a specific city by ID"""
    for province in iran_data:
        city = next((c for c in province['cities'] if c['id'] == city_id), None)
        if city:
            city_data = city.copy()
            city_data['province_id'] = province['id']
            city_data['province_name'] = province['province']
            return jsonify({
                'success': True,
                'data': city_data
            })
    
    return jsonify({
        'success': False,
        'message': 'City not found'
    }), 404

@app.route('/api/search', methods=['GET'])
def search():
    """Search in provinces and cities"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'Query parameter "q" is required'
        }), 400
    
    results = {
        'provinces': [],
        'cities': []
    }
    
    # Search in provinces
    for province in iran_data:
        if (query in province['province'].lower() or 
            query in province['english_name'].lower()):
            results['provinces'].append({
                'id': province['id'],
                'province': province['province'],
                'english_name': province['english_name']
            })
        
        # Search in cities
        for city in province['cities']:
            if (query in city['name'].lower() or 
                query in city.get('english_name', '').lower()):
                results['cities'].append({
                    'id': city['id'],
                    'name': city['name'],
                    'english_name': city.get('english_name', ''),
                    'province': province['province']
                })
    
    return jsonify({
        'success': True,
        'query': query,
        'results': results,
        'total': len(results['provinces']) + len(results['cities'])
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print('🚀 Iran Cities API Server')
    print('📡 Server running on http://localhost:8000')
    print('📚 API Documentation: http://localhost:8000')
    print('\nAvailable endpoints:')
    print('  GET /api/provinces')
    print('  GET /api/provinces/<id>')
    print('  GET /api/cities')
    print('  GET /api/cities/<id>')
    print('  GET /api/search?q=<query>')
    print('\nPress Ctrl+C to stop the server\n')
    
    app.run(host='0.0.0.0', port=8000, debug=True)
