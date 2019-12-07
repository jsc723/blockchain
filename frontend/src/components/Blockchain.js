import React, {useState, useEffect} from 'react'
import {Link} from 'react-router-dom';
import { API_BASE_URL } from '../config'
import Block from './Block'
import { Button } from 'react-bootstrap'

const PAGE_RANGE = 3;


function Blockchain() {
    const [blockchain, setBlockchain] = useState([]);
    const [blockchainLength, setBlockchainLength] = useState(0);
    const fetchBlockchainPage = ({start, end}) => {
        fetch(`${API_BASE_URL}/blockchain/range?start=${start}&end=${end}`)
            .then(response => response.json())
            .then(json => setBlockchain(json));
    }
    useEffect(()=>{
        fetchBlockchainPage({start: 0, end: PAGE_RANGE});
        fetch(`${API_BASE_URL}/blockchain/length`)
            .then(response => response.json())
            .then(json => setBlockchainLength(json));
    }, []);

    const buttonNumbers = [];
    for (let i=0; i < blockchainLength/PAGE_RANGE; i++) {
        buttonNumbers.push(i);
    }

    return (
        <div>
            <Link to='/'>Home</Link>
            <hr />
            <h3>BLockchain</h3>
            <div>
                {
                    blockchain.map(block =>  <Block key={block.hash} block={block}/>)
                }
            </div>
            <div>
                {
                    buttonNumbers.map(number => {
                        const start = number * PAGE_RANGE;
                        const end = start + PAGE_RANGE;
                        return (
                            <span key={number} onClick={() => fetchBlockchainPage({start, end})}>
                                <Button size="sm" varient="danger">
                                    {number+1}
                                </Button>{' '}
                            </span>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Blockchain