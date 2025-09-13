import yaml
import re

def escape_latex_text(text):
    """
    Escapes special LaTeX characters in a string, while preserving math environments.
    """
    # Find all math segments ($...$) and replace them with a unique placeholder.
    math_segments = re.findall(r'(\$.*?\$)', text)
    placeholder_text = re.sub(r'\$.*?\$', '@@MATH@@', text)

    # Escape special characters in the non-math text.
    escaped_text = placeholder_text.replace('&', r'\&')
    escaped_text = escaped_text.replace('%', r'\%')
    escaped_text = escaped_text.replace('$', r'\$')
    escaped_text = escaped_text.replace('#', r'\#')
    escaped_text = escaped_text.replace('_', r'\_')
    escaped_text = escaped_text.replace('{', r'\{')
    escaped_text = escaped_text.replace('}', r'\}')

    # Restore the math segments, replacing the placeholders.
    for segment in math_segments:
        escaped_text = escaped_text.replace('@@MATH@@', segment, 1)
        
    return escaped_text

def generate_latex_document(symbols):
    """
    Generates a full LaTeX document string from a list of symbol data.
    """
    preamble = r"""% Symbol Guide for Doodles Cards (v1)
% Auto-generated first draft. Edit for accuracy/refinement.
\documentclass[11pt,a4paper]{article}
\usepackage[margin=1.9cm]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{wrapfig}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{qrcode}
\usepackage{xcolor}
\usepackage{xparse}
\setlist[itemize]{leftmargin=*,nosep,topsep=2pt,partopsep=0pt}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=teal}
\pagestyle{plain}
\setlength{\parindent}{0pt}

% \newcommand{\symbolcard}[4]{%
%   \includegraphics[width=5cm]{#1}%
  
%   \begin{wrapfigure}{r}{0.2\textwidth}%
%     \qrcode{#2}%
%   \end{wrapfigure}%
%   {\Large \textbf{#3}} - #4%
  
%   \vspace{3\baselineskip}%
% }

% Custom command for creating symbol cards with images, descriptions, and QR codes
% Usage: \symbolcard{image_path}{url}{title}{description}
% Parameters:
%   #1: Path to the image file (relative to document)
%   #2: URL for the QR code (typically a reference link)
%   #3: Title/name of the symbol or concept
%   #4: Detailed description or explanation text
% Layout: Two-column design with image on left (30% width) and content on right (65% width)
% Features: Horizontal rule separator, responsive image scaling, bottom-aligned QR code
\newcommand{\symbolcard}[4]{%
  \noindent\hrule\vspace{18pt}                                % Top horizontal line separator + spacing
  % Image column is narrower (0.3), text column is wider (0.65)
  \begin{minipage}[c]{0.3\textwidth}                           % Left column: 30% width for image
    \includegraphics[width=\linewidth, keepaspectratio]{#1}    % The main image/symbol/logo
  \end{minipage}\hfill                                         % Gap between columns
  \begin{minipage}[c]{0.65\textwidth}                          % Right column: 65% width for text content
    {\Large\bfseries #3}\par\medskip                           % Large bold title at top of right column
    #4                                                         % Main description text body
    \par\vfill                                                 % Pushes QR code to bottom of right column
    \vspace{12pt}                                              % Horizontal gap between description and QR code
    \raggedleft                                                % Right-align the QR code
    \qrcode[height=2cm]{#2}                                    % Small QR code at bottom-right
  \end{minipage}
  \vspace{18pt}                                               % Bottom spacing before next card
}

\begin{document}
\begin{center}\Large\bfseries Particle / HEP Symbol \& Logo Guide (Draft)\end{center}
% \vspace{0.5em}\hrule\vspace{1em}

% NOTE: Verify physics accuracy; refine wording for final release.

"""

    postamble = r"""
\vfill\centerline{\small Draft generated on \today\ -- Review for accuracy before publication.}
\end{document}
"""

    body = ""
    for symbol in symbols:
        # Escape only the % character in URLs to match the original
        image = symbol.get('image', '')
        url = symbol.get('url', '').replace('%', r'\%')
        title = symbol.get('title', '')
        description = symbol.get('description', '')
        
        body += f"\\symbolcard{{{image}}}{{{url}}}{{{title}}}{{{description}}}\n"

    return preamble + body + postamble

if __name__ == "__main__":
    try:
        with open('symbols.yaml', 'r') as f:
            symbols_data = yaml.safe_load(f)
        
        if not symbols_data:
            raise ValueError("YAML file is empty or could not be read.")

        full_latex_doc = generate_latex_document(symbols_data)

        with open('symbol_guide_from_yaml.tex', 'w') as f:
            f.write(full_latex_doc)
        
        print("Successfully generated symbol_guide_from_yaml.tex")

    except Exception as e:
        print(f"An error occurred: {e}")
