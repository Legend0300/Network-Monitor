#!/usr/bin/env python3
"""
Test Network Process - Creates network activity for testing the dashboard
Enhanced to show blocking behavior with continuous connection attempts
"""

import requests
import time
import threading
import socket
from datetime import datetime

class NetworkTestProcess:
    def __init__(self):
        self.running = True
        self.request_count = 0
        self.failed_requests = 0
        self.blocked_detected = False
        
    def continuous_http_requests(self):
        """Make continuous HTTP requests to test network activity - keeps trying even when blocked"""
        urls = [
            'https://httpbin.org/json',
            'https://api.github.com/users/github',
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://httpbin.org/uuid',
            'https://api.github.com/repos/python/cpython'
        ]
        
        consecutive_failures = 0
        
        while self.running:
            try:
                for url in urls:
                    if not self.running:
                        break
                    
                    try:
                        response = requests.get(url, timeout=5)
                        self.request_count += 1
                        consecutive_failures = 0
                        self.blocked_detected = False
                        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] SUCCESS: GET {url} - Status: {response.status_code} - Total: {self.request_count}")
                        
                    except requests.exceptions.ConnectionError as e:
                        self.failed_requests += 1
                        consecutive_failures += 1
                        if consecutive_failures >= 3:
                            self.blocked_detected = True
                        print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] CONNECTION BLOCKED/FAILED: {url}")
                        print(f"   └─ Error: {str(e)[:100]}...")
                        print(f"   └─ Failed attempts: {self.failed_requests} | Consecutive failures: {consecutive_failures}")
                        if self.blocked_detected:
                            print(f"   └─ ⚠️  NETWORK BLOCKING DETECTED - Process appears to be blocked from internet access")
                        
                    except requests.exceptions.Timeout as e:
                        self.failed_requests += 1
                        consecutive_failures += 1
                        print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] TIMEOUT: {url} - Request timed out after 5 seconds")
                        print(f"   └─ This could indicate network blocking or slow connection")
                        
                    except Exception as e:
                        self.failed_requests += 1
                        consecutive_failures += 1
                        print(f"💥 [{datetime.now().strftime('%H:%M:%S')}] UNEXPECTED ERROR: {url}")
                        print(f"   └─ Error: {str(e)}")
                    
                    # Always wait between requests, blocked or not
                    time.sleep(1.5)
                    
            except Exception as e:
                print(f"🚨 [{datetime.now().strftime('%H:%M:%S')}] CRITICAL HTTP ERROR: {e}")
                time.sleep(3)
    
    def tcp_connections(self):
        """Create TCP connections to various servers - keeps trying even when blocked"""
        servers = [
            ('google.com', 80),
            ('github.com', 80),
            ('stackoverflow.com', 80),
            ('httpbin.org', 80),
            ('api.github.com', 443)
        ]
        
        consecutive_tcp_failures = 0
        
        while self.running:
            try:
                for host, port in servers:
                    if not self.running:
                        break
                    
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(5)
                        start_time = time.time()
                        result = sock.connect_ex((host, port))
                        end_time = time.time()
                        
                        if result == 0:
                            consecutive_tcp_failures = 0
                            print(f"🔗 [{datetime.now().strftime('%H:%M:%S')}] TCP SUCCESS: {host}:{port} (Connected in {end_time-start_time:.2f}s)")
                        else:
                            consecutive_tcp_failures += 1
                            print(f"🚫 [{datetime.now().strftime('%H:%M:%S')}] TCP FAILED: {host}:{port} - Error code: {result}")
                            print(f"   └─ Connection refused or blocked - Consecutive TCP failures: {consecutive_tcp_failures}")
                            if consecutive_tcp_failures >= 5:
                                print(f"   └─ ⚠️  TCP BLOCKING DETECTED - Multiple consecutive TCP connection failures")
                        
                        sock.close()
                        
                    except socket.timeout:
                        consecutive_tcp_failures += 1
                        print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] TCP TIMEOUT: {host}:{port} - Connection timed out")
                        print(f"   └─ This indicates network blocking or firewall interference")
                        
                    except Exception as e:
                        consecutive_tcp_failures += 1
                        print(f"💥 [{datetime.now().strftime('%H:%M:%S')}] TCP ERROR: {host}:{port} - {str(e)}")
                        
                    time.sleep(2)
                    
            except Exception as e:
                print(f"🚨 [{datetime.now().strftime('%H:%M:%S')}] CRITICAL TCP ERROR: {e}")
                time.sleep(3)
    
    def status_reporter(self):
        """Reports connection status every 10 seconds"""
        while self.running:
            time.sleep(10)
            if not self.running:
                break
                
            print(f"\n📊 [{datetime.now().strftime('%H:%M:%S')}] STATUS REPORT:")
            print(f"   ├─ Successful HTTP requests: {self.request_count}")
            print(f"   ├─ Failed requests: {self.failed_requests}")
            print(f"   ├─ Success rate: {(self.request_count / max(self.request_count + self.failed_requests, 1) * 100):.1f}%")
            print(f"   └─ Blocking detected: {'YES' if self.blocked_detected else 'NO'}")
            
            if self.blocked_detected:
                print(f"   └─ 🔴 NETWORK ACCESS APPEARS TO BE BLOCKED")
            else:
                print(f"   └─ 🟢 NETWORK ACCESS IS WORKING")
            print("=" * 60)
    
    def start(self):
        """Start the test process with multiple network activities"""
        print("🌐 Enhanced Network Test Process Starting...")
        print("📋 This process demonstrates network blocking behavior:")
        print("   • Continuously attempts HTTP requests")
        print("   • Tries TCP connections to multiple servers") 
        print("   • Shows detailed error messages when blocked")
        print("   • Keeps trying even when internet access is blocked")
        print("   • Reports status every 10 seconds")
        print("\n🎯 Use your network dashboard to:")
        print("   • Block this process (will show blocking behavior)")
        print("   • Unblock after 10 seconds (automatic)")
        print("   • Pause/Resume/Kill this process")
        print("=" * 60)
        
        # Start HTTP requests in one thread
        http_thread = threading.Thread(target=self.continuous_http_requests, daemon=True)
        http_thread.start()
        
        # Start TCP connections in another thread  
        tcp_thread = threading.Thread(target=self.tcp_connections, daemon=True)
        tcp_thread.start()
        
        # Start status reporter
        status_thread = threading.Thread(target=self.status_reporter, daemon=True)
        status_thread.start()
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping network test process...")
            self.running = False
            print("✅ Process stopped gracefully.")

if __name__ == "__main__":
    test_process = NetworkTestProcess()
    test_process.start()