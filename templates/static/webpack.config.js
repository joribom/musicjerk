const webpack = require('webpack');
const resolve = require('path').resolve;

const config = {
 devtool: 'eval-source-map',
 entry: __dirname + '/js/index.jsx',
 output:{
  path: resolve('../public'),
  filename: 'bundle.js',
  publicPath: resolve('../public')
},
 resolve: {
  extensions: ['.js','.jsx','.css']
 },
 module: {
  rules: [
  {
   test: /\.jsx?/,
   loader: 'babel-loader',
   exclude: /node_modules/
  },
  {
   test: /\.css$/,
   loader: 'style-loader!css-loader?modules'
  }]
  },
  externals: {
    moment: 'moment'
  }
};

if (process.env.NODE_ENV = "production"){
  config.mode = "production";
  config.devtool = undefined;
}

module.exports = config;
