import yaml
import re
import argparse


def escape_latex_text(text: str) -> str:
    """
    Escapes special LaTeX characters in a string, while preserving math environments.
    """
    # Find all math segments ($...$) and replace them with a unique placeholder.
    math_segments = re.findall(r"(\$.*?\$)", text)
    placeholder_text = re.sub(r"\$.*?\$", "@@MATH@@", text)

    # Escape special characters in the non-math text.
    escaped_text = placeholder_text.replace("&", r"\&")
    escaped_text = escaped_text.replace("%", r"\%")
    escaped_text = escaped_text.replace("$", r"\$")
    escaped_text = escaped_text.replace("#", r"\#")
    escaped_text = escaped_text.replace("_", r"\_")
    escaped_text = escaped_text.replace("{", r"\{")
    escaped_text = escaped_text.replace("}", r"\}")

    # Restore the math segments, replacing the placeholders.
    for segment in math_segments:
        escaped_text = escaped_text.replace("@@MATH@@", segment, 1)

    return escaped_text


def generate_latex_document(symbols: list[dict[str, str]]) -> str:
    """
    Generates a full LaTeX document string from a list of symbol data.
    """
    with open("preamble.tex", "r") as f:
        preamble = f.read()

    postamble = r"\end{document}"

    body = ""
    for symbol in symbols:
        # Escape only the % character in URLs to match the original
        image = symbol.get("image", "")
        url = escape_latex_text(symbol.get("url", ""))
        title = escape_latex_text(symbol.get("title", ""))
        description = escape_latex_text(symbol.get("description", ""))

        body += f"\\symbolcard{{{image}}}{{{url}}}{{{title}}}{{{description}}}\n"

    return preamble + body + postamble


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LaTeX document from YAML symbols file")
    parser.add_argument(
        "yaml_file",
        nargs="?",
        default="symbols.yaml",
        help="Path to the YAML file containing symbol data (default: symbols.yaml)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="symbol_guide_from_yaml.tex",
        help="Output LaTeX file name (default: symbol_guide_from_yaml.tex)",
    )

    args = parser.parse_args()

    try:
        with open(args.yaml_file, "r") as f:
            symbols_data = yaml.safe_load(f)

        if not symbols_data:
            raise ValueError("YAML file is empty or could not be read.")

        full_latex_doc = generate_latex_document(symbols_data)

        with open(args.output, "w") as f:
            f.write(full_latex_doc)

        print(f"Successfully generated {args.output} from {args.yaml_file}")

    except FileNotFoundError:
        print(f"Error: YAML file '{args.yaml_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
