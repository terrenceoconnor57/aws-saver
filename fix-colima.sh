#!/bin/bash
set -e

echo "🔧 Fixing stuck Colima..."

# Force kill all Colima-related processes
echo "Killing hung processes..."
pkill -9 colima 2>/dev/null || true
pkill -9 limactl 2>/dev/null || true
pkill -9 qemu-system 2>/dev/null || true

# Remove stale socket files
echo "Cleaning up stale socket files..."
rm -f ~/.lima/colima/ha.sock 2>/dev/null || true
rm -f ~/.lima/colima/ssh.sock 2>/dev/null || true
rm -f ~/.lima/colima/qmp.sock 2>/dev/null || true

# Wait a moment for cleanup
sleep 2

# Restart Colima
echo "Starting Colima..."
colima start --cpu 4 --memory 8 --disk 60

# Verify Docker is working
echo ""
echo "✅ Verifying Docker..."
docker version --format '{{.Server.Version}}' > /dev/null 2>&1 && echo "✅ Docker is running!" || echo "❌ Docker check failed"

echo ""
echo "✨ Done! You can now reopen your project in the dev container."

