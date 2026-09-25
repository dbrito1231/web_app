import { useState, type ReactElement, type ReactNode } from 'react';

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      className="copy-btn"
      onClick={async () => {
        await navigator.clipboard.writeText(text);
        setCopied(true);
        window.setTimeout(() => setCopied(false), 1500);
      }}
    >
      {copied ? 'Copied' : 'Copy'}
    </button>
  );
}

export function MarkdownBody({ source }: { source: string }) {
  const blocks = source.split(/\n```/);
  const nodes: ReactElement[] = [];

  blocks.forEach((block, index) => {
    if (index === 0) {
      nodes.push(...renderTextBlock(block, `t-${index}`));
      return;
    }
    const newline = block.indexOf('\n');
    const lang = newline >= 0 ? block.slice(0, newline).trim() : '';
    const code = newline >= 0 ? block.slice(newline + 1) : block;
    const trimmed = code.replace(/\n```$/, '').trimEnd();
    nodes.push(
      <div className="code-block-wrap" key={`c-${index}`}>
        <div className="code-block-head">
          <span className="code-lang">{lang || 'code'}</span>
          <CopyButton text={trimmed} />
        </div>
        <pre>
          <code>{trimmed}</code>
        </pre>
      </div>,
    );
    const tail = block.includes('```') ? '' : '';
    if (tail) nodes.push(...renderTextBlock(tail, `tail-${index}`));
  });

  return <div className="markdown-body">{nodes}</div>;
}

function renderTextBlock(text: string, keyPrefix: string): ReactElement[] {
  const lines = text.split('\n');
  const out: ReactElement[] = [];
  let list: string[] | null = null;

  const flushList = (at: number) => {
    if (!list?.length) return;
    out.push(
      <ul key={`${keyPrefix}-ul-${at}`}>
        {list.map((item) => (
          <li key={item}>{inlineFormat(item)}</li>
        ))}
      </ul>,
    );
    list = null;
  };

  lines.forEach((line, i) => {
    const trimmed = line.trim();
    if (!trimmed) {
      flushList(i);
      return;
    }
    if (trimmed.startsWith('- ')) {
      if (!list) list = [];
      list.push(trimmed.slice(2));
      return;
    }
    flushList(i);
    if (trimmed.startsWith('## ')) {
      out.push(
        <h3 key={`${keyPrefix}-h-${i}`}>{trimmed.slice(3)}</h3>,
      );
      return;
    }
    if (trimmed.startsWith('# ')) {
      out.push(
        <h2 key={`${keyPrefix}-h1-${i}`}>{trimmed.slice(2)}</h2>,
      );
      return;
    }
    out.push(<p key={`${keyPrefix}-p-${i}`}>{inlineFormat(trimmed)}</p>);
  });
  flushList(lines.length);
  return out;
}

function inlineFormat(text: string): ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={i}>{part.slice(1, -1)}</code>;
    }
    return part;
  });
}
