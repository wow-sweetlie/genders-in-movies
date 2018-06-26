const HtmlWebpackPlugin = require('html-webpack-plugin')
const path = require('path');

module.exports = {
	mode: process.env.WEBPACK_SERVE ? 'development' : 'production',
  entry: './src/index.js',
  output: {
    filename: 'main.js',
    path: path.resolve(__dirname, 'dist')
  },
  module: {
    rules: [
      {
        test: /\.(png|jpg|gif)$/,
        exclude: [/node_modules/],
        use: [
          {
            loader: 'file-loader',
            options: {
              outputPath: 'images/',
              name: '[name][hash].[ext]',
            },
          },
        ],
      },
      {
        test: /\.(sass|scss)$/,
        use: [
          'style-loader',
          'css-loader',
          'sass-loader',
        ]
      },
      {
        test: /\.jsx?$/,
        exclude: [/node_modules/],
        loader: "babel-loader"
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
      inject: 'body',
      })
  ]
};
