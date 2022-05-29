import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';

interface Item {
  id: number;
  name: string;
  category: string;
  image_filename: string;
};

const server = process.env.API_URL || 'http://127.0.0.1:9000';
const placeholderImage = process.env.PUBLIC_URL + '/logo192.png';

interface Prop {
  reload?: boolean;
  onLoadCompleted?: () => void;
}

export const ItemList: React.FC<Prop> = (props) => {
  const { reload = true, onLoadCompleted } = props;
  const [items, setItems] = useState<Item[]>([])
  const history=useHistory();
  const onClickGoSell=()=>history.push("/sell")

  const fetchItems = () => {
    fetch(server.concat('/items'),
      {
        method: 'GET',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
      })
      .then(response => response.json())
      .then(data => {
        console.log('GET success:', data);
        setItems(data.items);
        onLoadCompleted && onLoadCompleted();
      })
      .catch(error => {
        console.error('GET error:', error)
      })
  }

  useEffect(() => {
    if (reload) {
      fetchItems();
    }
  }, [reload]);

  return (
    <div>
      <header className='Title'>
        <p>
          <b>商品一覧</b>
        </p>
        <div className='text-center'>
          <button onClick={onClickGoSell} className="btn btn-danger">出品</button>
        </div>
      </header>
    <div id="top" className='ItemList'>
      <div className="item">
      {items.map((item) => {
        return (
          <div>
            <img src={server + '/image/' + item.id + '.jpg'}/>
            <p><span>Name: {item.name}</span></p>
            <p><span>Category: {item.category}</span></p>
          </div>
        )
      })}
      </div>
    </div>

    </div>
  )
};