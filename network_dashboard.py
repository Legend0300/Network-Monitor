#!/usr/bin/env python3
"""
Simple Network Dashboard - Shows apps using internet with basic control
"""

import psutil
from flask import Flask, render_template, jsonify, request
import ipaddress
from datetime import datetime
import threading
import time
import subprocess
import os

app = Flask(__name__)

# Store blocked processes with timeout info
blocked_processes = {}
timeout_threads = {}

def is_local_ip(ip):
    """Check if IP is local/private"""
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local
    except:
        return True

def get_process_details(pid):
    """Get basic process information"""
    try:
        process = psutil.Process(pid)
        timeout_remaining = 0
        if pid in blocked_processes:
            elapsed = time.time() - blocked_processes[pid]['blocked_at']
            timeout_remaining = max(0, 5 - elapsed)
        
        return {
            'cpu_percent': round(process.cpu_percent(), 1),
            'memory_mb': round(process.memory_info().rss / 1024 / 1024, 1),
            'status': process.status(),
            'is_blocked': pid in blocked_processes,
            'timeout_remaining': round(timeout_remaining, 1) if timeout_remaining > 0 else 0
        }
    except:
        return {'cpu_percent': 0, 'memory_mb': 0, 'status': 'unknown', 'is_blocked': False, 'timeout_remaining': 0}

def auto_unblock_process(pid):
    """Auto-unblock process after 5 seconds"""
    time.sleep(5)
    try:
        if pid in blocked_processes:
            # Resume the process instead of using iptables
            process_name = blocked_processes[pid]['name']
            try:
                process = psutil.Process(pid)
                process.resume()
                print(f"Auto-unblocked process {pid} ({process_name}) after 5 seconds")
            except:
                pass
            del blocked_processes[pid]
        if pid in timeout_threads:
            del timeout_threads[pid]
    except Exception as e:
        print(f"Failed to auto-unblock process {pid}: {e}")
        if pid in blocked_processes:
            del blocked_processes[pid]
        if pid in timeout_threads:
            del timeout_threads[pid]

def block_process(pid):
    """Block network access for a process by suspending it with 5-second auto-unblock"""
    try:
        process = psutil.Process(pid)
        if pid not in blocked_processes:
            # Suspend the process instead of using iptables
            process.suspend()
            
            blocked_processes[pid] = {
                'name': process.name(),
                'blocked_at': time.time()
            }
            
            # Start timeout thread
            timeout_thread = threading.Thread(target=auto_unblock_process, args=(pid,), daemon=True)
            timeout_threads[pid] = timeout_thread
            timeout_thread.start()
            
            return True, f"Process suspended (will auto-resume in 5 seconds)"
        return False, "Already blocked"
    except Exception as e:
        return False, f"Failed to suspend process: {e}"

def unblock_process(pid):
    """Unblock network access for a process manually by resuming it"""
    try:
        process = psutil.Process(pid)
        if pid in blocked_processes:
            # Resume the process
            process.resume()
            
            del blocked_processes[pid]
            # Cancel timeout thread
            if pid in timeout_threads:
                del timeout_threads[pid]
            return True, f"Process resumed"
        return False, "Not blocked"
    except Exception as e:
        return False, f"Failed to resume process: {e}"

def kill_process(pid):
    """Kill a process"""
    try:
        process = psutil.Process(pid)
        # Clean up any blocks first
        if pid in blocked_processes:
            del blocked_processes[pid]
        if pid in timeout_threads:
            del timeout_threads[pid]
        
        process.terminate()
        return True, f"Process terminated"
    except Exception as e:
        return False, f"Failed to terminate: {e}"

def get_network_apps():
    """Get apps using internet"""
    apps = {}
    
    try:
        for conn in psutil.net_connections(kind='inet'):
            if not conn.pid or not conn.raddr or is_local_ip(conn.raddr.ip):
                continue
            
            try:
                process = psutil.Process(conn.pid)
                name = process.name()
                
                if name not in apps:
                    apps[name] = {
                        'name': name,
                        'pid': conn.pid,
                        'connections': 0,
                        'details': get_process_details(conn.pid)
                    }
                
                apps[name]['connections'] += 1
                
            except:
                continue
    except:
        return {"error": "Permission denied"}
    
    return list(apps.values())

@app.route('/')
def index():
    return render_template('network_dashboard.html')

@app.route('/api/apps')
def get_apps():
    return jsonify(get_network_apps())

@app.route('/api/control/<int:pid>', methods=['POST'])
def control_process(pid):
    action = request.json.get('action')
    
    if action == 'block':
        success, message = block_process(pid)
    elif action == 'unblock':
        success, message = unblock_process(pid)
    elif action == 'kill':
        success, message = kill_process(pid)
    else:
        return jsonify({'success': False, 'message': 'Invalid action'})
    
    return jsonify({'success': success, 'message': message})

def cleanup_iptables():
    """Clean up any leftover iptables rules on startup"""
    try:
        # Remove any existing rules that might match our pattern
        subprocess.run("sudo iptables -S OUTPUT | grep 'owner --pid-owner' | sed 's/-A/-D/' | while read rule; do sudo iptables $rule 2>/dev/null || true; done", shell=True, capture_output=True)
        print("Cleaned up any existing iptables rules")
    except Exception as e:
        print(f"Warning: Could not clean up iptables rules: {e}")

if __name__ == '__main__':
    print("🌐 Simple Network Dashboard")
    print("🚫 Network blocking mode - suspends processes instead of blocking network")
    print("📝 Blocked processes auto-resume after 5 seconds")
    print("Access at: http://localhost:5000")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)