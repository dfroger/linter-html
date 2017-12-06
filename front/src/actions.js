import { SET_FLOW_DATA, SET_PATH } from './actionTypes';


export function setFlowData(data) {
    return {
        type: SET_FLOW_DATA,
        data
    }
}

export function setPath(path) {
    return {
        type: SET_PATH,
        path
    }
}
