#!/bin/bash

#######################################
# SPOTIFYDL - Complete Music Tool
# Download from Spotify + Convert to 432Hz
#######################################

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default directories
DOWNLOAD_DIR="./downloads"
CONVERTED_DIR="./432hz"

#######################################
# FUNCTIONS
#######################################

show_banner() {
    echo -e "${CYAN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     🎵 SPOTIFYDL - Complete Music Tool 🎵                 ║"
    echo "║     Download from Spotify + Convert to 432Hz              ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

show_help() {
    echo -e "${YELLOW}USAGE:${NC}"
    echo "  ./run.sh [option] [arguments]"
    echo ""
    echo -e "${YELLOW}OPTIONS:${NC}"
    echo -e "  ${GREEN}download${NC}    <spotify_url>     Download playlist/album/track"
    echo -e "  ${GREEN}convert${NC}     <file.mp3>        Convert single file to 432Hz"
    echo -e "  ${GREEN}convert-dir${NC} <folder>          Convert all MP3s in folder to 432Hz"
    echo -e "  ${GREEN}verify${NC}      <original> <converted>  Compare two files"
    echo -e "  ${GREEN}menu${NC}                          Interactive menu"
    echo -e "  ${GREEN}help${NC}                          Show this help"
    echo ""
    echo -e "${YELLOW}EXAMPLES:${NC}"
    echo "  ./run.sh download \"https://open.spotify.com/playlist/xxxxx\""
    echo "  ./run.sh convert \"./downloads/song.mp3\""
    echo "  ./run.sh convert-dir \"./downloads\""
    echo "  ./run.sh verify \"original.mp3\" \"converted_432hz.mp3\""
    echo "  ./run.sh menu"
    echo ""
}

check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python &> /dev/null; then
        echo -e "${RED}✗ Python not found${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Python OK${NC}"
    fi
    
    # Check FFmpeg
    if ! command -v ffmpeg &> /dev/null; then
        echo -e "${RED}✗ FFmpeg not found${NC}"
        echo "  Install with: winget install FFmpeg"
        return 1
    else
        echo -e "${GREEN}✓ FFmpeg OK${NC}"
    fi
    
    # Check spotdl
    if ! python -m spotdl --version &> /dev/null; then
        echo -e "${YELLOW}⚠ spotdl not found, installing...${NC}"
        pip install spotdl
    else
        echo -e "${GREEN}✓ spotdl OK${NC}"
    fi
    
    echo ""
    return 0
}

download_spotify() {
    local url="$1"
    local output_dir="${2:-$DOWNLOAD_DIR}"
    
    if [ -z "$url" ]; then
        echo -e "${RED}Error: No URL provided${NC}"
        echo "Usage: ./run.sh download <spotify_url>"
        return 1
    fi
    
    mkdir -p "$output_dir"
    
    echo -e "${CYAN}Downloading from Spotify...${NC}"
    echo -e "URL: ${YELLOW}$url${NC}"
    echo -e "Output: ${YELLOW}$output_dir${NC}"
    echo ""
    
    python -m spotdl "$url" --output "$output_dir"
    
    echo ""
    echo -e "${GREEN}✓ Download complete!${NC}"
    echo -e "Files saved to: ${YELLOW}$output_dir${NC}"
}

convert_file() {
    local input_file="$1"
    
    if [ -z "$input_file" ]; then
        echo -e "${RED}Error: No file provided${NC}"
        echo "Usage: ./run.sh convert <file.mp3>"
        return 1
    fi
    
    if [ ! -f "$input_file" ]; then
        echo -e "${RED}Error: File not found: $input_file${NC}"
        return 1
    fi
    
    echo -e "${CYAN}Converting to 432Hz...${NC}"
    python convertir_432hz_v2.py "$input_file"
}

convert_directory() {
    local input_dir="$1"
    local output_dir="${2:-}"
    
    if [ -z "$input_dir" ]; then
        echo -e "${RED}Error: No directory provided${NC}"
        echo "Usage: ./run.sh convert-dir <folder>"
        return 1
    fi
    
    if [ ! -d "$input_dir" ]; then
        echo -e "${RED}Error: Directory not found: $input_dir${NC}"
        return 1
    fi
    
    echo -e "${CYAN}Converting all MP3s in folder to 432Hz...${NC}"
    
    if [ -n "$output_dir" ]; then
        python convertir_432hz_v2.py "$input_dir" "$output_dir"
    else
        python convertir_432hz_v2.py "$input_dir"
    fi
}

verify_conversion() {
    local original="$1"
    local converted="$2"
    
    if [ -z "$original" ] || [ -z "$converted" ]; then
        echo -e "${RED}Error: Need two files to compare${NC}"
        echo "Usage: ./run.sh verify <original.mp3> <converted.mp3>"
        return 1
    fi
    
    echo -e "${CYAN}Comparing files...${NC}"
    echo ""
    
    # Get durations using ffprobe
    orig_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$original" 2>/dev/null)
    conv_duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$converted" 2>/dev/null)
    
    echo -e "Original:  ${YELLOW}$(basename "$original")${NC}"
    echo -e "  Duration: ${GREEN}${orig_duration}s${NC}"
    echo ""
    echo -e "Converted: ${YELLOW}$(basename "$converted")${NC}"
    echo -e "  Duration: ${GREEN}${conv_duration}s${NC}"
    echo ""
    
    # Calculate ratio
    if [ -n "$orig_duration" ] && [ -n "$conv_duration" ]; then
        ratio=$(echo "scale=6; $conv_duration / $orig_duration" | bc)
        echo -e "Duration ratio: ${CYAN}$ratio${NC}"
        
        # Check if ratio is close to 1.0 (tempo preserved)
        diff=$(echo "scale=6; $ratio - 1.0" | bc)
        abs_diff=${diff#-}
        
        if (( $(echo "$abs_diff < 0.02" | bc -l) )); then
            echo -e "${GREEN}✓ Tempo preserved correctly!${NC}"
            echo -e "${GREEN}✓ Pitch should be shifted to 432Hz${NC}"
        else
            echo -e "${YELLOW}⚠ Duration ratio differs from 1.0${NC}"
        fi
    fi
    
    echo ""
    echo -e "${CYAN}════════════════════════════════════════${NC}"
    echo -e "${YELLOW}To verify aurally:${NC}"
    echo "1. Play both files back-to-back"
    echo "2. The 432Hz version should sound LOWER in pitch"
    echo "3. But should play at the SAME SPEED"
    echo ""
    echo "4. Use a phone tuner app (Pano Tuner, gStrings):"
    echo "   - 440Hz: notes show normal"
    echo "   - 432Hz: notes show ~31 cents flat"
    echo -e "${CYAN}════════════════════════════════════════${NC}"
}

interactive_menu() {
    while true; do
        show_banner
        
        echo -e "${YELLOW}MAIN MENU${NC}"
        echo ""
        echo -e "  ${CYAN}1.${NC} Download from Spotify"
        echo -e "  ${CYAN}2.${NC} Convert single file to 432Hz"
        echo -e "  ${CYAN}3.${NC} Convert entire folder to 432Hz"
        echo -e "  ${CYAN}4.${NC} Verify conversion (compare files)"
        echo -e "  ${CYAN}5.${NC} Check dependencies"
        echo -e "  ${CYAN}6.${NC} Show help"
        echo -e "  ${CYAN}0.${NC} Exit"
        echo ""
        
        read -p "Select option: " choice
        echo ""
        
        case $choice in
            1)
                echo -e "${CYAN}=== DOWNLOAD FROM SPOTIFY ===${NC}"
                read -p "Spotify URL (playlist/album/track): " url
                read -p "Output folder [./downloads]: " output
                output=${output:-./downloads}
                download_spotify "$url" "$output"
                ;;
            2)
                echo -e "${CYAN}=== CONVERT SINGLE FILE ===${NC}"
                read -p "MP3 file path: " filepath
                convert_file "$filepath"
                ;;
            3)
                echo -e "${CYAN}=== CONVERT FOLDER ===${NC}"
                read -p "Folder with MP3s: " folder
                read -p "Output folder [auto]: " output
                convert_directory "$folder" "$output"
                ;;
            4)
                echo -e "${CYAN}=== VERIFY CONVERSION ===${NC}"
                read -p "Original file (440Hz): " original
                read -p "Converted file (432Hz): " converted
                verify_conversion "$original" "$converted"
                ;;
            5)
                check_dependencies
                ;;
            6)
                show_help
                ;;
            0)
                echo -e "${GREEN}Goodbye! 🎵${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
        clear
    done
}

#######################################
# MAIN
#######################################

# Change to script directory
cd "$(dirname "$0")"

# Parse command line arguments
case "${1:-menu}" in
    download)
        download_spotify "$2" "$3"
        ;;
    convert)
        convert_file "$2"
        ;;
    convert-dir)
        convert_directory "$2" "$3"
        ;;
    verify)
        verify_conversion "$2" "$3"
        ;;
    check)
        check_dependencies
        ;;
    help|--help|-h)
        show_banner
        show_help
        ;;
    menu|"")
        interactive_menu
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_help
        exit 1
        ;;
esac

