#!/bin/bash
# Network Traffic Blocker - Block all outbound traffic

ACTION=${1:-block}

if [ "$ACTION" = "block" ]; then
    echo "Blocking all outbound network traffic..."
    
    # Block all outbound traffic except loopback
    sudo iptables -A OUTPUT -o lo -j ACCEPT
    sudo iptables -A OUTPUT -j DROP
    
    echo "✓ All outbound network traffic blocked"
    echo "Use '$0 unblock' to restore network access"
    
elif [ "$ACTION" = "unblock" ]; then
    echo "Restoring network access..."
    
    # Remove the blocking rules
    sudo iptables -D OUTPUT -o lo -j ACCEPT 2>/dev/null
    sudo iptables -D OUTPUT -j DROP 2>/dev/null
    
    echo "✓ Network access restored"
    
elif [ "$ACTION" = "status" ]; then
    echo "Current iptables OUTPUT rules:"
    sudo iptables -L OUTPUT -n
    
else
    echo "Usage: $0 [block|unblock|status]"
    echo "  block   - Block all outbound network traffic"
    echo "  unblock - Restore network access"
    echo "  status  - Show current iptables rules"
fi