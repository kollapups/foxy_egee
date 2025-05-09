const fs = require('fs');

// Читаем tasks_data_svg.json
const svgData = JSON.parse(fs.readFileSync('tasks_data_svg.json', 'utf8'));

// Генерируем HTML
let html = `
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Проверка SVG</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .task { margin-bottom: 20px; border-bottom: 1px solid #ccc; }
    .task h2 { color: #333; }
    .svg-content svg { max-width: 100%; height: auto; vertical-align: middle; }
    .latex-error { color: red; font-style: italic; }
  </style>
</head>
<body>
<h1>Проверка отрендеренных SVG</h1>
`;

svgData.forEach(task => {
  const taskId = task.pk || task.fields?.id || 'unknown';
  const fields = task.fields || task;
  html += `
  <div class="task">
    <h2>Задача ${taskId}</h2>
    <h3>Текст:</h3>
    <div class="svg-content">${fields.text_svg || fields.text}</div>
    <h3>Решение:</h3>
    <div class="svg-content">${fields.solution_text_svg || fields.solution_text}</div>
    ${fields.latex_formula_svg ? `<h3>Формула:</h3><div class="svg-content">${fields.latex_formula_svg}</div>` : ''}
  </div>
  `;
});

html += `
</body>
</html>
`;

// Сохраняем HTML
fs.writeFileSync('test_svg.html', html, 'utf8');
console.log('HTML-файл для проверки SVG создан: test_svg.html');