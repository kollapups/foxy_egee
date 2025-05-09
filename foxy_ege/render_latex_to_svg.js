const fs = require('fs');
const mjAPI = require('mathjax-node');

mjAPI.config({
  MathJax: {
    SVG: {
      font: 'TeX',
      linebreaks: { automatic: false },
    },
  },
});
mjAPI.start();

function stripHtml(html) {
  return html.replace(/<[^>]+>/g, '');
}

async function renderLatexToSVG(latex, latexType = 'inline') {
  try {
    const result = await mjAPI.typeset({
      math: latex,
      format: 'TeX',
      svg: true,
      linebreaks: false,
    });
    const cleanSvg = result.svg.replace(/(\r\n|\n|\r)+/g, ' ').trim();
    const svgWithAttributes = cleanSvg.replace(
      '<svg ',
      `<svg data-latex-type="${latexType}" class="${latexType}-formula" `
    );
    return svgWithAttributes;
  } catch (error) {
    console.error(`Ошибка рендеринга LaTeX: ${latex.slice(0, 50)}...`, error.message);
    return `<span class="latex-error">${latex}</span>`;
  }
}

function cleanLatexFormula(latex) {
  if (!latex) return latex;
  return latex
    .replace(/^\\\[([\s\S]*?)\\\]$/, '$1')
    .replace(/^\\\(([\s\S]*?)\\\)$/, '$1')
    .replace(/^\$\$([\s\S]*?)\$\$$/, '$1')
    .replace(/^\$([\s\S]*?)\$$/, '$1')
    .trim();
}

function getLatexType(latex) {
  if (
    latex.includes('\\begin{array}') ||
    latex.includes('\\begin{cases}') ||
    latex.includes('\\begin{aligned}')
  ) {
    return 'complex';
  }
  if (latex.match(/^\\\[.*\\\]$/)) {
    return 'display';
  }
  return 'inline';
}

async function processLatexFragment(latex) {
  const latexType = getLatexType(latex);
  console.log(`Рендеринг LaTeX: ${latex.slice(0, 50)}... (Тип: ${latexType})`);
  return await renderLatexToSVG(latex, latexType);
}

async function processText(text) {
  if (!text) return null;

  const cleanText = stripHtml(text);
  const latexRegex = /\$\$([\s\S]*?)\$\$|\$(?!\$)([\s\S]*?)(?<!\\)\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g;
  const newlineRegex = /\[NEWLINE\]/g;

  let result = '';
  let lastIndex = 0;
  let match;

  while ((match = latexRegex.exec(cleanText)) !== null) {
    // Добавляем текст до формулы
    result += cleanText.slice(lastIndex, match.index).replace(/\s+/g, ' ');
    const latex = match[1] || match[2] || match[3] || match[4];
    const processed = await processLatexFragment(latex);
    result += processed;
    lastIndex = latexRegex.lastIndex;
  }

  // Добавляем оставшийся текст
  result += cleanText.slice(lastIndex).replace(/\s+/g, ' ');
  // Заменяем [NEWLINE] на <br>
  result = result.replace(newlineRegex, '<br>');
  // Нормализуем пробелы
  result = result.replace(/\s+/g, ' ').trim();

  return result;
}

async function processTasks() {
  try {
    const inputData = JSON.parse(fs.readFileSync('tasks_data.json', 'utf8'));
    const outputData = [];
    for (const task of inputData) {
      const taskId = task.pk || task.fields?.id || 'unknown';
      console.log(`Обработка задачи ${taskId}`);
      const processedTask = { ...task };
      const fields = task.fields || task;

      if (fields.text) {
        console.log(`Обработка text для задачи ${taskId}: ${fields.text.slice(0, 50)}...`);
        processedTask.fields.text_svg = await processText(fields.text);
      }
      if (fields.solution_text) {
        console.log(`Обработка solution_text для задачи ${taskId}: ${fields.solution_text.slice(0, 50)}...`);
        processedTask.fields.solution_text_svg = await processText(fields.solution_text);
      }
      if (fields.latex_formula) {
        console.log(`Обработка latex_formula для задачи ${taskId}: ${fields.latex_formula.slice(0, 50)}...`);
        const cleanedLatex = cleanLatexFormula(fields.latex_formula);
        processedTask.fields.latex_formula_svg = await renderLatexToSVG(cleanedLatex, getLatexType(cleanedLatex));
      }

      outputData.push(processedTask);
    }

    fs.writeFileSync('tasks_data_svg.json', JSON.stringify(outputData, null, 2), 'utf8');
    console.log('Обработка завершена. Результат сохранён в tasks_data_svg.json');
  } catch (err) {
    console.error('Ошибка при обработке задач:', err);
  }
}

processTasks();