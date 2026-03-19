import os
import glob
import re


def create_dist_dirs():
    os.makedirs("dist/fastapi", exist_ok=True)
    os.makedirs("dist/docker", exist_ok=True)


def extract_title(html_content):
    m_h2 = re.search(r"<h2.*?>([\s\S]*?)</h2>", html_content)
    if m_h2:
        return m_h2.group(1).strip()
    return "Chapter"


def generate_handbook(src_dir, dist_folder, book_title):
    css_path = os.path.join(src_dir, "styles.css")
    cover_path = os.path.join(src_dir, "cover.html")

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    with open(cover_path, "r", encoding="utf-8") as f:
        cover = f.read()

    chapter_files = sorted(glob.glob(os.path.join(src_dir, "chapters", "*.html")))

    # 1. Autogenerate TOC HTML based on discovered chapters
    toc_links = []
    chapters_data = []

    for i, cf in enumerate(chapter_files):
        filename = os.path.basename(cf)  # e.g. chapter_01.html
        with open(cf, "r", encoding="utf-8") as f:
            content = f.read()
        title = extract_title(content)
        chapters_data.append({"filename": filename, "title": title, "content": content})
        toc_links.append(f'<li><a href="{filename}">{title}</a></li>')

    toc_html = '<ul class="toc-list">\n' + "\n".join(toc_links) + "\n</ul>"

    # Base layout template
    def render_page(content_html, current_idx=None):
        nav_buttons = ""
        if current_idx is not None:
            prev_btn = (
                f'<a href="{chapters_data[current_idx-1]["filename"]}" class="nav-btn">← Previous</a>'
                if current_idx > 0
                else f'<a href="index.html" class="nav-btn">← Cover</a>'
            )
            next_btn = (
                f'<a href="{chapters_data[current_idx+1]["filename"]}" class="nav-btn">Next →</a>'
                if current_idx < len(chapters_data) - 1
                else '<a href="#" class="nav-btn disabled">End of Handbook</a>'
            )
            nav_buttons = f'<div class="nav-buttons">{prev_btn}{next_btn}</div>'
        else:
            # We are on the cover page
            start_btn = (
                f'<a href="{chapters_data[0]["filename"]}" class="nav-btn">Start Reading →</a>'
                if chapters_data
                else ""
            )
            nav_buttons = f'<div class="nav-buttons">{start_btn}</div>'

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book_title}</title>
    <style>{css}</style>
</head>
<body>
    <div class="layout">
        <nav class="sidebar">
            <h3>Table of Contents</h3>
            {toc_html}
        </nav>
        <main class="content-wrapper">
            {content_html}
            {nav_buttons}
        </main>
    </div>
</body>
</html>"""

    # Write Cover/Index
    with open(
        os.path.join("dist", dist_folder, "index.html"), "w", encoding="utf-8"
    ) as f:
        f.write(render_page(cover))

    # Write Chapters
    for i, chap in enumerate(chapters_data):
        with open(
            os.path.join("dist", dist_folder, chap["filename"]), "w", encoding="utf-8"
        ) as f:
            f.write(render_page(chap["content"], i))


def build_hub():
    hub_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
    <title>Developer Handbooks Hub</title>
    <style>
        :root {
            --ink: #e6edf8;
            --paper: #101a2e;
            --teal: #10bfae;
            --blue: #2496ed;
            --muted: #9bb0d1;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: "Sora", "Segoe UI", sans-serif;
            color: var(--ink);
            background:
                radial-gradient(circle at 8% 10%, rgba(16, 191, 174, 0.24), transparent 36%),
                radial-gradient(circle at 92% 90%, rgba(36, 150, 237, 0.28), transparent 40%),
                linear-gradient(165deg, #070d19 0%, #081528 48%, #070c16 100%);
            display: grid;
            place-items: center;
            padding: 24px;
        }

        .shell {
            width: min(1040px, 100%);
            border-radius: 28px;
            border: 1px solid rgba(140, 167, 206, 0.2);
            background: rgba(9, 19, 34, 0.78);
            backdrop-filter: blur(6px);
            box-shadow: 0 24px 60px rgba(2, 6, 12, 0.56);
            padding: 44px 38px;
            animation: rise 420ms ease-out both;
        }

        .eyebrow {
            margin: 0 0 10px 0;
            font-family: "IBM Plex Mono", monospace;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--blue);
            font-size: 12px;
        }

        h1 {
            margin: 0;
            font-size: clamp(2rem, 3.8vw, 3.4rem);
            line-height: 1.12;
            max-width: 14ch;
        }

        .lead {
            margin: 14px 0 34px 0;
            color: var(--muted);
            max-width: 60ch;
            line-height: 1.6;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
        }

        .card {
            text-decoration: none;
            color: var(--ink);
            background: var(--paper);
            border: 1px solid rgba(140, 167, 206, 0.22);
            border-radius: 20px;
            padding: 24px;
            min-height: 208px;
            display: grid;
            align-content: space-between;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 14px 36px rgba(2, 8, 18, 0.5);
        }

        .fastapi:hover {
            border-color: rgba(15, 118, 110, 0.45);
        }

        .docker:hover {
            border-color: rgba(3, 105, 161, 0.45);
        }

        .chip {
            width: fit-content;
            border-radius: 999px;
            padding: 6px 10px;
            font-size: 11px;
            font-family: "IBM Plex Mono", monospace;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .chip.fastapi { background: rgba(15, 118, 110, 0.12); color: var(--teal); }
        .chip.docker { background: rgba(36, 150, 237, 0.16); color: var(--blue); }

        h2 {
            margin: 14px 0 10px;
            font-size: 1.25rem;
        }

        p {
            margin: 0;
            color: var(--muted);
            line-height: 1.55;
        }

        .cta {
            margin-top: 16px;
            font-family: "IBM Plex Mono", monospace;
            font-size: 0.83rem;
            color: #bdd8ff;
        }

        @media (max-width: 820px) {
            .shell { padding: 30px 22px; border-radius: 22px; }
            .grid { grid-template-columns: 1fr; }
            .card { min-height: 170px; }
        }

        @keyframes rise {
            from { opacity: 0; transform: translateY(14px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <main class="shell">
        <p class="eyebrow">Developer Library</p>
        <h1>Choose your handbook and start learning fast.</h1>
        <p class="lead">Structured notes with practical examples and chapter-level navigation for backend and platform engineering topics.</p>

        <div class="grid">
            <a href="/fastapi/" class="card fastapi">
                <div>
                    <span class="chip fastapi">Backend</span>
                    <h2>FastAPI Notes</h2>
                    <p>Build, validate, document, and deploy production-grade APIs from first endpoint to advanced patterns.</p>
                </div>
                <p class="cta">Open handbook -></p>
            </a>

            <a href="/docker/" class="card docker">
                <div>
                    <span class="chip docker">Platform</span>
                    <h2>Docker Notes</h2>
                    <p>Container fundamentals and workflows for local development, image design, and practical deployment habits.</p>
                </div>
                <p class="cta">Open handbook -></p>
            </a>
        </div>
    </main>
</body>
</html>"""
    with open(os.path.join("dist", "index.html"), "w", encoding="utf-8") as f:
        f.write(hub_html)


if __name__ == "__main__":
    create_dist_dirs()
    print("Building FastAPI Handbook...")
    generate_handbook("src_fastapi", "fastapi", "FastAPI Complete Handbook")
    print("Building Docker Handbook...")
    generate_handbook("src_docker", "docker", "Docker for Developers")
    print("Building Hub...")
    build_hub()
    print("Successfully compiled SSG to /dist/")
