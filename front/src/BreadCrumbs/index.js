import React, { Component } from 'react';
import { connect } from 'react-redux';


class BreadCrumbs extends Component {
    render() {
        if (this.props.path === null) {
            return <p>Click on the SunBurst to select a path</p>;
        } else {
            return <p>{this.props.path.join(' > ')}</p>;
        }
    }
}


export default connect(
    state => ({
        path: state.path
    }),
    null
)(BreadCrumbs);
