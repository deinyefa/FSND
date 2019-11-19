import React from 'react'
import { Col, Card, CardBody, CardTitle, CardText, Button } from 'reactstrap';

export const Movie = ({ movie }) => (
    <Col md="4">
        <Card>
            <CardBody>
                <CardTitle>{movie.title}</CardTitle>
                <CardText>Release Date: {movie.release_date}</CardText>
                <div className="clearfix p-2">
                    <Button color="primary" className="float-left">Edit</Button>
                    <Button color="danger" className="float-right">Delete</Button>
                </div>
            </CardBody>
        </Card>
    </Col>
)