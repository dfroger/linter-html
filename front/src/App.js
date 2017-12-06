import React, { Component } from 'react';
import './App.css';
import Sunburst from './Sunburst';
import BreadCrumbs from './BreadCrumbs';
import ErrorViewer from './ErrorViewer';

class App extends Component {
    render() {
        return (
            <div className="App">
                <Sunburst />
                <div>
                    <BreadCrumbs />
                    <ErrorViewer />
                </div>
            </div>
        );
    }
}

export default App;
