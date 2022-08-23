module.exports = {

  darkMode: 'class',
  theme: {
    screens: {
      'sm': '320px',
      // => @media (min-width: 640px) { ... }
      'm': '475px',
      'ml': '425px',
      'md': '768px',
      // => @media (min-width: 768px) { ... }

      'lg': '1024px',
      // => @media (min-width: 1024px) { ... }

      'xl': '1280px',
      // => @media (min-width: 1280px) { ... }

      '2xl': '1536px',
      // => @media (min-width: 1536px) { ... }
    },container: {
      center: true,
    },
    extend: {
      colors: {
          transparent: 'transparent',
          current: 'currentColor',
          'white': '#ffffff',
          'purple': '#3f3cbb',
          'midnight': '#121063',
          'metal': '#565584',
          'tahiti': '#3ab7bf',
          'silver': '#ecebff',
          'bubble-gum': '#ff77e9',
          'bermuda': '#78dcca',
          'red': {
            '100': '#ffeaea',
            '200': '#ffc9c9',
            '300': '#ff9d9d',
            '400': '#ff6b6b',
            '500': '#ff4d4d',
            '600': '#ff3b3b',
            '700': '#ff2a2a',
            '800': '#ff1a1a',
            '900': '#ff0000',
          },
        },
        backgroundImage: {
          'gradient-purple': 'linear-gradient(to bottom, #3f3cbb, #121063)',
          'ml-view': 'url(https://i.imgur.com/0iFiz7f.png)',
          'valorant-view': 'url(https://i.imgur.com/DAqnrMC.png)',
          'dota-view': 'url(https://i.imgur.com/cFUMMxQ.png)',
          'cod-view': 'url(https://i.imgur.com/xO7ngnQ.png)',
          'pubg-view': 'url(https://i.imgur.com/c4JxF6e.png)',
          'midlane': 'url(https://i.imgur.com/JFY6fQP.png)',
          'jungler': 'url(https://i.imgur.com/Ijt8Ck5.png)',
          'goldlaner': 'url(https://i.imgur.com/nob1TRl.png)',
          'explaner': 'url(https://i.imgur.com/tpmVFsc.png)',
          'tank': 'url(https://i.imgur.com/AIrboqY.png)',
        },
    },
  }, 
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  plugins: [
    require('flowbite/plugin')
  ],
}