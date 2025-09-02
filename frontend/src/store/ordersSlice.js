import { createSlice } from '@reduxjs/toolkit';

const ordersSlice = createSlice({
  name: 'orders',
  initialState: { list: [], current: null },
  reducers: {
    setOrders(state, action) {
      state.list = action.payload;
    },
    setCurrentOrder(state, action) {
      state.current = action.payload;
    },
  },
});

export const { setOrders, setCurrentOrder } = ordersSlice.actions;
export default ordersSlice.reducer;
