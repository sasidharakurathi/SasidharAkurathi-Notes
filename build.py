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

    js_script = """
                <script type="text/javascript">
                    (function(c,l,a,r,i,t,y){
                        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
                    })(window, document, "clarity", "script", "vxhj0j0zwn");
                </script>
    
                <script>
                        (function () {
                            const pages = Array.from(document.querySelectorAll('.page'));
                            const tocContainer = document.getElementById('toc');
                            const prevBtn = document.getElementById('btn-prev-page');
                            const nextBtn = document.getElementById('btn-next-page');
                            const topBtn = document.getElementById('btn-top');
                            const linkStatus = document.getElementById('link-status');
                            if (!pages.length || !prevBtn || !nextBtn || !topBtn) {
                                return;
                            }

                            let currentPage = 0;
                            let activeAnimation = null;

                            function easeInOutCubic(t) {
                                return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
                            }

                            function animateTo(targetY, duration) {
                                const startY = window.scrollY || document.documentElement.scrollTop || 0;
                                const maxY = Math.max(document.documentElement.scrollHeight - window.innerHeight, 0);
                                const clampedTarget = Math.min(Math.max(targetY, 0), maxY);
                                const distance = clampedTarget - startY;

                                if (Math.abs(distance) < 1) {
                                    window.scrollTo(0, clampedTarget);
                                    return;
                                }

                                if (activeAnimation) {
                                    cancelAnimationFrame(activeAnimation);
                                    activeAnimation = null;
                                }

                                const startTime = performance.now();

                                function step(now) {
                                    const elapsed = now - startTime;
                                    const progress = Math.min(elapsed / duration, 1);
                                    const eased = easeInOutCubic(progress);
                                    window.scrollTo(0, startY + (distance * eased));

                                    if (progress < 1) {
                                        activeAnimation = requestAnimationFrame(step);
                                    } else {
                                        activeAnimation = null;
                                    }
                                }

                                activeAnimation = requestAnimationFrame(step);
                            }

                            function getCurrentPageIndex() {
                                const mid = window.innerHeight * 0.5;
                                let bestIndex = 0;
                                let bestDistance = Number.POSITIVE_INFINITY;

                                pages.forEach(function (page, index) {
                                    const rect = page.getBoundingClientRect();
                                    const pageMid = rect.top + rect.height * 0.5;
                                    const distance = Math.abs(pageMid - mid);
                                    if (distance < bestDistance) {
                                        bestDistance = distance;
                                        bestIndex = index;
                                    }
                                });

                                return bestIndex;
                            }

                            function updateButtonStates() {
                                currentPage = getCurrentPageIndex();
                                prevBtn.disabled = currentPage <= 0;
                                nextBtn.disabled = currentPage >= pages.length - 1;
                            }

                            function scrollToPage(index) {
                                if (index < 0 || index >= pages.length) {
                                    return;
                                }
                                const targetY = pages[index].offsetTop;
                                animateTo(targetY, 560);
                            }

                            function getPreviewUrl(targetSelector) {
                                return window.location.origin + window.location.pathname + targetSelector;
                            }

                            function showLinkStatus(targetSelector) {
                                if (!linkStatus || !targetSelector) {
                                    return;
                                }

                                linkStatus.textContent = getPreviewUrl(targetSelector);
                                linkStatus.classList.add('is-visible');
                            }

                            function hideLinkStatus() {
                                if (!linkStatus) {
                                    return;
                                }

                                linkStatus.classList.remove('is-visible');
                            }

                            prevBtn.addEventListener('click', function () {
                                updateButtonStates();
                                scrollToPage(currentPage - 1);
                            });

                            nextBtn.addEventListener('click', function () {
                                updateButtonStates();
                                scrollToPage(currentPage + 1);
                            });

                            topBtn.addEventListener('click', function () {
                                animateTo(0, 560);
                            });

                            if (tocContainer) {
                                tocContainer.addEventListener('mouseover', function (event) {
                                    const target = event.target;
                                    if (!(target instanceof Element)) {
                                        return;
                                    }

                                    const link = target.closest('.toc-link[data-target]');
                                    if (!(link instanceof HTMLElement)) {
                                        hideLinkStatus();
                                        return;
                                    }

                                    showLinkStatus(link.dataset.target || '');
                                });

                                tocContainer.addEventListener('mouseout', function (event) {
                                    const relatedTarget = event.relatedTarget;
                                    if (relatedTarget instanceof Node && tocContainer.contains(relatedTarget)) {
                                        return;
                                    }

                                    hideLinkStatus();
                                });

                                tocContainer.addEventListener('focusin', function (event) {
                                    const target = event.target;
                                    if (!(target instanceof HTMLElement)) {
                                        return;
                                    }

                                    const link = target.closest('.toc-link[data-target]');
                                    if (!(link instanceof HTMLElement)) {
                                        return;
                                    }

                                    showLinkStatus(link.dataset.target || '');
                                });

                                tocContainer.addEventListener('focusout', function (event) {
                                    const relatedTarget = event.relatedTarget;
                                    if (relatedTarget instanceof Node && tocContainer.contains(relatedTarget)) {
                                        return;
                                    }

                                    hideLinkStatus();
                                });

                                tocContainer.addEventListener('click', function (event) {
                                    const target = event.target;
                                    if (!(target instanceof Element)) {
                                        return;
                                    }

                                    const link = target.closest('.toc-link[data-target]');
                                    if (!(link instanceof HTMLElement)) {
                                        return;
                                    }

                                    const targetSelector = link.dataset.target;
                                    if (!targetSelector || targetSelector.length < 2) {
                                        return;
                                    }

                                    const section = document.querySelector(targetSelector);
                                    if (!(section instanceof HTMLElement)) {
                                        return;
                                    }

                                    event.preventDefault();
                                    hideLinkStatus();
                                    animateTo(section.offsetTop, 620);

                                    if (history && typeof history.replaceState === 'function') {
                                        history.replaceState(null, '', targetSelector);
                                    }
                                });
                            }

                            window.addEventListener('scroll', updateButtonStates, { passive: true });
                            window.addEventListener('resize', updateButtonStates);
                            updateButtonStates();
                        })();
                    </script>"""

    html_template = f"""<!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>FastAPI Complete Handbook</title>
                <style>
                    {css}
                </style>
            </head>
            <body>

                {cover}

                {toc}

                {chapters_content}

                <div id="link-status" class="link-status" aria-hidden="true"></div>

                <div class="floating-controls" aria-label="Page navigation controls">
                    <button id="btn-prev-page" type="button" class="floating-btn">Prev Page</button>
                    <button id="btn-next-page" type="button" class="floating-btn">Next Page</button>
                    <button id="btn-top" type="button" class="floating-btn floating-btn-top">Top</button>
                </div>

                {js_script}

            </body>
        </html>
    """

    with open(dist_file, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Successfully built {dist_file}")


if __name__ == "__main__":
    build_handbook()
