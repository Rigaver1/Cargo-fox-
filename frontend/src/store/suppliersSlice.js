import { createSlice } from '@reduxjs/toolkit';

const suppliersSlice = createSlice({
  name: 'suppliers',
  initialState: { list: [], current: null },
  reducers: {
    setSuppliers(state, action) {
      state.list = action.payload;
    },
    setCurrentSupplier(state, action) {
      state.current = action.payload;
    },
  },
});

export const { setSuppliers, setCurrentSupplier } = suppliersSlice.actions;
export default suppliersSlice.reducer;
