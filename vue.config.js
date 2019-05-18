const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    // publicPath: "http://127.0.0.1:8080/",
    publicPath: "msn-match-test.herokuapp.com/",
    outputDir: './dist/',

    pages: {
        home: {
          // entry for the page
          entry: 'src/home/main.js',
          // the source template
          template: 'templates/home.html',
          // output as dist/home.html
          filename: 'home.html',
          // when using title option,
          // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
        //   title: 'Index Page',
          // chunks to include on this page, by default includes
          // extracted common chunks and vendor chunks.
        //   chunks: ['chunk-vendors', 'chunk-common', 'index']
        },
        // when using the entry-only string format,
        // template is inferred to be `public/subpage.html`
        // and falls back to `public/index.html` if not found.
        // Output filename is inferred to be `subpage.html`.
        superadmin: {
            // entry for the page
            entry: 'src/superadmin/main.js',
            // the source template
            template: 'templates/superadmin.html',
            // output as dist/superadmin.html
            filename: 'superadmin.html',
        }
      },

    chainWebpack: config => {

        config.optimization
            .splitChunks(false)

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: 'webpack-stats.json'}])

        config.resolve.alias
            .set('__STATIC__', 'static')
        
        config.devServer
            .public('http://0.0.0.0:8080')
            .host('0.0.0.0')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
            .clientLogLevel('info')
            }
    };