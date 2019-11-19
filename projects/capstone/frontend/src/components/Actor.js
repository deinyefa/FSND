import React from 'react'
import { Col, Card, CardBody, CardTitle, CardText, Button } from 'reactstrap';

export const Actor = ({ actor }) => (
    <Col md="4">
        <Card>
            <CardBody>
                <CardTitle>{actor.name}, {actor.age}</CardTitle>
                <CardText>{actor.gender}</CardText>
                <div className="clearfix p-2">
                    <Button color="primary" className="float-left">Edit</Button>
                    <Button color="danger" className="float-right">Delete</Button>
                </div>
            </CardBody>
        </Card>
    </Col>
)