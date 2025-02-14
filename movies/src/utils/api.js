import axios from "axios";

const api=axios.create({
    baseURL:"https://api.themoviedb.org/3/",
    headers: {
        Authorization: `Bearer ${process.env.REACT_APP_ACCESS}`,
        'Content-Type' :'application/json'
    },
});

export const getPopularMovies = ()=> api.get('/movie/popular');
export const getTrendingMovies = ()=> api.get('/trending/movie/week');


