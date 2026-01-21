#!/bin/bash

# JARVIS /// NEURAL BACKEND
# Starts the API Server and Inference Engine

# Colors
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

clear
echo -e "${PURPLE}
    ____  ___    ________ __  _______   ______
   / __ )/   |  / ____/ //_// ____/ | / /   \ 
  / __  / /| | / /   / ,<  / __/ /  |/ /  |  |
 / /_/ / ___ |/ /___/ /| |/ /___/ /|  /   |  |
/_____/_/  |_|\____/_/ |_/_____/_/ |_/____/  /
                                     /_____/  
${NC}"

echo -e "${BLUE}[SYSTEM] Initializing Neural Engine...${NC}"
echo -e "${BLUE}[CONFIG] Port: 8000 | Host: 0.0.0.0${NC}"
echo -e "${BLUE}[STATUS] Loading LLaMA Model & Vector Database...${NC}"
echo -e ""

# Start Uvicorn
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --reload
