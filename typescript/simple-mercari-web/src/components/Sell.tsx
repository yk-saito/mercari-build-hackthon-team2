import { useHistory } from "react-router-dom"
import { Listing } from './Listing';

export const Sell=(props)=>{
    const {setReload}=props
    const history=useHistory();

    const onClickSell=()=>history.push("/")

    return (
        <>
        <header className='Title'>
          <p>
          <b>mercari</b>
          </p>
          </header>
          <h4>商品の出品</h4>
          <div>
          <Listing onListingCompleted={() => setReload(true)} />
          </div>
        <button onClick={onClickSell}>出品する</button>
        </>
    )
} 