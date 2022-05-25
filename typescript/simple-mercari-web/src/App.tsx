//@ts-ignore
import { useState } from 'react';
import { Route, useHistory, Link, Switch, BrowserRouter as Router} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { ItemList } from './components/ItemList';

import { Sell } from './components/Sell'

function App() {
  // reload ItemList after Listing complete
  const [reload, setReload] = useState(true);

  const history=useHistory();

  const onClickGoSell=()=>history.push("/sell")

  return (
    <div>
      <Router>
        
        <Switch>
        <Route exact path="/">
          <div>
            <ItemList reload={reload} onLoadCompleted={() => setReload(false)} />
            <button onClick={onClickGoSell}>出品</button>
          </div>
        </Route>
        <Route path="/sell">
          <Sell setReload={setReload} />
        </Route>
        </Switch>
        
        {/* <Route path="/sell"> */}
          
        {/* </Route> */}
      </Router>
      
    </div>
  )
}

export default App;