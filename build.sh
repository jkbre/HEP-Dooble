#!/bin/bash

# Script to generate and compile LaTeX symbol guide from YAML file
# Usage: ./build_guide.sh <yaml_file> [expected_png_count] [output_name]

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if YAML file is provided
if [ $# -lt 1 ]; then
    print_error "Usage: $0 <yaml_file> [expected_png_count] [output_name]"
    print_error "Example: $0 symbols_v2.yaml 57 my_guide"
    exit 1
fi

YAML_FILE="$1"
EXPECTED_PNG_COUNT="${2:-57}"  # Default to 57 if not provided
OUTPUT_NAME="${3:-symbol_guide_from_yaml}"  # Default output name

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    print_error "pdflatex could not be found. Please install a LaTeX distribution."
    exit 1
fi

# Check if YAML file exists
if [ ! -f "$YAML_FILE" ]; then
    print_error "YAML file '$YAML_FILE' not found!"
    exit 1
fi

print_status "Processing YAML file: $YAML_FILE"

# Check HEP folder and PNG files
print_status "Checking HEP folder..."
if [ ! -d "HEP" ]; then
    print_error "HEP directory not found!"
    exit 1
fi

# Count PNG files in HEP directory
PNG_COUNT=$(ls HEP/*.png 2>/dev/null | wc -l)
print_status "Found $PNG_COUNT PNG files in HEP directory"

# Check if PNG count matches expected
if [ "$PNG_COUNT" -ne "$EXPECTED_PNG_COUNT" ]; then
    print_warning "Expected $EXPECTED_PNG_COUNT PNG files, but found $PNG_COUNT"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Aborted by user"
        exit 1
    fi
else
    print_success "PNG file count matches expected ($EXPECTED_PNG_COUNT)"
fi

# Generate LaTeX file using Python script
print_status "Generating LaTeX file..."
if python generate_tex.py "$YAML_FILE" -o "${OUTPUT_NAME}.tex"; then
    print_success "LaTeX file generated: ${OUTPUT_NAME}.tex"
else
    print_error "Failed to generate LaTeX file!"
    exit 1
fi

# Check if required TeX files exist
for tex_file in preamble.tex; do
    if [ ! -f "$tex_file" ]; then
        print_error "Required file '$tex_file' not found!"
        exit 1
    fi
done

# Compile LaTeX file to PDF
print_status "Compiling LaTeX to PDF..."

# First compilation
if pdflatex -interaction=nonstopmode "${OUTPUT_NAME}.tex" > /dev/null 2>&1; then
    print_status "First compilation completed"
else
    print_error "First LaTeX compilation failed!"
    print_error "Check ${OUTPUT_NAME}.log for details"
    exit 1
fi

# Second compilation (for references, TOC, etc.)
if pdflatex -interaction=nonstopmode "${OUTPUT_NAME}.tex" > /dev/null 2>&1; then
    print_success "PDF compilation completed: ${OUTPUT_NAME}.pdf"
else
    print_warning "Second LaTeX compilation had issues, but PDF may still be usable"
fi

# Clean up auxiliary files
print_status "Cleaning up auxiliary files..."
rm -f "${OUTPUT_NAME}.aux" "${OUTPUT_NAME}.log" "${OUTPUT_NAME}.out"

# Final status
if [ -f "${OUTPUT_NAME}.pdf" ]; then
    PDF_SIZE=$(du -h "${OUTPUT_NAME}.pdf" | cut -f1)
    print_success "Build completed successfully!"
    print_success "Generated files:"
    print_success "  - ${OUTPUT_NAME}.tex (LaTeX source)"
    print_success "  - ${OUTPUT_NAME}.pdf (${PDF_SIZE})"
    
    # # Optional: Open PDF if display is available
    # if command -v xdg-open > /dev/null 2>&1 && [ -n "$DISPLAY" ]; then
    #     read -p "Open PDF file? (y/n): " -n 1 -r
    #     echo
    #     if [[ $REPLY =~ ^[Yy]$ ]]; then
    #         xdg-open "${OUTPUT_NAME}.pdf" &
    #     fi
    # fi
else
    print_error "PDF file was not generated successfully!"
    exit 1
fi
