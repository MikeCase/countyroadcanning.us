/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './website/templates/**/*.{html,js}',
    './website/blueprints/**/*.{html,js}'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}

