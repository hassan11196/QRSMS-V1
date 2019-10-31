const proxy = require('http-proxy-middleware');

var options = {
    target: 'hhttp://qrsms-v1.herokuapp.com', // target host
    changeOrigin: true, // needed for virtual hosted sites
    ws: true, // proxy websockets
    pathRewrite: {
      '^/bts/': '/', // rewrite path
    },
    router: {
      // when request.headers.host == 'dev.localhost:3000',
      // override target 'http://www.example.org' to 'http://localhost:8000'
      'dev.localhost:3000': 'http://localhost:8000'
    }
  };


module.exports = function(app){
    
    
    // if ((process.env.proxy_url === 'http://qrsms-v1.herokuapp.com') || (process.env.proxy_url === 'https://qrsms-v1.herokuapp.com') ){
    //     app.use(proxy('/management', {target : 'http://qrsms-v1.herokuapp.com'}));
    // }
    // else{
    //     app.use(proxy('/management', {target : 'http://localhost:8000'}));
    // }
    app.use(proxy('/management', {target : 'http://localhost:8000'}));
}
