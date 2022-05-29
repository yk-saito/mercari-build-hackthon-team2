import React, { useState } from 'react';
import { useHistory } from "react-router-dom"

const server = process.env.API_URL || 'http://127.0.0.1:9000';

interface Prop {
  onListingCompleted?: () => void;
}

type formDataType = {
  name: string,
  category: string,
  image: string | File,
  flag: string,
}

export const Listing: React.FC<Prop> = (props) => {
  const { onListingCompleted } = props;
  const initialState = {
    name: "",
    category: "",
    image: "",
    flag: "false",
  };
  const [values, setValues] = useState<formDataType>(initialState);

  const history=useHistory();

  // const onClickSell=()=>history.push("/")

  const onValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({
      ...values, [event.target.name]: event.target.value,
    })
  };
  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setValues({
      ...values, [event.target.name]: event.target.files![0],
    })
  };
  const onFlagChange=()=>{
    setValues({
      ...values, flag: "true",
    })
  }
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const data = new FormData()
    data.append('name', values.name)
    data.append('category', values.category)
    data.append('image', values.image)
    data.append('flag', values.flag)
    console.log(data.get('name'));
    console.log(data.get('category'));
    console.log(data.get('image'));
    console.log(data.get('flag'));

    fetch(server.concat('/items'), {
      method: 'POST',
      mode: 'cors',
      body: data,
    })
      .then(response => {
        console.log('POST status:', response.statusText);
        onListingCompleted && onListingCompleted();
      })
      .catch((error) => {
        console.error('POST error:', error);
      })
      history.push("/")
  };
  return (
    <div className='Listing'>
      <header className='Title'>
          <p>
          <b>mercari</b>
          </p>
          </header>
          <h5 className="text-center fw-bold">商品の出品</h5>
      <form onSubmit={onSubmit} className="p-lg-5">
        <div>
          <div className="mb-3">
            <label className="form-label">商品の名前</label>
            <input type='text' name='name' className="form-control" id='name' placeholder='name' onChange={onValueChange} required />
          </div>
          <div className="mb-3">
            <label className="form-label">商品のカテゴリー</label>
            <input type='text' name='category' className="form-control" id='category' placeholder='category' onChange={onValueChange} />
          </div>
          {/* <input type='text' name='itemCondition' id='itemCondition' placeholder='itemCondition' onChange={onValueChange} /> */}
          <div className="mb-3">
            <label className="form-label">出品画像</label>
            <br/>
            <input type='file' name='image' id='image' onChange={onFileChange} required />
          </div>
          {/* <button onClick={onFlagChange}>中央に寄せる</button> */}
          <input type='checkbox' onClick={onFlagChange}/> 画像を中央配置にされますか？
          <div className="text-center">
            <button type='submit' className="btn btn-danger">出品する</button>
          </div>
          {/* <button type='submit'>出品する</button> */}
        </div>
      </form>
    </div>
  );
}
