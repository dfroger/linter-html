import { SET_FLOW_DATA, SET_PATH } from './actionTypes';

export function flowReducer(state = null, action) {
    switch (action.type) {
        case SET_FLOW_DATA:
            return action.data;
        default:
            return state;
    }
}

export function pathReducer(state = null, action) {
    switch (action.type) {
        case SET_PATH:
            return action.path;
        default:
            return state;
    }
}
