(() => {
    const config = {
        handbook: "n8n",
        bodyClass: "theme-n8n",
        contextLabel: "n8n Handbook",
        copyLabel: "Copy",
        copiedLabel: "Copied",
    };

    const onReady = (callback) => {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", callback, { once: true });
        } else {
            callback();
        }
    };

    const normalizePath = (value) => {
        if (!value) return "/";
        const clean = value.replace(/\/+$/, "");
        return clean.length ? clean : "/";
    };

    const markActiveTocLink = () => {
        const links = Array.from(document.querySelectorAll(".toc-list a, .toc-list .toc-link"));
        if (!links.length) return;

        const currentPath = normalizePath(window.location.pathname);

        links.forEach((link) => {
            const rawHref = link.getAttribute("href") || link.getAttribute("data-href") || "";
            if (!rawHref || rawHref.startsWith("#")) return;

            const url = new URL(rawHref, window.location.origin);
            const targetPath = normalizePath(url.pathname);
            const targetNoExt = normalizePath(targetPath.replace(/\.html$/i, ""));
            const currentNoExt = normalizePath(currentPath.replace(/\.html$/i, ""));

            const isActive = currentPath === targetPath || currentNoExt === targetNoExt;
            link.classList.toggle("active", isActive);
            if (isActive) {
                link.setAttribute("aria-current", "page");
            } else {
                link.removeAttribute("aria-current");
            }
        });
    };

    const enhanceTocItems = () => {
        const links = Array.from(document.querySelectorAll(".toc-list a, .toc-list .toc-link"));
        links.forEach((link, index) => {
            const original = (link.textContent || "").trim();
            if (!original) return;

            if (link.querySelector(".toc-index")) return;

            link.textContent = "";

            const indexBadge = document.createElement("span");
            indexBadge.className = "toc-index";
            indexBadge.textContent = String(index + 1).padStart(2, "0");

            const label = document.createElement("span");
            label.className = "toc-label";
            label.textContent = original;

            link.append(indexBadge, label);
        });
    };

    const updateTopbarContext = () => {
        const context = document.getElementById("topbar-context");
        if (!(context instanceof HTMLElement)) return;

        const activeLink = document.querySelector(".toc-list a.active, .toc-list .toc-link.active");
        const activeLabel =
            activeLink?.querySelector(".toc-label")?.textContent || activeLink?.textContent || "";
        const cleanLabel = activeLabel.replace(/^\s*\d{1,2}\s*/, "").trim();
        const suffix = cleanLabel ? ` • ${cleanLabel}` : "";
        context.textContent = `${config.contextLabel}${suffix}`;
    };

    const setupTocToggle = () => {
        const toggle = document.getElementById("toc-toggle");
        const sidebar = document.getElementById("toc-sidebar");
        if (!(toggle instanceof HTMLButtonElement) || !(sidebar instanceof HTMLElement)) return;

        const updateToggleState = (isOpen) => {
            toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
            toggle.classList.toggle("is-open", isOpen);
            toggle.setAttribute(
                "aria-label",
                isOpen ? "Close table of contents" : "Open table of contents"
            );
        };

        const closeToc = () => {
            document.body.classList.remove("toc-open");
            updateToggleState(false);
        };

        toggle.addEventListener("click", () => {
            const isOpen = document.body.classList.toggle("toc-open");
            updateToggleState(isOpen);
        });

        sidebar.addEventListener("click", (event) => {
            if ((event.target instanceof Element) && event.target.closest("a, .toc-link")) {
                closeToc();
            }
        });

        document.addEventListener("click", (event) => {
            if (window.innerWidth > 1000) return;
            if (!document.body.classList.contains("toc-open")) return;
            if (!(event.target instanceof Element)) return;
            if (event.target.closest("#toc-sidebar") || event.target.closest("#toc-toggle")) return;
            closeToc();
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth > 1000) closeToc();
        });

        updateToggleState(false);
    };

    const setupTocNavigation = () => {
        const tocButtons = Array.from(document.querySelectorAll(".toc-list .toc-link[data-href]"));
        tocButtons.forEach((button) => {
            button.addEventListener("click", () => {
                const href = button.getAttribute("data-href") || "";
                if (!href) return;
                window.location.href = href;
            });
        });
    };

    const setupKeyboardNavigation = () => {
        const navLinks = Array.from(document.querySelectorAll(".nav-buttons .nav-btn:not(.disabled)"));
        if (!navLinks.length) return;

        const prevLink = navLinks[0] || null;
        const nextLink = navLinks.length > 1 ? navLinks[1] : null;

        document.addEventListener("keydown", (event) => {
            const tag = (event.target && event.target.tagName) || "";
            if (tag === "INPUT" || tag === "TEXTAREA" || event.metaKey || event.ctrlKey || event.altKey) {
                return;
            }

            if (event.key === "ArrowLeft" && prevLink) {
                window.location.href = prevLink.href;
            }

            if (event.key === "ArrowRight" && nextLink) {
                window.location.href = nextLink.href;
            }
        });
    };

    const secureExternalLinks = () => {
        const links = Array.from(document.querySelectorAll("a[href]"));
        links.forEach((link) => {
            const href = link.getAttribute("href") || "";
            if (!/^https?:\/\//i.test(href)) return;
            if (href.includes(window.location.hostname)) return;

            link.setAttribute("target", "_blank");
            link.setAttribute("rel", "noopener noreferrer");
        });
    };

    const normalizeCodeBlocks = () => {
        const preBlocks = Array.from(document.querySelectorAll("pre"));
        preBlocks.forEach((pre) => {
            if (pre.querySelector("code")) return;

            const text = pre.textContent || "";
            pre.textContent = "";

            const code = document.createElement("code");
            code.textContent = text.trimEnd();

            const dataLang = (pre.getAttribute("data-lang") || "").trim();
            if (dataLang) code.classList.add(`language-${dataLang.toLowerCase()}`);

            pre.appendChild(code);
        });
    };

    const setupLinkStatusPreview = () => {
        const items = Array.from(document.querySelectorAll(".toc-list .toc-link[data-href]"));
        if (!items.length) return;

        const status = document.createElement("div");
        status.className = "link-status";
        status.setAttribute("aria-hidden", "true");
        document.body.appendChild(status);

        let hideTimer = null;

        const hideStatus = () => {
            status.classList.remove("is-visible");
            if (hideTimer) window.clearTimeout(hideTimer);
            hideTimer = window.setTimeout(() => {
                status.textContent = "";
            }, 160);
        };

        items.forEach((item) => {
            const rawHref = (item.getAttribute("data-href") || "").trim();
            if (!rawHref) return;

            const showStatus = () => {
                if (hideTimer) {
                    window.clearTimeout(hideTimer);
                    hideTimer = null;
                }
                const url = new URL(rawHref, window.location.origin);
                const label = `${url.host}${url.pathname}${url.search}${url.hash}`;
                if (!label) return;
                status.textContent = label;
                status.classList.add("is-visible");
            };

            item.addEventListener("mouseenter", showStatus);
            item.addEventListener("focus", showStatus);
            item.addEventListener("mouseleave", hideStatus);
            item.addEventListener("blur", hideStatus);
        });
    };

    const setupCodeCopyButtons = () => {
        const blocks = Array.from(document.querySelectorAll("pre > code"));
        blocks.forEach((code) => {
            const pre = code.parentElement;
            if (!pre || pre.querySelector(".copy-btn")) return;

            const wrapper = document.createElement("div");
            wrapper.className = "code-wrapper";
            pre.parentNode.insertBefore(wrapper, pre);
            wrapper.appendChild(pre);

            const button = document.createElement("button");
            button.className = "copy-btn";
            button.type = "button";
            button.textContent = config.copyLabel;

            button.addEventListener("click", async () => {
                try {
                    await navigator.clipboard.writeText(code.textContent || "");
                    button.textContent = config.copiedLabel;
                    button.classList.add("copied");
                    window.setTimeout(() => {
                        button.textContent = config.copyLabel;
                        button.classList.remove("copied");
                    }, 1300);
                } catch {
                    button.textContent = "Failed";
                    window.setTimeout(() => {
                        button.textContent = config.copyLabel;
                    }, 1300);
                }
            });

            wrapper.appendChild(button);
        });
    };

    const init = () => {
        document.body.classList.add(config.bodyClass);
        normalizeCodeBlocks();
        enhanceTocItems();
        markActiveTocLink();
        updateTopbarContext();
        setupTocToggle();
        setupTocNavigation();
        setupKeyboardNavigation();
        secureExternalLinks();
        setupLinkStatusPreview();
        setupCodeCopyButtons();
    };

    onReady(init);
})();
