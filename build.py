import os
import glob
import re
import shutil


HUB_THEME = {
    "ink": "#e6edf8",
    "paper": "#101a2e",
    "teal": "#10bfae",
    "blue": "#2496ed",
    "muted": "#9bb0d1",
    "bg_gradient": "linear-gradient(165deg, #070d19 0%, #081528 48%, #070c16 100%)",
    "bg_spot_teal": "radial-gradient(circle at 8% 10%, rgba(16, 191, 174, 0.24), transparent 36%)",
    "bg_spot_blue": "radial-gradient(circle at 92% 90%, rgba(36, 150, 237, 0.28), transparent 40%)",
    "shell_border": "rgba(140, 167, 206, 0.2)",
    "shell_bg": "rgba(9, 19, 34, 0.78)",
    "shell_shadow": "rgba(2, 6, 12, 0.56)",
    "card_border": "rgba(140, 167, 206, 0.22)",
    "card_shadow": "rgba(2, 8, 18, 0.5)",
    "card_fastapi_hover": "rgba(15, 118, 110, 0.45)",
    "card_docker_hover": "rgba(3, 105, 161, 0.45)",
    "card_n8n_hover": "rgba(255, 109, 90, 0.45)",
    "chip_fastapi_bg": "rgba(15, 118, 110, 0.12)",
    "chip_docker_bg": "rgba(36, 150, 237, 0.16)",
    "chip_n8n_bg": "rgba(255, 109, 90, 0.16)",
    "card_llamaindex_hover": "rgba(157, 78, 221, 0.45)",
    "chip_llamaindex_bg": "rgba(157, 78, 221, 0.16)",
    "cta": "#bdd8ff",
}


def create_dist_dirs():
    os.makedirs("dist/fastapi", exist_ok=True)
    os.makedirs("dist/docker", exist_ok=True)
    os.makedirs("dist/n8n", exist_ok=True)
    os.makedirs("dist/llamaindex", exist_ok=True)


def sync_local_preview_dirs():
    """Mirror dist handbooks to workspace root for VS Code Live Server preview."""
    hub_source = os.path.join("dist", "index.html")
    if os.path.exists(hub_source):
        shutil.copyfile(hub_source, "index.html")

    for folder in ("fastapi", "docker", "n8n", "llamaindex"):
        source = os.path.join("dist", folder)
        target = folder

        if not os.path.exists(source):
            continue

        if os.path.exists(target):
            shutil.rmtree(target)

        shutil.copytree(source, target)

        # Live Server does not support extensionless HTML routes by default.
        # Create no-extension aliases for chapter files for local preview URLs.
        for filename in os.listdir(target):
            if not filename.endswith(".html") or filename == "index.html":
                continue

            stem, _ = os.path.splitext(filename)
            src_file = os.path.join(target, filename)
            alias_file = os.path.join(target, stem)
            shutil.copyfile(src_file, alias_file)


def extract_title(html_content):
    m_h2 = re.search(r"<h2.*?>([\s\S]*?)</h2>", html_content)
    if m_h2:
        return m_h2.group(1).strip()
    return "Chapter"


def generate_handbook(src_dir, dist_folder, book_title):
    css_path = os.path.join(src_dir, "styles.css")
    cover_path = os.path.join(src_dir, "cover.html")
    script_path = os.path.join(src_dir, "script.js")

    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    with open(cover_path, "r", encoding="utf-8") as f:
        cover = f.read()

    script_content = ""
    has_script = os.path.exists(script_path)
    if has_script:
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

    chapter_files = sorted(glob.glob(os.path.join(src_dir, "chapters", "*.html")))

    # 1. Autogenerate TOC HTML based on discovered chapters
    toc_links = []
    chapters_data = []

    section_base = f"/{dist_folder}"

    def chapter_url(filename):
        return f"{section_base}/{filename}"

    script_tag = (
        f'<script src="{section_base}/script.js" defer></script>' if has_script else ""
    )

    for i, cf in enumerate(chapter_files):
        filename = os.path.basename(cf)  # e.g. chapter_01.html
        with open(cf, "r", encoding="utf-8") as f:
            content = f.read()
        title = extract_title(content)
        chapters_data.append({"filename": filename, "title": title, "content": content})
        toc_links.append(
            f'<li><button class="toc-link" type="button" data-href="{chapter_url(filename)}">{title}</button></li>'
        )

    toc_html = '<ul class="toc-list">\n' + "\n".join(toc_links) + "\n</ul>"

    active_fastapi = "active" if dist_folder == "fastapi" else ""
    active_docker = "active" if dist_folder == "docker" else ""
    active_n8n = "active" if dist_folder == "n8n" else ""
    active_llamaindex = "active" if dist_folder == "llamaindex" else ""

    topbar_html = f"""
    <header class="topbar">
        <div class="topbar-inner">
            <a class="brand" href="/">Developer Handbooks</a>
            <span class="topbar-context" id="topbar-context" aria-live="polite"></span>
            <nav class="top-nav" aria-label="Primary navigation">
                <a href="/fastapi/" class="top-link {active_fastapi}">FastAPI</a>
                <a href="/docker/" class="top-link {active_docker}">Docker</a>
                <a href="/n8n/" class="top-link {active_n8n}">n8n</a>
                <a href="/llamaindex/" class="top-link {active_llamaindex}">LlamaIndex</a>
                <button id="toc-toggle" class="top-link top-link-btn" type="button" aria-expanded="false" aria-controls="toc-sidebar" aria-label="Open table of contents">
                    <span class="hamburger-icon" aria-hidden="true"><span></span><span></span><span></span></span>
                </button>
            </nav>
        </div>
    </header>"""

    # Base layout template
    def render_page(content_html, current_idx=None):
        nav_buttons = ""
        if current_idx is not None:
            prev_btn = (
                f'<a href="{chapter_url(chapters_data[current_idx-1]["filename"])}" class="nav-btn">← Previous</a>'
                if current_idx > 0
                else f'<a href="{section_base}" class="nav-btn">← Cover</a>'
            )
            next_btn = (
                f'<a href="{chapter_url(chapters_data[current_idx+1]["filename"])}" class="nav-btn">Next →</a>'
                if current_idx < len(chapters_data) - 1
                else '<a href="#" class="nav-btn disabled">End of Handbook</a>'
            )
            nav_buttons = f'<div class="nav-buttons">{prev_btn}{next_btn}</div>'
        else:
            # We are on the cover page
            start_btn = (
                f'<a href="{chapter_url(chapters_data[0]["filename"])}" class="nav-btn">Start Reading →</a>'
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
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "vxhj0j0zwn");
    </script>
    <style>{css}</style>
</head>
<body data-handbook="{dist_folder}">
    {topbar_html}
    <div class="layout">
        <nav class="sidebar" id="toc-sidebar">
            <h3>Table of Contents</h3>
            {toc_html}
        </nav>
        <main class="content-wrapper">
            {content_html}
            {nav_buttons}
        </main>
    </div>
    {script_tag}
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

    if has_script:
        with open(
            os.path.join("dist", dist_folder, "script.js"), "w", encoding="utf-8"
        ) as f:
            f.write(script_content)


def build_hub():
    hub_css_vars = f"""
        :root {{
            --ink: {HUB_THEME['ink']};
            --paper: {HUB_THEME['paper']};
            --teal: {HUB_THEME['teal']};
            --blue: {HUB_THEME['blue']};
            --muted: {HUB_THEME['muted']};
            --shell-border: {HUB_THEME['shell_border']};
            --shell-bg: {HUB_THEME['shell_bg']};
            --shell-shadow: {HUB_THEME['shell_shadow']};
            --card-border: {HUB_THEME['card_border']};
            --card-shadow: {HUB_THEME['card_shadow']};
            --card-fastapi-hover: {HUB_THEME['card_fastapi_hover']};
            --card-docker-hover: {HUB_THEME['card_docker_hover']};
            --card-n8n-hover: {HUB_THEME['card_n8n_hover']};
            --card-llamaindex-hover: {HUB_THEME['card_llamaindex_hover']};
            --chip-fastapi-bg: {HUB_THEME['chip_fastapi_bg']};
            --chip-docker-bg: {HUB_THEME['chip_docker_bg']};
            --chip-n8n-bg: {HUB_THEME['chip_n8n_bg']};
            --chip-llamaindex-bg: {HUB_THEME['chip_llamaindex_bg']};
            --cta: {HUB_THEME['cta']};
            --bg-spot-teal: {HUB_THEME['bg_spot_teal']};
            --bg-spot-blue: {HUB_THEME['bg_spot_blue']};
            --bg-gradient: {HUB_THEME['bg_gradient']};
        }}
"""

    hub_html = (
        """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">
    <title>Developer Handbooks Hub</title>
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){
            c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        })(window, document, "clarity", "script", "vxhj0j0zwn");
    </script>
    <style>"""
        + hub_css_vars
        + """

        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: "Sora", "Segoe UI", sans-serif;
            color: var(--ink);
            background:
                var(--bg-spot-teal),
                var(--bg-spot-blue),
                var(--bg-gradient);
            display: grid;
            place-items: center;
            padding: 24px;
        }

        .shell {
            width: min(1040px, 100%);
            border-radius: 28px;
            border: 1px solid var(--shell-border);
            background: var(--shell-bg);
            backdrop-filter: blur(6px);
            box-shadow: 0 24px 60px var(--shell-shadow);
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
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 24px;
            min-height: 208px;
            display: grid;
            align-content: space-between;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 14px 36px var(--card-shadow);
        }

        .fastapi:hover {
            border-color: var(--card-fastapi-hover);
        }

        .docker:hover {
            border-color: var(--card-docker-hover);
        }

        .n8n:hover {
            border-color: var(--card-n8n-hover);
        }

        .llamaindex:hover {
            border-color: var(--card-llamaindex-hover);
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

        .chip.fastapi { background: var(--chip-fastapi-bg); color: var(--teal); }
        .chip.docker { background: var(--chip-docker-bg); color: var(--blue); }
        .chip.n8n { background: var(--chip-n8n-bg); color: #ff6d5a; }
        .chip.llamaindex { background: var(--chip-llamaindex-bg); color: #b36cf2; }

        .card-head {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 14px;
            margin-bottom: 10px;
        }

        .brand-logo {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.14);
            flex-shrink: 0;
        }

        .brand-logo svg {
            width: 24px;
            height: 24px;
            display: block;
        }

        .brand-logo.fastapi {
            background: linear-gradient(145deg, rgba(16, 191, 174, 0.25), rgba(11, 107, 97, 0.35));
            color: #8bfff2;
        }

        .brand-logo.docker {
            background: linear-gradient(145deg, #2ea8ff, #1b79c8);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.28);
        }

        .brand-logo.n8n {
            background: linear-gradient(145deg, #ea4262, #ff6d5a);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.28);
        }

        .brand-logo.llamaindex {
            background: linear-gradient(145deg, #b36cf2, #9d4edd);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.28);
        }

        .brand-logo.docker svg {
            width: 27px;
            height: 27px;
        }

        h2 {
            margin: 0;
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
            color: var(--cta);
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
        <p class="lead">Structured notes with practical examples and chapter-level navigation.</p>

        <div class="grid">
            <a href="/fastapi/" class="card fastapi">
                <div>
                    <span class="chip fastapi">Backend</span>
                    <div class="card-head">
                        <span class="brand-logo fastapi" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 2.4C6.7 2.4 2.4 6.7 2.4 12s4.3 9.6 9.6 9.6 9.6-4.3 9.6-9.6S17.3 2.4 12 2.4Z" stroke="currentColor" stroke-width="1.6"/>
                                <path d="M13.8 4.8 8 13.2h3.7L10.3 19l5.7-8.3h-3.6l1.4-5.9Z" fill="currentColor"/>
                            </svg>
                        </span>
                        <h2>FastAPI Notes</h2>
                    </div>
                    <p>Build, validate, document, and deploy production-grade APIs from first endpoint to advanced patterns.</p>
                </div>
                <p class="cta">Open handbook -></p>
            </a>

            <a href="/docker/" class="card docker">
                <div>
                    <span class="chip docker">Platform</span>
                    <div class="card-head">
                        <span class="brand-logo docker" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <rect x="3.6" y="8.6" width="3.2" height="3" rx="0.5" fill="currentColor"/>
                                <rect x="7.3" y="8.6" width="3.2" height="3" rx="0.5" fill="currentColor"/>
                                <rect x="11" y="8.6" width="3.2" height="3" rx="0.5" fill="currentColor"/>
                                <rect x="7.3" y="5.2" width="3.2" height="3" rx="0.5" fill="currentColor"/>
                                <rect x="11" y="5.2" width="3.2" height="3" rx="0.5" fill="currentColor"/>
                                <path d="M2.8 13.2h12.9c1.7 0 3.1-.4 4.1-1.3.3 3.8-2.3 6.8-6.8 6.8H8.2c-3.1 0-5-2.1-5.4-5.5Z" fill="currentColor"/>
                                <path d="M18 9.7c.9-.4 1.8-.9 2.1-1.7.7.9 1 2 .9 3.2" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                            </svg>
                        </span>
                        <h2>Docker Notes</h2>
                    </div>
                    <p>Container fundamentals and workflows for local development, image design, and practical deployment habits.</p>
                </div>
                <p class="cta">Open handbook -></p>
            </a>

            <a href="/n8n/" class="card n8n">
                <div>
                    <span class="chip n8n">Automation</span>
                    <div class="card-head">
                        <span class="brand-logo n8n" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="12" cy="12" r="10" fill="currentColor" />
                                <circle cx="7" cy="12" r="2" fill="#131920"/>
                                <circle cx="16" cy="8" r="2" fill="#131920"/>
                                <circle cx="16" cy="16" r="2" fill="#131920"/>
                                <path d="M 9 12 Q 12 12 12 10 T 14 8" stroke="#131920" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                                <path d="M 9 12 Q 12 12 12 14 T 14 16" stroke="#131920" stroke-width="1.5" fill="none" stroke-linecap="round"/>
                            </svg>
                        </span>
                        <h2>n8n Notes</h2>
                    </div>
                    <p>Build, self-host, and extend n8n automations. Zero fluff. Real examples.</p>
                </div>
                <p class="cta">Open handbook -></p>
            </a>

            <a href="/llamaindex/" class="card llamaindex">
                <div>
                    <span class="chip llamaindex">AI / RAG</span>
                    <div class="card-head">
                        <span class="brand-logo llamaindex" aria-hidden="true">
                            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <circle cx="12" cy="12" r="11" fill="currentColor" fill-opacity="0.1"/>
                                <path d="M10 16V13C10 11.5 11.5 10.5 11.5 9C11.5 7.5 13 6 13 6C13 6 14.5 8 14.5 9C14.5 10 16 11 16 12C16 12 15.5 13.5 14 14V16H12.5V14.5C12 14.5 11.5 16 11.5 16H10Z" fill="currentColor" />
                            </svg>
                        </span>
                        <h2>LlamaIndex Notes</h2>
                    </div>
                    <p>Build RAG applications, setup vector stores, retrieve relevant data, and create agents.</p>
                </div>
                <p class="cta">Open handbook -></p>
            </a>
        </div>
    </main>
</body>
</html>"""
    )
    for output_path in (os.path.join("dist", "index.html"), "index.html"):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(hub_html)


if __name__ == "__main__":
    create_dist_dirs()
    print("Building FastAPI Handbook...")
    generate_handbook("src_fastapi", "fastapi", "FastAPI Complete Handbook")
    print("Building Docker Handbook...")
    generate_handbook("src_docker", "docker", "Docker Complete Handbook")
    print("Building n8n Handbook...")
    generate_handbook("src_n8n", "n8n", "n8n Complete Handbook")
    print("Building LlamaIndex Handbook...")
    generate_handbook("src_llamaindex", "llamaindex", "LlamaIndex Complete Handbook")
    print("Building Hub...")
    build_hub()
    print("Syncing local preview folders...")
    sync_local_preview_dirs()
    print("Successfully compiled SSG to /dist/")
