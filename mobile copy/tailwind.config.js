/** @type {import('tailwindcss').Config} */
module.exports = {
  // files where tailwind can be used (feel free to add more as needed)
  content: [
    "./assets/**/*.js",
    "./components/**/*.js",
    "./screens/**/*.js",
    "./navigation/**/*.js",
    "./models/**/*.js",
    "./translations/**/*.js",
    "./App.js",
],
  mode: 'jit',

  theme: {
    extend: {
      colors: {
        'gray': '#D1D5DB',
        'offwhite': '#FEFFF4',
        'lavenderlight': '#DDD6F6',
        'lavender': '#C0B3F1',
        'salmon': '#ff7f73',
        'teal': '#00394E',
        'turquoise': '#005C6A',
        'seafoam': '#5B9F8F',
        'greydark': '#272727',
        'dullwhite': '#EDEEE0'
      }
    }
  },

  plugins: [],
    safelist: [{
      pattern: /(bg|text|border)-(gray|offwhite|lavenderlight|lavender|salmon|teal|turquoise|seafoam|greydark)/
    },
    {
      pattern: /(h|w)-(full|1\/4|1\/2|3\/4)/
    }
  ]
}
