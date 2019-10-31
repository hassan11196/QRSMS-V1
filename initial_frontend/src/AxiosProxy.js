import axios from 'axios';

export default axios.create({
  baseURL: (process.env.proxy_url === 'http://qrsms-v1.herokuapp.com') ?  `http://qrsms-v1.herokuapp.com` : 'http://localhost:8000',
});