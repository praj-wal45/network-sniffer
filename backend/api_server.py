"""
Network Sniffer - Flask REST API Server

Provides REST endpoints for packet capture, retrieval, filtering, and analysis.
Integrates with the Sniffer core engine for real-time packet capture.

Author: Network Sniffer Team
Version: 1.0.0
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Tuple

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

from backend.sniffer import get_sniffer
from utils.config import API_HOST, API_PORT, DEBUG_MODE
from utils.logger import setup_logger

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup logger
logger = setup_logger(__name__)

# Get global sniffer instance
sniffer = get_sniffer()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def success_response(data: Any = None, message: str = None, **kwargs) -> Dict:
    """Create a standardized success response."""
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    response.update(kwargs)
    return response


def error_response(message: str, code: int = 400, **kwargs) -> Tuple[Dict, int]:
    """Create a standardized error response."""
    response = {'success': False, 'message': message}
    response.update(kwargs)
    return response, code


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        200: {"status": "healthy", "message": "Network Sniffer API is running"}
    """
    return jsonify(success_response(
        message='Network Sniffer API is running',
        status='healthy',
        timestamp=datetime.now().isoformat()
    )), 200


@app.route('/api/sniffer/status', methods=['GET'])
def get_status():
    """
    Get current sniffer status.
    
    Returns:
        200: {
            "success": true,
            "data": {
                "is_running": bool,
                "packets_captured": int,
                "status": "running" or "stopped"
            }
        }
    """
    stats = sniffer.get_statistics()
    return jsonify(success_response(
        data={
            'is_running': sniffer.is_sniffer_running(),
            'packets_captured': stats['packets_captured'],
            'status': 'running' if sniffer.is_sniffer_running() else 'stopped',
            'packet_buffer_size': stats['total_packets']
        }
    )), 200


# ============================================================================
# SNIFFER CONTROL ENDPOINTS
# ============================================================================

@app.route('/api/sniffer/start', methods=['POST'])
def start_sniffer():
    """
    Start packet sniffing.
    
    Request body:
        {
            "packet_count": 0  (optional, 0 = infinite)
        }
    
    Returns:
        200: {"success": true, "message": "Packet sniffing started"}
        400: If already running
        500: If error occurs
    """
    try:
        data = request.get_json() or {}
        packet_count = data.get('packet_count', 0)
        
        if sniffer.is_sniffer_running():
            return error_response('Sniffer is already running', 400)
        
        success = sniffer.start(packet_count=packet_count)
        
        if success:
            logger.info(f'Sniffer started (packet_count={packet_count})')
            return jsonify(success_response(
                message='Packet sniffing started',
                packet_count=packet_count
            )), 200
        else:
            return error_response('Failed to start sniffer', 500)
            
    except Exception as e:
        logger.error(f'Error starting sniffer: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


@app.route('/api/sniffer/stop', methods=['POST'])
def stop_sniffer():
    """
    Stop packet sniffing.
    
    Returns:
        200: {
            "success": true,
            "message": "Packet sniffing stopped",
            "packets_captured": int
        }
        400: If not running
        500: If error occurs
    """
    try:
        if not sniffer.is_sniffer_running():
            return error_response('Sniffer is not running', 400)
        
        packet_count = sniffer.stop()
        
        logger.info(f'Sniffer stopped - {packet_count} packets captured')
        return jsonify(success_response(
            message='Packet sniffing stopped',
            packets_captured=packet_count
        )), 200
        
    except Exception as e:
        logger.error(f'Error stopping sniffer: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


# ============================================================================
# PACKET RETRIEVAL ENDPOINTS
# ============================================================================

@app.route('/api/packets', methods=['GET'])
def get_packets():
    """
    Get captured packets with pagination.
    
    Query parameters:
        limit (int, optional): Packets per page (default: 50, max: 500)
        offset (int, optional): Starting position (default: 0)
    
    Returns:
        200: {
            "success": true,
            "data": [...packets...],
            "pagination": {
                "limit": int,
                "offset": int,
                "total": int
            }
        }
    """
    try:
        limit = min(int(request.args.get('limit', 50)), 500)
        offset = int(request.args.get('offset', 0))
        
        if limit < 1:
            return error_response('Limit must be greater than 0', 400)
        if offset < 0:
            return error_response('Offset cannot be negative', 400)
        
        packets = sniffer.get_packets(limit=limit, offset=offset)
        total = sniffer.get_packet_count()
        
        return jsonify(success_response(
            data=packets,
            pagination={
                'limit': limit,
                'offset': offset,
                'total': total
            }
        )), 200
        
    except ValueError:
        return error_response('Invalid limit or offset value', 400)
    except Exception as e:
        logger.error(f'Error retrieving packets: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


@app.route('/api/packets/filter', methods=['GET'])
def filter_packets():
    """
    Filter captured packets by criteria.
    
    Query parameters:
        src_ip (string, optional): Filter by source IP
        dest_ip (string, optional): Filter by destination IP
        protocol (string, optional): Filter by protocol (TCP, UDP, ICMP, etc.)
    
    Returns:
        200: {
            "success": true,
            "data": [...filtered_packets...],
            "count": int
        }
    """
    try:
        src_ip = request.args.get('src_ip')
        dest_ip = request.args.get('dest_ip')
        protocol = request.args.get('protocol')
        
        packets = sniffer.filter_packets(src_ip=src_ip, dest_ip=dest_ip, protocol=protocol)
        
        logger.info(f'Filtered packets: src_ip={src_ip}, dest_ip={dest_ip}, protocol={protocol} -> {len(packets)} results')
        
        return jsonify(success_response(
            data=packets,
            count=len(packets),
            filters={
                'src_ip': src_ip,
                'dest_ip': dest_ip,
                'protocol': protocol
            }
        )), 200
        
    except Exception as e:
        logger.error(f'Error filtering packets: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


@app.route('/api/packets/search', methods=['GET'])
def search_packets():
    """
    Search packets by IP address or protocol.
    
    Query parameters:
        q (string, required): Search query (IP or protocol name)
    
    Returns:
        200: {
            "success": true,
            "data": [...search_results...],
            "count": int,
            "query": string
        }
        400: If search query is missing
    """
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return error_response('Search query parameter "q" is required', 400)
        
        packets = sniffer.search_packets(query)
        
        logger.info(f'Packet search: "{query}" -> {len(packets)} results')
        
        return jsonify(success_response(
            data=packets,
            count=len(packets),
            query=query
        )), 200
        
    except Exception as e:
        logger.error(f'Error searching packets: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


# ============================================================================
# STATISTICS ENDPOINT
# ============================================================================

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get aggregated traffic statistics.
    
    Returns:
        200: {
            "success": true,
            "data": {
                "total_packets": int,
                "protocols": {protocol: count, ...},
                "top_sources": [{ip: string, count: int}, ...],
                "top_destinations": [{ip: string, count: int}, ...]
            }
        }
    """
    try:
        stats = sniffer.get_statistics()
        
        return jsonify(success_response(data=stats)), 200
        
    except Exception as e:
        logger.error(f'Error getting statistics: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


# ============================================================================
# DATA MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/api/packets/clear', methods=['POST'])
def clear_packets():
    """
    Clear all captured packets from buffer.
    
    Returns:
        200: {
            "success": true,
            "message": "Packet buffer cleared",
            "packets_cleared": int
        }
        500: If error occurs
    """
    try:
        count = sniffer.clear_packets()
        
        logger.info(f'Cleared {count} packets from buffer')
        
        return jsonify(success_response(
            message='Packet buffer cleared',
            packets_cleared=count
        )), 200
        
    except Exception as e:
        logger.error(f'Error clearing packets: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


@app.route('/api/packets/export', methods=['GET'])
def export_packets():
    """
    Export captured packets as JSON.
    
    Query parameters:
        format (string, optional): Export format (default: json)
    
    Returns:
        200: {
            "success": true,
            "format": string,
            "count": int,
            "timestamp": string,
            "data": [...packets...]
        }
    """
    try:
        export_format = request.args.get('format', 'json').lower()
        
        if export_format not in ['json']:
            return error_response('Unsupported export format. Supported: json', 400)
        
        stats = sniffer.get_statistics()
        packets = sniffer.get_packets(limit=stats['total_packets'])
        
        export_data = {
            'success': True,
            'format': export_format,
            'timestamp': datetime.now().isoformat(),
            'count': len(packets),
            'metadata': {
                'total_packets': stats['total_packets'],
                'protocols': stats['protocols'],
                'top_sources': stats['top_sources'],
                'top_destinations': stats['top_destinations']
            },
            'data': packets
        }
        
        logger.info(f'Exported {len(packets)} packets in {export_format} format')
        
        return jsonify(export_data), 200
        
    except Exception as e:
        logger.error(f'Error exporting packets: {str(e)}')
        return error_response(f'Internal server error: {str(e)}', 500)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    return error_response('Endpoint not found', 404), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors."""
    return error_response('Method not allowed', 405), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server Error."""
    logger.error(f'Internal server error: {str(error)}')
    return error_response('Internal server error', 500), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    try:
        logger.info(f'Starting Network Sniffer API on {API_HOST}:{API_PORT}')
        logger.info(f'Debug mode: {DEBUG_MODE}')
        
        app.run(
            host=API_HOST,
            port=API_PORT,
            debug=DEBUG_MODE,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info('Shutting down...')
        if sniffer.is_sniffer_running():
            sniffer.stop()
    except Exception as e:
        logger.error(f'Fatal error: {str(e)}')
        raise
