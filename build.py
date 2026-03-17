import os
import glob


def build_handbook():
    src_dir = "src"
    dist_file = "index.html"

    # Read CSS
    with open(os.path.join(src_dir, "styles.css"), "r", encoding="utf-8") as f:
        css = f.read()

    # Read cover
    with open(os.path.join(src_dir, "cover.html"), "r", encoding="utf-8") as f:
        cover = f.read()

    # Read toc
    with open(os.path.join(src_dir, "toc.html"), "r", encoding="utf-8") as f:
        toc = f.read()

    # Read chapters
    chapters_dir = os.path.join(src_dir, "chapters")
    chapter_files = sorted(glob.glob(os.path.join(chapters_dir, "*.html")))

    chapters_content = ""
    for cf in chapter_files:
        with open(cf, "r", encoding="utf-8") as f:
            chapters_content += f.read() + "\n"

    html_template = f"""<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>FastAPI Complete Handbook</title>
                <style>
                    {css}
                </style>
            </head>
            <body>

                {cover}

                {toc}

                {chapters_content}

            </body>
        </html>
    """

    with open(dist_file, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Successfully built {dist_file}")


if __name__ == "__main__":
    build_handbook()
