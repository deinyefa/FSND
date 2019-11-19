import React, { useState } from 'react';
import { Container, Row } from 'reactstrap';
import { useFetch } from '../utils/hooks/useFetch';
import { Actor } from './Actor'

export const Actors = () => {
    const [pageNum, setPageNum] = useState(1)
    
    const url = `http://localhost:5000/actors?page=${pageNum}`
    const result = useFetch(url, {})

    const selectPage = num => setPageNum(num)
    const create_pagination = () => {
        let pageNumbers = [];
        let maxPage = Math.ceil(result.total_actors / 10)

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
            <h1>Actors!</h1>
            <Row>
                {result.actors ? result.actors.map(actor => <Actor key={actor.id} actor={actor} />) : null}
            </Row>
            <Row>
                {create_pagination()}
            </Row>
        </Container>
    )
}