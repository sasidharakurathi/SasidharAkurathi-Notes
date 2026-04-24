import os

def create_llamaindex_files():
    os.makedirs("src_llamaindex/chapters", exist_ok=True)

    # 1. create styles.css
    with open("src_fastapi/styles.css", "r", encoding="utf-8") as f:
        css = f.read()

    # Color replacements for llamaindex theme (Purple/Violet)
    replacements = {
        "--primary: #10bfae;": "--primary: #9d4edd;",
        "--primary-strong: #0e988c;": "--primary-strong: #7b2cbf;",
        "--bg-main: #061414;": "--bg-main: #08060c;",
        "--bg-surface: #0b1f20;": "--bg-surface: #100b18;",
        "--bg-elevated: #102a2c;": "--bg-elevated: #160f24;",
        "--border-color: #1d3d3f;": "--border-color: #2b1f42;",
        "#113335": "#2a153d",  # html gradient
        "rgba(7, 24, 25, 0.86)": "rgba(9, 7, 14, 0.86)",  # topbar
        "rgba(16, 191, 174,": "rgba(157, 78, 221,",  # various alpha primary
        "#d5fffa": "#eadbfa",  # context text
        "#dffffb": "#ffffff",  # brand text
        "#c4ece7": "#f1e5fa",  # top link text
        "#e9fffd": "#ffffff",  # top link hover
        "#ecfffc": "#ffffff",  # top link active
        "rgba(11, 31, 32, 0.98)": "rgba(16, 11, 24, 0.98)",  # sidebar
        "rgba(7, 24, 25, 0.98)": "rgba(10, 7, 16, 0.98)",  # sidebar
        "rgba(6, 20, 20,": "rgba(10, 8, 16,",  # content wrapper
        "#031312": "#1a0f2b",  # nav btn text
        "#102a2c": "#1b122e",  # page
        "#0d2526": "#140c21",  # page
        "#7de6d8": "#c38cff",  # a
        "#a7fff2": "#dab0ff",  # a hover
        "#6ad9cb": "#a85eff",  # a visited
        "#009688": "#9d4edd",  # logic svg
        "#11c9b7": "#b36cf2",  # btn grad
        "#0f9d92": "#8c3edf",  # btn grad
        "#03211f": "#ffffff",  # cover btn text
        "rgba(10, 153, 139,": "rgba(127, 45, 199,",  # shadow
        "#b4d7d2": "#d1c4e9",  # subtitle
        "#d6f3ef": "#ede7f6",  # pre text
        "#c9fff8": "#ede7f6",  # code text
        "rgba(7, 32, 33, 0.95)": "rgba(16, 11, 24, 0.95)",  # copy bg
        "#d9fffb": "#ffffff",  # copy text
        "rgba(13, 57, 58, 0.98)": "rgba(24, 18, 36, 0.98)",  # copy hover
        "#e7fffc": "#ffffff",  # copied text
        "#7ff4e6": "#dcb3ff",  # strong text
        "#95fff2": "#ede7f6",  # th text
        "#d3f3ef": "#d1c4e9",  # toc a
        "#b8fff6": "#ffffff",  # toc index
        "#9dd7d2": "#a39bb8",  # toc visited
        "rgba(7, 25, 26, 0.95)": "rgba(16, 11, 24, 0.95)",  # link status
        "#dcfffb": "#ffffff",  # link status text
        "rgba(8, 26, 28, 0.98)": "rgba(10, 7, 16, 0.98)",  # topbar mobile
        "rgba(8, 29, 30, 0.95)": "rgba(16, 11, 24, 0.95)",  # sidebar mobile
        "#d4fbf6": "#ede7f6",  # toc m
        "rgba(2, 12, 12, 0.52)": "rgba(0, 0, 0, 0.6)",  # overlay
    }

    for k, v in replacements.items():
        css = css.replace(k, v)

    with open("src_llamaindex/styles.css", "w", encoding="utf-8") as f:
        f.write(css)

    # 2. create script.js
    with open("src_fastapi/script.js", "r", encoding="utf-8") as f:
        js = f.read()

    js = js.replace('handbook: "fastapi",', 'handbook: "llamaindex",')
    js = js.replace('bodyClass: "theme-fastapi",', 'bodyClass: "theme-llamaindex",')
    js = js.replace('contextLabel: "FastAPI Handbook",', 'contextLabel: "LlamaIndex Handbook",')

    with open("src_llamaindex/script.js", "w", encoding="utf-8") as f:
        f.write(js)

    # 3. create toc.html
    with open("src_fastapi/toc.html", "r", encoding="utf-8") as f:
        toc_lines = f.readlines()
        
    toc_html = """<!-- Table of Contents Page -->
<div class="page">
        <div class="header">Table of Contents</div>
        <h2 style="margin-top: 0;">Table of Contents</h2>
        <ul class="toc-list" id="toc">
                <li class="toc-section">PART I - GETTING STARTED</li>
                <li><button type="button" class="toc-link" data-target="#chapter-1">CHAPTER 1 - What is LlamaIndex?</button> <span class="page-num">3</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-2">CHAPTER 2 - High-Level Concepts</button> <span class="page-num">5</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-3">CHAPTER 3 - Installation and Setup</button> <span class="page-num">7</span></li>
                
                <li class="toc-section">PART II - DATA CONNECTORS & INGESTION</li>
                <li><button type="button" class="toc-link" data-target="#chapter-4">CHAPTER 4 - Loading Data (SimpleDirectoryReader)</button> <span class="page-num">10</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-5">CHAPTER 5 - Nodes and Documents</button> <span class="page-num">13</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-6">CHAPTER 6 - Data Transformations (Node Parsers)</button> <span class="page-num">16</span></li>
                
                <li class="toc-section">PART III - INDEXING</li>
                <li><button type="button" class="toc-link" data-target="#chapter-7">CHAPTER 7 - Vector Store Index</button> <span class="page-num">19</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-8">CHAPTER 8 - Summary Index & Keyword Table Index</button> <span class="page-num">22</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-9">CHAPTER 9 - Storage Context & Vector Stores</button> <span class="page-num">25</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-10">CHAPTER 10 - Persisting and Loading Indexes</button> <span class="page-num">28</span></li>
                
                <li class="toc-section">PART IV - QUERYING & RETRIEVAL</li>
                <li><button type="button" class="toc-link" data-target="#chapter-11">CHAPTER 11 - Query Engines vs Chat Engines</button> <span class="page-num">31</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-12">CHAPTER 12 - Retrievers</button> <span class="page-num">34</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-13">CHAPTER 13 - Node Postprocessors & Reranking</button> <span class="page-num">37</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-14">CHAPTER 14 - Response Synthesizers</button> <span class="page-num">40</span></li>
                
                <li class="toc-section">PART V - ADVANCED TOPICS</li>
                <li><button type="button" class="toc-link" data-target="#chapter-15">CHAPTER 15 - Agents & Tools</button> <span class="page-num">43</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-16">CHAPTER 16 - Callbacks & Observability</button> <span class="page-num">47</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-17">CHAPTER 17 - Evaluation</button> <span class="page-num">51</span></li>
                <li><button type="button" class="toc-link" data-target="#chapter-18">CHAPTER 18 - Deployment Patterns</button> <span class="page-num">55</span></li>
        </ul>
        <div class="footer">
                <span>LlamaIndex Complete Handbook</span>
                <span>Page 2</span>
        </div>
</div>
"""
    with open("src_llamaindex/toc.html", "w", encoding="utf-8") as f:
        f.write(toc_html)

if __name__ == "__main__":
    create_llamaindex_files()
