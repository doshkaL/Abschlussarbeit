const { override, addBabelPresets } = require('customize-cra');

module.exports = override(
  addBabelPresets('@babel/preset-env', '@babel/preset-react')
);
