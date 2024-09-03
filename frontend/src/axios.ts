// src/axios.js
import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000', // TODO - environment variable
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});


export default axiosInstance;