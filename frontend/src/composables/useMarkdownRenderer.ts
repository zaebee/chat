import { marked } from 'marked';
import DOMPurify from 'dompurify';
import hljs from 'highlight.js';

export function useMarkdownRenderer() {
  const renderMarkdown = (text: string) => {
    const renderer = new marked.Renderer();

    renderer.link = (token) => {
      const { href, title, text } = token;
      if (!href) {
        return text;
      }
      const imageExtensions = [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"];
      const isImage = imageExtensions.some((ext) => href.toLowerCase().endsWith(ext));

      if (isImage) {
        const imageId = `img-wrapper-${Math.random().toString(36).substring(2, 9)}`;
        return `
          <div id="${imageId}" class="chat-image-wrapper collapsed">
            <img src="${href}" alt="${text}" title="${title || text}" class="chat-image" onclick="window.toggleImageExpansion('${imageId}')" />
            <button class="expand-image-btn" onclick="window.toggleImageExpansion('${imageId}')">Expand</button>
          </div>
        `;
      }

      const linkTitle = title || text;
      return `<a href="${href}" title="${linkTitle}" target="_blank" rel="noopener noreferrer">${text}</a>`;
    };

    renderer.code = (token) => {
      const { text: code, lang } = token;
      const language = hljs.getLanguage(lang || "") ? lang : "plaintext";
      const highlightedCode = hljs.highlight(code || "", { language: language || "plaintext" }).value;
      const codeId = `code-${Math.random().toString(36).substring(2, 9)}`;
      const codeWrapperId = `code-wrapper-${Math.random().toString(36).substring(2, 9)}`;

      return `
        <div id="${codeWrapperId}" class="code-block-wrapper collapsed">
          <button onclick="window.copyCodeToClipboardAndProvideFeedback('${codeId}', this)" class="copy-code-btn">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/></svg> Copy
          </button>
          <pre><code id="${codeId}" class="language-${language}">${highlightedCode}</code></pre>
          <button class="expand-code-btn" onclick="window.toggleCodeExpansion('${codeWrapperId}')">Expand</button>
        </div>
      `;
    };

    const rawHtml = marked.parse(text, {
      gfm: true,
      breaks: true,
      renderer: renderer,
    }) as string;
    const sanitizedHtml = DOMPurify.sanitize(rawHtml, { ADD_ATTR: ["target"] });
    return sanitizedHtml;
  };

  return { renderMarkdown };
}
