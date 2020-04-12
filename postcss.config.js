const tailwindcss = require('tailwindcss');

const purgecss = require('@fullhuman/postcss-purgecss')({
  content: ['./src/**/*.vue', './public/index.html'],
  defaultExtractor: (content) => content.match(/[\w-/:.]+(?<!:)/g) || [],
  whitelistPatterns: [],
});

module.exports = {
  plugins: [
    tailwindcss('./tailwind.config.js'),
    require('autoprefixer'),
    ...(process.env.NODE_ENV === 'production' ? [purgecss] : []),
  ],
};
