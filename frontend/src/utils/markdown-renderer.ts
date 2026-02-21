/**
 * Lightweight markdown-to-HTML renderer for grammar summary content.
 * Supports: headings, bold, italic, code, tables, blockquotes, lists, hr, custom boxes.
 */
export function renderMarkdown(text: string): string {
  return text
    // Custom boxes: :::tip, :::example, :::warning
    .replace(/:::tip\n([\s\S]*?):::/gm, (_, c) => `<div class="tip-box"><strong>💡 Mẹo:</strong> ${c.trim()}</div>`)
    .replace(/:::example\n([\s\S]*?):::/gm, (_, c) => `<div class="example-box"><strong>📝 Ví dụ:</strong><br>${c.trim()}</div>`)
    .replace(/:::warning\n([\s\S]*?):::/gm, (_, c) => `<div class="warning-box"><strong>⚠️ Lưu ý:</strong> ${c.trim()}</div>`)
    // Headings
    .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    // Horizontal rule (before list processing)
    .replace(/^---$/gm, '<hr>')
    // Bold and italic
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // Blockquotes
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // Tables: convert markdown table rows to HTML
    .replace(/^\|(.+)\|$/gm, (row) => {
      const cells = row.slice(1, -1).split('|').map(c => c.trim())
      return `<tr>${cells.map(c => `<td>${c}</td>`).join('')}</tr>`
    })
    // Wrap consecutive <tr> blocks in <table>, promote first row to <thead>
    .replace(/(<tr>[\s\S]*?<\/tr>\n?)+/g, (block) => {
      const rows = block.trim().split('\n').filter(r => r.startsWith('<tr>'))
      if (rows.length === 0) return block
      const [head, , ...body] = rows
      const thead = head
        .replace(/<td>/g, '<th>')
        .replace(/<\/td>/g, '</th>')
      // Filter out separator rows (cells containing only dashes)
      const bodyRows = body.filter(r => !/<td>-+<\/td>/.test(r))
      return `<div class="table-wrapper"><table><thead>${thead}</thead><tbody>${bodyRows.join('\n')}</tbody></table></div>`
    })
    // Unordered lists
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>\n?)+/g, match => `<ul>${match}</ul>`)
    // Paragraphs: wrap non-tag lines
    .replace(/^(?!<[a-z/])(.+)$/gm, line => line.trim() ? `<p>${line}</p>` : '')
    // Clean up blank lines between tags
    .replace(/\n{2,}/g, '\n')
}
