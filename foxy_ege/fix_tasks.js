const fs = require('fs');

const data = JSON.parse(fs.readFileSync('tasks_data.json', 'utf8'));

data.forEach(task => {
  const fields = task.fields || task;
  if (fields.text) {
    // Оборачиваем текст внутри формул в \text{...}
    fields.text = fields.text.replace(
      /\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g,
      (match, blockContent, inlineContent) => {
        const content = blockContent || inlineContent;
        const fixedContent = content.replace(
          /([а-яА-Я\s]+)(?![^{]*\})/g,
          '\\text{$1}'
        );
        return blockContent ? `\\[${fixedContent}\\]` : `\\(${fixedContent}\\)`;
      }
    );
  }
  if (fields.solution_text) {
    fields.solution_text = fields.solution_text.replace(
      /\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g,
      (match, blockContent, inlineContent) => {
        const content = blockContent || inlineContent;
        const fixedContent = content.replace(
          /([а-яА-Я\s]+)(?![^{]*\})/g,
          '\\text{$1}'
        );
        return blockContent ? `\\[${fixedContent}\\]` : `\\(${fixedContent}\\)`;
      }
    );
    // Исправляем \begin{cases}
    fields.solution_text = fields.solution_text.replace(
      /\\begin\{cases\}([\s\S]*?)\\end\{cases\}/g,
      (match, content) => {
        const lines = content.split('\\\\');
        const fixedLines = lines.map(line => {
          const parts = line.split('&');
          if (parts.length > 1 && !parts[1].includes('\\text{')) {
            const comment = parts[1].trim();
            if (comment.startsWith('(') && comment.endsWith(')')) {
              parts[1] = `\\text{${comment.slice(1, -1)}}`;
            } else {
              parts[1] = `\\text{${comment}}`;
            }
          }
          return parts.join(' & ');
        });
        return `\\begin{cases}${fixedLines.join('\\\\')}\\end{cases}`;
      }
    );
  }
});

fs.writeFileSync('tasks_data_fixed.json', JSON.stringify(data, null, 2), 'utf8');
console.log('Исправленный JSON сохранён: tasks_data_fixed.json');