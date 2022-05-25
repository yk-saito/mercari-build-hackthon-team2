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
          <h5 className="text-center fw-bold">商品の出品</h5>
          <div>
          <Listing onListingCompleted={() => setReload(true)} />
          </div>
        <div className="text-center">
        <button type='submit' className="btn btn-danger" onClick={onClickSell}>出品する</button>
        </div>
        
        </>
    )
} 