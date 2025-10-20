module.exports = {
  presets: [
    ['@vue/cli-plugin-babel/preset', {
      useBuiltIns: false
    }]
  ],
  env: {
    development: {
      sourceMaps: true,
      retainLines: true
    }
  }
};
