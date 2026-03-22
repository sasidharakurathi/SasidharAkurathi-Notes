import os


def create_n8n_styles():
    with open("src_fastapi/styles.css", "r", encoding="utf-8") as f:
        css = f.read()

    # Color replacements for n8n theme
    replacements = {
        "--primary: #10bfae;": "--primary: #ff6d5a;",
        "--primary-strong: #0e988c;": "--primary-strong: #ea4262;",
        "--bg-main: #061414;": "--bg-main: #0a0b10;",
        "--bg-surface: #0b1f20;": "--bg-surface: #141b22;",
        "--bg-elevated: #102a2c;": "--bg-elevated: #1c2431;",
        "--border-color: #1d3d3f;": "--border-color: #2b3544;",
        "#113335": "#2c1516",  # html gradient
        "rgba(7, 24, 25, 0.86)": "rgba(10, 11, 16, 0.86)",  # topbar
        "rgba(16, 191, 174,": "rgba(255, 109, 90,",  # various alpha primary
        "#d5fffa": "#ffdfdb",  # context text
        "#dffffb": "#ffffff",  # brand text
        "#c4ece7": "#f1f5f9",  # top link text
        "#e9fffd": "#ffffff",  # top link hover
        "#ecfffc": "#ffffff",  # top link active
        "rgba(11, 31, 32, 0.98)": "rgba(20, 27, 34, 0.98)",  # sidebar
        "rgba(7, 24, 25, 0.98)": "rgba(10, 11, 16, 0.98)",  # sidebar
        "rgba(6, 20, 20,": "rgba(10, 11, 16,",  # content wrapper
        "#031312": "#1a0505",  # nav btn text
        "#102a2c": "#1c2431",  # page
        "#0d2526": "#141b22",  # page
        "#7de6d8": "#ff8a7a",  # a
        "#a7fff2": "#ffaa9e",  # a hover
        "#6ad9cb": "#e55a48",  # a visited
        "#009688": "#ff6d5a",  # logic svg
        "#11c9b7": "#ff8a7a",  # btn grad
        "#0f9d92": "#ea4262",  # btn grad
        "#03211f": "#ffffff",  # cover btn text
        "rgba(10, 153, 139,": "rgba(234, 66, 98,",  # shadow
        "#b4d7d2": "#cbd5e1",  # subtitle
        "#d6f3ef": "#e2e8f0",  # pre text
        "#c9fff8": "#ffdfdb",  # code text
        "rgba(7, 32, 33, 0.95)": "rgba(20, 27, 34, 0.95)",  # copy bg
        "#d9fffb": "#ffffff",  # copy text
        "rgba(13, 57, 58, 0.98)": "rgba(30, 41, 59, 0.98)",  # copy hover
        "#e7fffc": "#ffffff",  # copied text
        "#7ff4e6": "#ffaa9e",  # strong text
        "#95fff2": "#ffdfdb",  # th text
        "#d3f3ef": "#cbd5e1",  # toc a
        "#b8fff6": "#ffffff",  # toc index
        "#9dd7d2": "#94a3b8",  # toc visited
        "rgba(7, 25, 26, 0.95)": "rgba(20, 27, 34, 0.95)",  # link status
        "#dcfffb": "#ffffff",  # link status text
        "rgba(8, 26, 28, 0.98)": "rgba(10, 11, 16, 0.98)",  # topbar mobile
        "rgba(8, 29, 30, 0.95)": "rgba(20, 27, 34, 0.95)",  # sidebar mobile
        "#d4fbf6": "#e2e8f0",  # toc m
        "rgba(2, 12, 12, 0.52)": "rgba(0, 0, 0, 0.6)",  # overlay
    }

    for k, v in replacements.items():
        css = css.replace(k, v)

    with open("src_n8n/styles.css", "w", encoding="utf-8") as f:
        f.write(css)


create_n8n_styles()
