const { mathjax } = require('mathjax-full/js/mathjax');
const { TeX } = require('mathjax-full/js/input/tex');
const { SVG } = require('mathjax-full/js/output/svg');
const { liteAdaptor } = require('mathjax-full/js/adaptors/liteAdaptor');
const { RegisterHTMLHandler } = require('mathjax-full/js/handlers/html');

async function renderFormula(latex) {
    try {
        const adaptor = liteAdaptor();
        RegisterHTMLHandler(adaptor);

        const tex = new TeX({
            packages: ['base', 'ams', 'amsmath', 'amssymb'],
            formatError: (jax, err) => `<span style="color: red;">Ошибка: ${err.message}</span>`,
        });
        const svg = new SVG({ fontCache: 'global', scale: 1.2 });

        const doc = mathjax.document('', {
            InputJax: tex,
            OutputJax: svg,
        });

        const node = doc.convert(latex, { display: true });
        if (!node) {
            throw new Error('Не удалось преобразовать формулу');
        }
        return adaptor.outerHTML(node);
    } catch (error) {
        console.error('Ошибка рендеринга MathJax:', error.message);
        return `<span style="color: red;">Ошибка рендеринга формулы: ${latex}</span>`;
    }
}

if (process.argv.length > 2) {
    const latex = process.argv[2];
    renderFormula(latex).then(svg => {
        console.log(svg);
        process.exit(0);
    }).catch(err => {
        console.error('Ошибка в процессе рендеринга:', err.message);
        process.exit(1);
    });
}

module.exports = { renderFormula };