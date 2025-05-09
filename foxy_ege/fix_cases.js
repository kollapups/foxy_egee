const fs = require('fs');

const data = JSON.parse(fs.readFileSync('tasks_data.json', 'utf8'));

data.forEach(task => {
  const fields = task.fields || task;
  if (fields.solution_text) {
    // Оборачиваем текст после & в \text{...}
    fields.solution_text = fields.solution_text.replace(
      /\\begin\{cases\}(.*?)\\end\{cases\}/gs,
      (match, content) => {
        const lines = content.split('\\\\');
        const fixedLines = lines.map(line => {
          const parts = line.split('&');
          if (parts.length > 1 && !parts[1].includes('\\text{')) {
            parts[1] = `\\text{${parts[1].trim()}}`;
          }
          return parts.join('&');
        });
        return `\\begin{cases}${fixedLines.join('\\\\')}\\end{cases}`;
      }
    );
  }
});

fs.writeFileSync('tasks_data_fixed.json', JSON.stringify(data, null, 2), 'utf8');
console.log('Исправленный JSON сохранён: tasks_data_fixed.json');