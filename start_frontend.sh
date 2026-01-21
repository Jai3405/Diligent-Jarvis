#!/bin/bash

# JARVIS /// NEURAL INTERFACE
# Starts the Vite Development Server

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${GREEN}
       _ ___   ______  _   _____________
      | /   | / __ \ | / /  _/ ___/
  __  | / /| |/ /_/ / |/ // / \__ \ 
 / /_/ / ___ / _, _/|  // / ___/ / 
 \____/_/  |/_/ |_| |_/___//____/  
                                    
${NC}"

echo -e "${CYAN}[SYSTEM] Initializing React Neural Interface...${NC}"
echo -e "${CYAN}[TARGET] http://localhost:5173${NC}"

cd frontend

if [ ! -d "node_modules" ]; then
    echo -e "${CYAN}[SETUP] Installing dependencies (first run)...${NC}"
    npm install
fi

echo -e "${GREEN}>>> SYSTEM ONLINE <<<${NC}"
npm run dev