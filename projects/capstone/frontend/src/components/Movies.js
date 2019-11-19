import React, { useState } from 'react';
import { Container, Row } from 'reactstrap';
import { useFetch } from '../utils/hooks/useFetch';
import { Movie } from './Movie'

export const Movies = () => {
    const [pageNum, setPageNum] = useState(1)
    
    const url = `http://localhost:5000/movies?page=${pageNum}`
    const result = useFetch(url, {})

    const selectPage = num => setPageNum(num)
    const create_pagination = () => {
        let pageNumbers = [];
        let maxPage = Math.ceil(result.total_movies / 10)

        for (let i = 1; i <= maxPage; i++) {
            pageNumbers = [...pageNumbers, <span
                key={i}
                className={`page-num ${i === pageNum ? 'active' : ''}`}
                onClick={() => { selectPage(i) }}>{i}
            </span>]
        }
        return pageNumbers
    }

    console.log(result)

    return (
        <Container>
            <h1>Movies!</h1>
            <Row>
                {result.movies ? result.movies.map(movie => <Movie key={movie.id} movie={movie} />) : null}
            </Row>
            <Row>
                {create_pagination()}
            </Row>
        </Container>
    )
}