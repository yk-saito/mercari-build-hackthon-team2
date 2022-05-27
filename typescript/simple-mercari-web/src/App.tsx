//@ts-ignore
import { useState } from 'react';
import { Route, useHistory, Switch, BrowserRouter as Router} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { ItemList } from './components/ItemList';
import { Listing } from './components/Listing';

function App() {
  // reload ItemList after Listing complete
  const [reload, setReload] = useState(true);

  

  return (
    <div>

      <Router>
        
        <Switch>
        <Route exact path="/">
          <div>
            <ItemList reload={reload} onLoadCompleted={() => setReload(false)} />
            
          </div>
        </Route>
        <Route
          exact 
          path="/sell"
          render={(props)=>(
            <Listing onListingCompleted={() => setReload(true)} />
          )}></Route>
        </Switch>
      </Router>
      
    </div>
  )
}

export default App;