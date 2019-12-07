import React , {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';
import Transaction from './Transaction';
import {Button} from 'react-bootstrap';
import {API_BASE_URL,  SECONDS_JS} from '../config';
import history from '../history';

const POLL_INTERVAL = 10 * SECONDS_JS;

function TransactionPool() {
    const [transactions, setTransactions] = useState([]);
    const fetchTransactions = () => {
        fetch(`${API_BASE_URL}/transactions`)
        .then(response => response.json())
        .then(json => {
            console.log('transactions json', json);
            setTransactions(json);
        });
    }

    useEffect(() => {
        fetchTransactions();
        const id = setInterval(fetchTransactions, POLL_INTERVAL);
        return () => clearInterval(id);
    }, []);

    const fetchMineBlock = () => {
        fetch(`${API_BASE_URL}/blockchain/mine`)
        .then(() => {
            alert('Success');
            history.push('/blockchain');
        })
    }

    return (
        <div className="TransactionPool">
            <Link to="/">Home</Link>
            <h3>Transaction Pool</h3>
            <div>
                {
                    transactions.map(transaction => (
                        <div key={transaction.id}>
                            <hr />
                            <Transaction transaction={transaction} />
                        </div>
                    ))
                }
            </div>
            <hr />
            <Button
                varient="danger"
                onClick={fetchMineBlock}
            >
                Mine a block of these transactions
            </Button>
        </div>
    )
}

export default TransactionPool;