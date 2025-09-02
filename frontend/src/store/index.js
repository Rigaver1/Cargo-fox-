import { configureStore } from '@reduxjs/toolkit';
import ordersReducer from './ordersSlice';
import clientsReducer from './clientsSlice';
import suppliersReducer from './suppliersSlice';
import messagesReducer from './messagesSlice';

const store = configureStore({
  reducer: {
    orders: ordersReducer,
    clients: clientsReducer,
    suppliers: suppliersReducer,
    messages: messagesReducer,
  },
});

export default store;
